from django.conf.urls import patterns, url

from . import views

#urlpatterns = patterns('apps.cgs.views',
#    url(r'^$', views.index, name='index')
#)

urlpatterns = (
    url(r'^configuration/$', 'apps.cgs.views.configurate_frequencies', name='new_device'),
)

#url(r'^new/experiment/$', 'apps.main.views.new_experiment', name='new_experiment')

