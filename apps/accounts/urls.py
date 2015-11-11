from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}),
)
