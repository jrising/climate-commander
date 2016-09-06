from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Dataset(models.Model):
    dataset_name = models.CharField(max_length=200, primary_key=True, unique=True)
    size = models.FloatField()
    store_folder = models.CharField(max_length=200)

    def __unicode__(self):
        return self.dataset_name


class Server(models.Model):
    server_name = models.CharField(max_length=20)
    server_location = models.CharField(max_length=20)
    server_cpus = models.IntegerField()
    cpu_time = models.CharField(max_length=6000)
    data_hosted = models.ManyToManyField(Dataset)
    roots_data = models.CharField(max_length=50)
    roots_src = models.CharField(max_length=50)
    crdntl_user = models.CharField(max_length=50)
    crdntl_domain = models.CharField(max_length=50)
    crdntl_password = models.CharField(max_length=20)

    def __unicode__(self):
        return self.server_name


class Job(models.Model):
    job_name = models.CharField(max_length=200, unique=True)
    data_used = models.ManyToManyField(Dataset)
    code_url = models.URLField(max_length=200)
    command = models.TextField()
    result_file = models.CharField(max_length=200)
    result_directory = models.CharField(max_length=200)
    create_time = models.DateTimeField('Time Created')
    start_time = models.DateTimeField('Time When the Job Starts', null=True)
    running = models.NullBooleanField()
    server_running = models.ManyToManyField(Server, through="JobRunningOnServer")

    def __unicode__(self):
        return self.job_name


class JobRunningOnServer(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    start_time = models.DateTimeField('Time When the Job Starts')
    result_nums = models.IntegerField(null=True)
    cores_used = models.IntegerField(null=True)
    process_living = models.IntegerField(null=True)
    status = models.CharField(max_length=600, null=True)

    def __unicode__(self):
        return self.job.job_name


class Process(models.Model):
    job_spawning = models.ForeignKey(JobRunningOnServer, on_delete=models.CASCADE)
    start_time = models.DateTimeField('Time When the Process Starts')
    pid = models.IntegerField()
    status = models.CharField(max_length=20, null=True)
    log_file = models.CharField(max_length=200)

    def __unicode__(self):
        return self.job_spawning.job.job_name
