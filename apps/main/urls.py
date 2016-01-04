from django.conf.urls import url

urlpatterns = (
    url(r'^device/new/$', 'apps.main.views.device_new', name='url_add_device'),
    url(r'^device/$', 'apps.main.views.devices', name='url_devices'),
    url(r'^device/(?P<id_dev>-?\d+)/$', 'apps.main.views.device', name='url_device'),
    url(r'^device/(?P<id_dev>-?\d+)/edit/$', 'apps.main.views.device_edit', name='url_edit_device'),
    url(r'^device/(?P<id_dev>-?\d+)/delete/$', 'apps.main.views.device_delete', name='url_delete_device'),
    
    url(r'^campaign/new/$', 'apps.main.views.campaign_new', name='url_add_campaign'),
    url(r'^campaign/$', 'apps.main.views.campaigns', name='url_campaigns'),
    url(r'^campaign/(?P<id_camp>-?\d+)/$', 'apps.main.views.campaign', name='url_campaign'),
    url(r'^campaign/(?P<id_camp>-?\d+)/edit/$', 'apps.main.views.campaign_edit', name='url_edit_campaign'),
    url(r'^campaign/(?P<id_camp>-?\d+)/delete/$', 'apps.main.views.campaign_delete', name='url_delete_campaign'),
    
    url(r'^campaign/(?P<id_camp>-?\d+)/new_experiment/$', 'apps.main.views.experiment_new', name='url_add_experiment'),
    url(r'^experiment/$', 'apps.main.views.experiments', name='url_experiments'),
    url(r'^experiment/(?P<id_exp>-?\d+)/$', 'apps.main.views.experiment', name='url_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/edit/$', 'apps.main.views.experiment_edit', name='url_edit_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/delete/$', 'apps.main.views.experiment_delete', name='url_delete_experiment'),
    
    url(r'^experiment/(?P<id_exp>-?\d+)/new_dev_conf/$', 'apps.main.views.dev_conf_new', name='url_add_dev_conf'),
    url(r'^dev_conf/$', 'apps.main.views.dev_confs', name='url_dev_confs'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/$', 'apps.main.views.dev_conf', name='url_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/edit/$', 'apps.main.views.dev_conf_edit', name='url_edit_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/delete/$', 'apps.main.views.dev_conf_delete', name='url_delete_dev_conf'),
)
