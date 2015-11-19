from django.conf.urls import url

urlpatterns = (
    url(r'^new/experiment/$', 'apps.main.views.new_experiment', name='new_experiment'),
    url(r'^new/device/$', 'apps.main.views.new_device', name='new_device'),
    url(r'^experiment/(?P<idtemplate>-?\d+)/$', 'apps.main.views.index', name='template'),
)
