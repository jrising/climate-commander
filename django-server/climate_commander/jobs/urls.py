from django.conf.urls import url
from . import views

app_name = 'jobs'
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^create/$', views.create, name='create'),
    url(r'^run/$', views.run, name='run'),
    url(r'^run_ajax/$', views.run_ajax, name='run_ajax'),
    url(r'^stop_job/$', views.stop_job, name='stop_job'),
    url(r'^delete_jobrun/$', views.delete_jobrun, name='delete_jobrun'),
    # url(r'^simple_chart/$', views.simple_chart, name="simple_chart"),
    # url(r'^edit/$', views.edit, name='edit'),
]
