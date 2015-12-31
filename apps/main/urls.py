from django.conf.urls import url

urlpatterns = (
    
    url(r'^device/add/$', 'apps.main.views.add_device', name='url_add_device'),
    url(r'^device/$', 'apps.main.views.devices', name='url_devices'),
    url(r'^device/(?P<id_dev>-?\d+)/$', 'apps.main.views.device', name='url_device'),
    url(r'^device/(?P<id_dev>-?\d+)/edit/$', 'apps.main.views.edit_device', name='url_edit_device'),
    
    url(r'^campaign/add/$', 'apps.main.views.add_campaign', name='url_add_campaign'),
    url(r'^campaign/$', 'apps.main.views.campaigns', name='url_campaigns'),
    url(r'^campaign/(?P<id_camp>-?\d+)/$', 'apps.main.views.campaign', name='url_campaign'),
    url(r'^campaign/(?P<id_camp>-?\d+)/edit/$', 'apps.main.views.edit_campaign', name='url_edit_campaign'),
    
    url(r'^campaign/(?P<id_camp>-?\d+)/add_experiment/$', 'apps.main.views.add_experiment', name='url_add_experiment'),
    url(r'^experiment/$', 'apps.main.views.experiments', name='url_experiments'),
    url(r'^experiment/(?P<id_exp>-?\d+)/$', 'apps.main.views.experiment', name='url_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/edit/$', 'apps.main.views.edit_experiment', name='url_edit_experiment'),

    url(r'^experiment/(?P<id_exp>-?\d+)/add_dev_conf/$', 'apps.main.views.add_dev_conf', name='url_add_dev_conf'),
    url(r'^dev_conf/$', 'apps.main.views.dev_confs', name='url_dev_confs'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/$', 'apps.main.views.dev_conf', name='url_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/edit/$', 'apps.main.views.edit_dev_conf', name='url_edit_dev_conf'),
      
)
