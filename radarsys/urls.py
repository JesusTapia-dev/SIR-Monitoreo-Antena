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
    url(r'^operation/', 'apps.main.views.operation', name='url_operation'),    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('apps.accounts.urls')),  
    url(r'^', include('apps.main.urls')),
    url(r'^rc/', include('apps.rc.urls')),
    url(r'^dds/', include('apps.dds.urls')),
    url(r'^cgs/', include('apps.cgs.urls')),
    url(r'^jars/', include('apps.jars.urls')),
    url(r'^usrp/', include('apps.usrp.urls')),
    url(r'^abs/', include('apps.abs.urls')),
    url(r'^misc/', include('apps.misc.urls')),
]
