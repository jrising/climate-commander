from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import JobCreateForm, JobRunForm
from .models import Job, Dataset, Server, Process, JobRunningOnServer
from .server_command import instantiate_server, update_cpu_util, prepare_server, update_process_live, count_result_files

servers_dict = {}
# Store instantiated servers as values under their 'server_name' as keys.


def dashboard(request):
    jobs = Job.objects.filter(running=True).order_by('-start_time')
    context = {'jobs': jobs}
    for job in jobs:
        for jobrun in job.jobrunningonserver_set.all():
            if jobrun.server.server_name not in servers_dict:
                servers_dict[jobrun.server.server_name] = instantiate_server(jobrun.server)
            count_result_files(job, jobrun, servers_dict[jobrun.server.server_name])
            count = 0
            for process in jobrun.process_set.all():
                count = count + 1 if update_process_live(process, servers_dict[jobrun.server.server_name]) else count
            jobrun.process_living = count
            jobrun.save()
    return render(request, 'jobs/index.html', context)


@csrf_exempt
def stop_job(request):
    if request.method == 'POST':

        job_model = Job.objects.get(job_name=request.POST['job_name'])

        # job_model.server_running.clear()

        # if server_model.server_name not in servers_dict:
        #     servers_dict[server_model.server_name] = instantiate_server(server_model)
        ret = {request.POST['server_name']: update_cpu_util(server_model, servers_dict)}
    return JsonResponse(ret)

@csrf_exempt
def delete_jobrun(request):
    ret = {}
    if request.method == 'POST':
        jobrun = JobRunningOnServer.objects.get(id=request.POST['id'])
        jobrun.delete()
        ret = {'status': 'success'}
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
            return HttpResponseRedirect(reverse('run'))
        else:
            return render(request, 'jobs/create.html', {'error_message': form.errors, 'dataset': dataset})
    else:
        return render(request, 'jobs/create.html', {'dataset': dataset})

@login_required
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
            for server_model in servers:
                if server_model.server_name in request.POST:
                    cores_used = int(request.POST[server_model.server_name])
                    if server_model.server_name not in servers_dict:
                        servers_dict[server_model.server_name] = instantiate_server(server_model)
                    server = prepare_server(server_model, servers_dict, job_selected)
                    job_running = JobRunningOnServer.objects.create(server=server_model, job=job_selected, cores_used=cores_used, start_time = timezone.now(), status='Running')
                    for i in range(cores_used):
                        proc = server.start_process(job_selected.command)
                        process = Process(job_spawning=job_running, start_time=timezone.now(), pid=int(proc.pid), log_file=proc.logfile, status="Running")
                        process.save()
            job_selected.save()
            return HttpResponseRedirect(reverse('dashboard'))
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
