from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Dataset(models.Model):
    dataset_name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.dataset_name


class Server(models.Model):
    server_name = models.CharField(max_length=200)
    # server_cpus = models.IntegerField()
    # roots_data = models.CharField(max_length=50)
    # roots_src = models.CharField(max_length=50)
    # crdntl_user = models.CharField(max_length=50)
    # crdntl_domain = models.CharField(max_length=50)
    # crdntl_password = models.CharField(max_length=20)
    data_hosted = models.ManyToManyField(Dataset)

    def __str__(self):
        return self.server_name


class Job(models.Model):
    job_name = models.CharField(max_length=200)
    data_used = models.ManyToManyField(Dataset)
    code_url = models.URLField(max_length=200)
    command = models.TextField()
    create_time = models.DateTimeField('Time Created')

    def __str__(self):
        return self.job_name
