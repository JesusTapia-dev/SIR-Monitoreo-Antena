"""radarsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'apps.main.views.index', name='index'),
    url(r'^experiment/$', 'apps.main.views.experiment', name='experiments'),
    url(r'^experiment/add/$', 'apps.main.views.add_experiment', name='add_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/$', 'apps.main.views.experiment', name='experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/edit/$', 'apps.main.views.edit_experiment', name='edit_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/device/(?P<id_dev_type>-?\d+)/$', 'apps.main.views.experiment', name='experiment_device'),
    url(r'^experiment/(?P<id_exp>-?\d+)/add_device/$', 'apps.main.views.experiment_add_device', name='experiment_add_device'),
    url(r'^device/$', 'apps.main.views.device', name='devices'),
    url(r'^device/(?P<id_dev>-?\d+)/$', 'apps.main.views.device'),
    url(r'^device/(?P<id_dev>-?\d+)/edit/$', 'apps.main.views.edit_device', name='edit_device'),
    url(r'^device/add/$', 'apps.main.views.add_device', name='add_device'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('apps.accounts.urls')),    
    url(r'^rc/', include('apps.rc.urls')),
    url(r'^dds/', include('apps.dds.urls')),
    url(r'^cgs/', include('apps.cgs.urls')),
    url(r'^jars/', include('apps.jars.urls')),
    url(r'^usrp/', include('apps.usrp.urls')),
    url(r'^abs/', include('apps.abs.urls')),
    url(r'^misc/', include('apps.misc.urls')),
]
