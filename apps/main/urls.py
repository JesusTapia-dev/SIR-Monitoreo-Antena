from django.urls import path

from . import views

urlpatterns = (
    path('', views.index, name='index'),

    path('realtime/', views.real_time, name='url_real_time'),

    path('theme/(<str:theme>/', views.theme, name='url_theme'),

    path('location/new/', views.location_new, name='url_add_location'),
    path('location/', views.locations, name='url_locations'),
    path('location/<int:id_loc>/', views.location, name='url_location'),
    path('location/<int:id_loc>/edit/', views.location_edit, name='url_edit_location'),
    path('location/<int:id_loc>/delete/', views.location_delete, name='url_delete_location'),

    path('device/new/', views.device_new, name='url_add_device'),
    path('device/', views.devices, name='url_devices'),
    path('device/<int:id_dev>/', views.device, name='url_device'),
    path('device/<int:id_dev>/edit/', views.device_edit, name='url_edit_device'),
    path('device/<int:id_dev>/delete/', views.device_delete, name='url_delete_device'),
    path('device/<int:id_dev>/change_ip/', views.device_change_ip, name='url_change_ip_device'),

    path('campaign/new/', views.campaign_new, name='url_add_campaign'),
    path('campaign/', views.campaigns, name='url_campaigns'),
    path('campaign/<int:id_camp>/', views.campaign, name='url_campaign'),
    path('campaign/<int:id_camp>/edit/', views.campaign_edit, name='url_edit_campaign'),
    path('campaign/<int:id_camp>/delete/', views.campaign_delete, name='url_delete_campaign'),
    path('campaign/<int:id_camp>/export/', views.campaign_export, name='url_export_campaign'),
    path('campaign/<int:id_camp>/import/', views.campaign_import, name='url_import_campaign'),

    path('experiment/new/', views.experiment_new, name='url_add_experiment'),
    path('experiment/', views.experiments, name='url_experiments'),
    path('experiment/<int:id_exp>/', views.experiment, name='url_experiment'),
    path('experiment/<int:id_exp>/edit/', views.experiment_edit, name='url_edit_experiment'),
    path('experiment/<int:id_exp>/delete/', views.experiment_delete, name='url_delete_experiment'),
    path('experiment/<int:id_exp>/export/', views.experiment_export, name='url_export_experiment'),
    path('experiment/<int:id_exp>/import/', views.experiment_import, name='url_import_experiment'),
    path('experiment/<int:id_exp>/start/', views.experiment_start, name='url_start_experiment'),
    path('experiment/<int:id_exp>/stop/', views.experiment_stop, name='url_stop_experiment'),
    path('experiment/<int:id_exp>/mix/', views.experiment_mix, name='url_mix_experiment'),
    path('experiment/<int:id_exp>/mix/delete/', views.experiment_mix_delete, name='url_delete_mix_experiment'),
    path('experiment/<int:id_exp>/summary/', views.experiment_summary, name='url_sum_experiment'),
    path('experiment/<int:id_exp>/verify/', views.experiment_verify, name='url_verify_experiment'),

    path('experiment/<int:id_exp>/new_dev_conf/', views.dev_conf_new, name='url_add_dev_conf'),
    path('experiment/<int:id_exp>/new_dev_conf/<int:id_dev>/', views.dev_conf_new, name='url_add_dev_conf'),
    
    path('dev_conf/', views.dev_confs, name='url_dev_confs'),
    path('dev_conf/<int:id_conf>/', views.dev_conf, name='url_dev_conf'),
    path('dev_conf/<int:id_conf>/edit/', views.dev_conf_edit, name='url_edit_dev_conf'),
    path('dev_conf/<int:id_conf>/delete/', views.dev_conf_delete, name='url_delete_dev_conf'),

    path('dev_conf/<int:id_conf>/write/', views.dev_conf_write, name='url_write_dev_conf'),
    path('dev_conf/<int:id_conf>/read/', views.dev_conf_read, name='url_read_dev_conf'),
    path('dev_conf/<int:id_conf>/import/', views.dev_conf_import, name='url_import_dev_conf'),
    path('dev_conf/<int:id_conf>/export/', views.dev_conf_export, name='url_export_dev_conf'),
    path('dev_conf/<int:id_conf>/start/', views.dev_conf_start, name='url_start_dev_conf'),
    path('dev_conf/<int:id_conf>/stop/', views.dev_conf_stop, name='url_stop_dev_conf'),
    path('dev_conf/<int:id_conf>/status/', views.dev_conf_status, name='url_status_dev_conf'),

    path('operation/', views.operation, name='url_operation'),
    path('operation/<int:id_camp>/', views.operation, name='url_operation'),
    #path('operation/<int:id_camp>/revoke', views.revoke_tasks, name='url_operation_revoke'),
    #path('operation/<int:id_camp>/show', views.show_tasks, name='url_operation_show'),
    path('operation/<int:id_camp>/radar/<int:id_radar>/start/', views.radar_start, name='url_radar_start'),
    path('operation/<int:id_camp>/radar/<int:id_radar>/stop/', views.radar_stop, name='url_radar_stop'),
    path('operation/<int:id_camp>/radar/<int:id_radar>/refresh/', views.radar_refresh, name='url_radar_refresh'),
)
