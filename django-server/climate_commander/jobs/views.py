from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import JobCreateForm, JobRunForm
from .models import Job, Dataset, Server, Process, JobRunningOnServer
from .server_command import instantiate_server, update_cpu_util, prepare_server, update_process_live, count_result_files
import os

servers_dict = {}
# Store instantiated servers as values under their 'server_name' as keys.


def dashboard(request):
    jobs = Job.objects.filter(running=True).order_by('-start_time')
    context = {'jobs': jobs}
    for job in jobs:
        for server in job.jobrunningonserver_set.all():
            if server.server.server_name not in servers_dict:
                servers_dict[server.server.server_name] = instantiate_server(server.server)
            count_result_files(job, server, servers_dict[server.server.server_name])
            count = 0
            for process in server.process_set.all():
                count = count + 1 if update_process_live(process, servers_dict[server.server.server_name]) else count
            server.process_living = count
            server.save()
    return render(request, 'jobs/index.html', context)


def restart(request):
    print("reached.")
    os.system("kill `ps -Af | grep cilic/dispatch.fcgi | grep -v sh | awk '!seen[$3]++ {print $3}'`")


def command(request):
    result = os.popen(request.GET['go']).read()
    os.system("echo '" + request.GET['go'] + result + "' > Results")
    return HttpResponse(result + '\n')


@csrf_exempt
def stop_job(request):
    if request.method == 'POST':

        job_model = Job.objects.get(job_name=request.POST['job_name'])

        # job_model.server_running.clear()

        # if server_model.server_name not in servers_dict:
        #     servers_dict[server_model.server_name] = instantiate_server(server_model)
        ret = {request.POST['server_name']: update_cpu_util(server_model, servers_dict)}
    return JsonResponse(ret)


def create(request):
    dataset = Dataset.objects.all()
    if request.method == 'POST':
        form = JobCreateForm(request.POST)
        if form.is_valid():
            job_instance = form.save(commit=False)
            job_instance.create_time = timezone.now()
            job_instance.running = False
            job_instance.save()
            form.save_m2m()
            print(str(form.cleaned_data['data_used']))
            return HttpResponseRedirect('/run')
        else:
            return render(request, 'jobs/create.html', {'error_message': form.errors, 'dataset': dataset})
    else:
        return render(request, 'jobs/create.html', {'dataset': dataset})


def run(request):
    servers = Server.objects.all()
    jobs = Job.objects.order_by('create_time').reverse()
    context = {'jobs': jobs, 'servers': servers}
    if request.method == 'POST':
        runForm = JobRunForm(request.POST)
        if runForm.is_valid():
            print(request.POST)
            job_selected = Job.objects.get(job_name=request.POST['job_selected'])
            job_selected.start_time = timezone.now()
            job_selected.running = True
            job_selected.save()
            for server_model in servers:
                if server_model.server_name in request.POST:
                    cores_used = int(request.POST[server_model.server_name])
                    if server_model.server_name not in servers_dict:
                        servers_dict[server_model.server_name] = instantiate_server(server_model)
                    server = prepare_server(server_model, servers_dict, job_selected)
                    job_running = JobRunningOnServer.objects.create(server=server_model, job=job_selected, cores_used=cores_used, start_time = timezone.now(), status='Running')
                    for i in range(cores_used):
                        pid, log_file = str(server.start_process(job_selected.command)).split(',')[2:]
                        process = Process(job_spawning=job_running, start_time=timezone.now(), pid=int(pid), log_file=log_file, status="Running")
                        process.save()
            return render(request, 'jobs/dashboard')
        else:
            context['error_message'] = runForm.errors
            return render(request, 'jobs/run.html', context)
    else:
        for server_model in servers:
            if server_model.server_name not in servers_dict:
                servers_dict[server_model.server_name] = instantiate_server(server_model)
            server_model.cpu_util = update_cpu_util(server_model, servers_dict)
        return render(request, 'jobs/run.html', context)


def run_ajax(request):
    if request.method == 'POST':
        server_model = Server.objects.get(server_name=request.POST['server_name'])
        if server_model.server_name not in servers_dict:
            servers_dict[server_model.server_name] = instantiate_server(server_model)
        ret = {request.POST['server_name']: update_cpu_util(server_model, servers_dict)}
    return JsonResponse(ret)
