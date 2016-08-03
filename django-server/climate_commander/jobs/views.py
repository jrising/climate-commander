from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from .forms import JobForm
from .models import Job, Dataset, Server


def dashboard(request):
    return render(request, 'jobs/index.html', )


def create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job_instance = form.save(commit=False)
            job_instance.create_time = timezone.now()
            job_instance.save()
            form.save_m2m()
            print(str(form.cleaned_data['data_used']))
            return HttpResponseRedirect(reverse('run'))
        else:
            return render(request, 'jobs/create.html', {'error_message': form.errors})
    else:
        form = JobForm()
        dataset = Dataset.objects.all()
        return render(request, 'jobs/create.html', {'dataset': dataset})


def run(request):
    jobs = Job.objects.all()
    context = {'jobs': jobs}
    return render(request, 'jobs/run.html', context)


def run_ajax(request):
    if request.method == 'POST':
        job_selected = request.GET['job_selected']
        job_return = Job.objects.filter("job_name" == job_selected)
        print(job_selected, job_return)
        return HttpResponse(job_return)
