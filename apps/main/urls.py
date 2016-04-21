from django.conf.urls import url

urlpatterns = (
    url(r'^location/new/$', 'apps.main.views.location_new', name='url_add_location'),
    url(r'^location/$', 'apps.main.views.locations', name='url_locations'),
    url(r'^location/(?P<id_loc>-?\d+)/$', 'apps.main.views.location', name='url_location'),
    url(r'^location/(?P<id_loc>-?\d+)/edit/$', 'apps.main.views.location_edit', name='url_edit_location'),
    url(r'^location/(?P<id_loc>-?\d+)/delete/$', 'apps.main.views.location_delete', name='url_delete_location'),
    
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
    url(r'^campaign/(?P<id_camp>-?\d+)/export/$', 'apps.main.views.campaign_export', name='url_export_campaign'),
    
    url(r'^experiment/new/$', 'apps.main.views.experiment_new', name='url_add_experiment'),
    url(r'^experiment/$', 'apps.main.views.experiments', name='url_experiments'),
    url(r'^experiment/(?P<id_exp>-?\d+)/$', 'apps.main.views.experiment', name='url_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/edit/$', 'apps.main.views.experiment_edit', name='url_edit_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/delete/$', 'apps.main.views.experiment_delete', name='url_delete_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/export/$', 'apps.main.views.experiment_export', name='url_export_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/mix/$', 'apps.main.views.experiment_mix', name='url_mix_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/mix/delete/$', 'apps.main.views.experiment_mix_delete', name='url_delete_mix_experiment'),
    
    url(r'^experiment/(?P<id_exp>-?\d+)/new_dev_conf/$', 'apps.main.views.dev_conf_new', name='url_add_dev_conf'),
    url(r'^experiment/(?P<id_exp>-?\d+)/new_dev_conf/(?P<id_dev>-?\d+)/$', 'apps.main.views.dev_conf_new', name='url_add_dev_conf'),
    url(r'^dev_conf/$', 'apps.main.views.dev_confs', name='url_dev_confs'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/$', 'apps.main.views.dev_conf', name='url_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/edit/$', 'apps.main.views.dev_conf_edit', name='url_edit_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/delete/$', 'apps.main.views.dev_conf_delete', name='url_delete_dev_conf'),
        
    url(r'^dev_conf/(?P<id_conf>-?\d+)/write/$', 'apps.main.views.dev_conf_write', name='url_write_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/read/$', 'apps.main.views.dev_conf_read', name='url_read_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/import/$', 'apps.main.views.dev_conf_import', name='url_import_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/export/$', 'apps.main.views.dev_conf_export', name='url_export_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/start/$', 'apps.main.views.dev_conf_start', name='url_start_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/stop/$', 'apps.main.views.dev_conf_stop', name='url_stop_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/status/$', 'apps.main.views.dev_conf_status', name='url_status_dev_conf'),
    
    url(r'^operation/$', 'apps.main.views.operation', name='url_operation'),
    url(r'^operation/(?P<id_camp>-?\d+)/$', 'apps.main.views.operation', name='url_operation'),
    url(r'^operation/search/$', 'apps.main.views.operation_search', name='url_operation_search'),
    url(r'^operation/search/(?P<id_camp>-?\d+)/$', 'apps.main.views.operation_search', name='url_operation_search'),
    url(r'^operation/(?P<id_camp>-?\d+)/radar/(?P<id_radar>-?\d+)/play/$', 'apps.main.views.radar_play', name='url_radar_play'),
    url(r'^operation/(?P<id_camp>-?\d+)/radar/(?P<id_radar>-?\d+)/stop/$', 'apps.main.views.radar_stop', name='url_radar_stop'),
    url(r'^operation/(?P<id_camp>-?\d+)/radar/(?P<id_radar>-?\d+)/refresh/$', 'apps.main.views.radar_refresh', name='url_radar_refresh'),
    
)
