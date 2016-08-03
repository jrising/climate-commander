# from django import forms
# class JobForm(forms.Form):
#     job_name = forms.CharField(max_length=200)
#     code_url = forms.URLField(max_length=200)
#     command = forms.CharField(widget=forms.Textarea)

from django.forms import ModelForm
from .models import Job


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['job_name', 'data_used', 'code_url', 'command']
