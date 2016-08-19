from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from .forms import JobCreateForm, JobRunForm
from .models import Job, Dataset, Server, JobRunningOnServer
from .server_command import instantiate_server, update_cpu_util, prepare_server, run_job


def dashboard(request):
    return render(request, 'jobs/index.html', )


def create(request):
    dataset = Dataset.objects.all()
    if request.method == 'POST':
        form = JobCreateForm(request.POST)
        if form.is_valid():
            job_instance = form.save(commit=False)
            job_instance.create_time = timezone.now()
            job_instance.save()
            form.save_m2m()
            print(str(form.cleaned_data['data_used']))
            return HttpResponseRedirect(reverse('jobs:run'))
        else:
            return render(request, 'jobs/create.html', {'error_message': form.errors, 'dataset': dataset})
    else:
        return render(request, 'jobs/create.html', {'dataset': dataset})

servers_dict = {}
# Store instantiated servers as values under their 'server_name' as keys.


def run(request):
    servers = Server.objects.all()
    jobs = Job.objects.order_by('create_time').reverse()
    context = {'jobs': jobs, 'servers': servers}
    if request.method == 'POST':
        runForm = JobRunForm(request.POST)
        if runForm.is_valid():
            print(request.POST)
            job_selected = Job.objects.get(job_name=request.POST['job_selected'])
            for server_model in servers:
                if server_model.server_name not in servers_dict:
                    servers_dict[server_model.server_name] = instantiate_server(server_model)
                if server_model.server_name in request.POST:
                    job_running = JobRunningOnServer.objects.create(server=server_model, job=job_selected, start_time=timezone.now())
                    prepare_server(server_model, servers_dict, job_selected, job_running)
                    pid = []
                    for i in range(int(request.POST[server_model.server_name])):
                        # run_job(server_model, servers_dict, job_selected, job_running)
                        pid.append(str(servers_dict[server_model.server_name].start_process(job_selected.command)) + "\n")
                    job_running.pid = pid
                    job_running.save()
            return HttpResponseRedirect(reverse('jobs:dashboard'))
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
        server = Server.objects.get(server_name=request.POST['server_name'])
        ret = {request.POST['server_name']: update_cpu_util(server, servers_dict)}
    return JsonResponse(ret)
