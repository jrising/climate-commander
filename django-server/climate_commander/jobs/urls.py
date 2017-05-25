from django.conf.urls import url
from . import views

app_name = 'jobs'
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^create/$', views.create, name='create'),
    url(r'^run/$', views.run, name='run'),
    url(r'^run_ajax/$', views.run_ajax, name='run_ajax'),
    url(r'^stop_job/$', views.stop_job, name='stop_job'),
    url(r'^restart$', views.restart, name='restart'),
    url(r'^command$', views.command, name='command'),
    # url(r'^edit/$', views.edit, name='edit'),
    url(r'^save_results/$', views.save_results, name="save_results"),
    url(r'^populate_tree/$', views.populate_tree, name='populate_tree')
]
