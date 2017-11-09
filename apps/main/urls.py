from django.conf.urls import url

from apps.main import views

urlpatterns = (
    url(r'^$', views.index, name='index'),

    url(r'^realtime/$', views.real_time, name='url_real_time'),

    url(r'^location/new/$', views.location_new, name='url_add_location'),
    url(r'^location/$', views.locations, name='url_locations'),
    url(r'^location/(?P<id_loc>-?\d+)/$', views.location, name='url_location'),
    url(r'^location/(?P<id_loc>-?\d+)/edit/$', views.location_edit, name='url_edit_location'),
    url(r'^location/(?P<id_loc>-?\d+)/delete/$', views.location_delete, name='url_delete_location'),

    url(r'^device/new/$', views.device_new, name='url_add_device'),
    url(r'^device/$', views.devices, name='url_devices'),
    url(r'^device/(?P<id_dev>-?\d+)/$', views.device, name='url_device'),
    url(r'^device/(?P<id_dev>-?\d+)/edit/$', views.device_edit, name='url_edit_device'),
    url(r'^device/(?P<id_dev>-?\d+)/delete/$', views.device_delete, name='url_delete_device'),
    url(r'^device/(?P<id_dev>-?\d+)/change_ip/$', views.device_change_ip, name='url_change_ip_device'),

    url(r'^campaign/new/$', views.campaign_new, name='url_add_campaign'),
    url(r'^campaign/$', views.campaigns, name='url_campaigns'),
    url(r'^campaign/(?P<id_camp>-?\d+)/$', views.campaign, name='url_campaign'),
    url(r'^campaign/(?P<id_camp>-?\d+)/edit/$', views.campaign_edit, name='url_edit_campaign'),
    url(r'^campaign/(?P<id_camp>-?\d+)/delete/$', views.campaign_delete, name='url_delete_campaign'),
    url(r'^campaign/(?P<id_camp>-?\d+)/export/$', views.campaign_export, name='url_export_campaign'),
    url(r'^campaign/(?P<id_camp>-?\d+)/import/$', views.campaign_import, name='url_import_campaign'),

    url(r'^experiment/new/$', views.experiment_new, name='url_add_experiment'),
    url(r'^experiment/$', views.experiments, name='url_experiments'),
    url(r'^experiment/(?P<id_exp>-?\d+)/$', views.experiment, name='url_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/edit/$', views.experiment_edit, name='url_edit_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/delete/$', views.experiment_delete, name='url_delete_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/export/$', views.experiment_export, name='url_export_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/import/$', views.experiment_import, name='url_import_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/start/$', views.experiment_start, name='url_start_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/stop/$', views.experiment_stop, name='url_stop_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/mix/$', views.experiment_mix, name='url_mix_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/mix/delete/$', views.experiment_mix_delete, name='url_delete_mix_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/summary/$', views.experiment_summary, name='url_sum_experiment'),
    url(r'^experiment/(?P<id_exp>-?\d+)/verify/$', views.experiment_verify, name='url_verify_experiment'),

    url(r'^experiment/(?P<id_exp>-?\d+)/new_dev_conf/$', views.dev_conf_new, name='url_add_dev_conf'),
    url(r'^experiment/(?P<id_exp>-?\d+)/new_dev_conf/(?P<id_dev>-?\d+)/$', views.dev_conf_new, name='url_add_dev_conf'),
    url(r'^dev_conf/$', views.dev_confs, name='url_dev_confs'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/$', views.dev_conf, name='url_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/edit/$', views.dev_conf_edit, name='url_edit_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/delete/$', views.dev_conf_delete, name='url_delete_dev_conf'),

    url(r'^dev_conf/(?P<id_conf>-?\d+)/write/$', views.dev_conf_write, name='url_write_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/read/$', views.dev_conf_read, name='url_read_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/import/$', views.dev_conf_import, name='url_import_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/export/$', views.dev_conf_export, name='url_export_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/start/$', views.dev_conf_start, name='url_start_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/stop/$', views.dev_conf_stop, name='url_stop_dev_conf'),
    url(r'^dev_conf/(?P<id_conf>-?\d+)/status/$', views.dev_conf_status, name='url_status_dev_conf'),

    url(r'^operation/$', views.operation, name='url_operation'),
    url(r'^operation/(?P<id_camp>-?\d+)/$', views.operation, name='url_operation'),    
    url(r'^operation/(?P<id_camp>-?\d+)/radar/(?P<id_radar>-?\d+)/start/$', views.radar_start, name='url_radar_start'),
    url(r'^operation/(?P<id_camp>-?\d+)/radar/(?P<id_radar>-?\d+)/stop/$', views.radar_stop, name='url_radar_stop'),
    url(r'^operation/(?P<id_camp>-?\d+)/radar/(?P<id_radar>-?\d+)/refresh/$', views.radar_refresh, name='url_radar_refresh'),
)
