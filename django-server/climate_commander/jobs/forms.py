# from django import forms
# class JobForm(forms.Form):
#     job_name = forms.CharField(max_length=200)
#     code_url = forms.URLField(max_length=200)
#     command = forms.CharField(widget=forms.Textarea)

from django import forms
from .models import Job, Server


class JobCreateForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_name', 'code_url', 'data_used', 'result_file', 'result_directory', 'command']


class JobRunForm(forms.Form):
    job_selected = forms.ChoiceField('job_selected')

    def __init__(self, *args, **kwargs):
        super(JobRunForm, self).__init__(*args, **kwargs)
        self.fields['job_selected'].choices = [(x, x.job_name) for x in Job.objects.all()]
        for server in Server.objects.all():
            self.fields[server.server_name] = forms.IntegerField(max_value=server.server_cpus, required=True)
