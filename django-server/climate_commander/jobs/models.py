from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Dataset(models.Model):
    dataset_name = models.CharField(max_length=200, primary_key=True, unique=True)
    size = models.FloatField()

    def __str__(self):
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

    def __str__(self):
        return self.server_name


class Job(models.Model):
    job_name = models.CharField(max_length=200, unique=True)
    data_used = models.ManyToManyField(Dataset)
    code_url = models.URLField(max_length=200)
    command = models.TextField()
    create_time = models.DateTimeField('Time Created')

    def __str__(self):
        return self.job_name
