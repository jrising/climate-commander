from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from .forms import JobForm
from .models import Job, Dataset, Server
from .server_command import instantiate_server, update_cpu_util

def dashboard(request):
    return render(request, 'jobs/index.html', )


def create(request):
    dataset = Dataset.objects.all()
    if request.method == 'POST':
        form = JobForm(request.POST)
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


def run(request):
    if request.method == 'POST':
        print(request.POST)
        job_selected = request.POST['job_selected']
        return HttpResponseRedirect(reverse('jobs:dashboard'))
    else:
        jobs = Job.objects.order_by('create_time').reverse()
        servers = Server.objects.all()
        for i in servers:
            servers_dict[i.server_name] = instantiate_server(i)
            i.cpu_util = update_cpu_util(i, servers_dict)
        context = {'jobs': jobs, 'servers': servers}
        return render(request, 'jobs/run.html', context)


def run_ajax(request):
    if request.method == 'POST':
        server = Server.objects.get(server_name=request.POST['server_name'])
        ret = {request.POST['server_name']: update_cpu_util(server, servers_dict)}
    return JsonResponse(ret)
