from django.conf.urls import url
from . import views

app_name = 'jobs'
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^create/$', views.create, name='create'),
    url(r'^run/$', views.run, name='run'),
    url(r'^run_ajax/$', views.run_ajax, name='run'),
]
