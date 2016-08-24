from django.contrib import admin
from .models import Job, Server, Dataset, Process, JobRunningOnServer
# Register your models here.

admin.site.register(Job)
admin.site.register(Server)
admin.site.register(Dataset)
admin.site.register(Process)
admin.site.register(JobRunningOnServer)
