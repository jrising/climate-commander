from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import JobCreateForm, JobRunForm
from .models import Job, Dataset, Server, Process, JobRunningOnServer
from .server_command import instantiate_server, update_cpu_util, prepare_server, update_process_live, count_result_files, run_job
import subprocess, os

# Store instantiated servers as values under their 'server_name' as keys.
servers_dict = {}


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


def save_results(request):
    # targetJob = request.GET['job']
    os.system("scp -F /home/jongkai/.ssh/config griffinvm:~/DummyTarget ./")
    return HttpResponseRedirect('/')


def restart(request):
    print("reached.")
    os.system("kill `ps -Af | grep cilic/dispatch.fcgi | grep -v sh | awk '!seen[$3]++ {print $3}'`")


def command(request):
    # TODO: Confirm IP Address before executing
    # TODO: Integrate the restart function
    ip = request.META.get('REMOTE_ADDR')
    com = request.GET['go'].split()
    exect = subprocess.Popen(com, stdout=subprocess.PIPE)
    result = exect.communicate()
    exect.wait()
    # result = os.popen(request.GET['go']).read()
    os.system("echo '" + request.GET['go'] + result + "' >> Results")
    os.system("echo '" + ip + "' >> Results")
    sshAgentList = os.popen("find /tmp/ -type s -name agent.* 2>/dev/null | grep '/tmp/ssh-.*/agent.*'").read().split("\n")[:-1]
    for i in range(len(sshAgentList)):
        os.system("kill " + str(int(sshAgentList[i].split(".")[1])+1))
    return HttpResponse(result + '\n' + ip + '\n')


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
    # Models for rendering the /run page
    servers = Server.objects.all()
    jobs = Job.objects.order_by('create_time').reverse()
    context = {'jobs': jobs, 'servers': servers}

    # User decided to run a job (Hit the run button), post requesting a form specifying the number of cores used on each server
    if request.method == 'POST':
        print("got POST request")
        runForm = JobRunForm(request.POST)
        if runForm.is_valid():
            print(request.POST)
            job_selected = Job.objects.get(job_name=request.POST['job_selected'])
            job_selected.start_time = timezone.now()
            job_selected.running = True
            job_selected.save()
            for server_model in servers:
                if server_model.server_name in request.POST:
                    cores_used = int(request.POST[server_model.server_name][0])
                    if cores_used > 0:
                        if server_model.server_name not in servers_dict:
                            servers_dict[server_model.server_name] = instantiate_server(server_model, debug=False)

                        server, message = prepare_server(server_model, servers_dict, job_selected)
                        context['message'] = message
                        if JobRunningOnServer.objects.filter(job=job_selected, server=server_model).exists():
                            job_running = JobRunningOnServer.objects.filter(job=job_selected, server=server_model)
                        else:
                            job_running = JobRunningOnServer.objects.create(server=server_model,
                                                                            job=job_selected, cores_used=cores_used,
                                                                            start_time=timezone.now(), status='Running')
                        pid_list = run_job(server_model, server, job_selected, cores_used)
                        for i in range(cores_used):
                            process = Process(job_spawning=job_running, start_time=timezone.now(),
                                              pid=int(pid_list[i][0]), log_file=pid_list[i][1], status="Running")
                            process.save()
            return HttpResponseRedirect('/')
            # return render(request, 'jobs/index.html')
        else:
            context['message'] = runForm.errors
            return render(request, 'jobs/run.html', context)
    else:
        for server_model in servers:
            if server_model.server_name not in servers_dict:
                servers_dict[server_model.server_name] = instantiate_server(server_model)
            server_model.cpu_util = update_cpu_util(server_model, servers_dict)
        return render(request, 'jobs/run.html', context)


# AJAX update CPU utilization for each server
def run_ajax(request):
    if request.method == 'POST':
        server_model = Server.objects.get(server_name=request.POST['server_name'])
        if server_model.server_name not in servers_dict:
            servers_dict[server_model.server_name] = instantiate_server(server_model)
        ret = {request.POST['server_name']: update_cpu_util(server_model, servers_dict)}
    return JsonResponse(ret)
