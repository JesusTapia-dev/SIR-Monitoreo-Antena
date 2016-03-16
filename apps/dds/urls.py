from django.conf.urls import url

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', 'apps.dds.views.dds_conf', name='url_dds_conf'),
    url(r'^(?P<id_conf>-?\d+)/(?P<message>-?\d+)/$', 'apps.dds.views.dds_conf', name='url_dds_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', 'apps.dds.views.dds_conf_edit', name='url_edit_dds_conf'),
#     url(r'^(?P<id_conf>-?\d+)/write/$', 'apps.dds.views.dds_conf_write', name='url_write_dds_conf'),
#     url(r'^(?P<id_conf>-?\d+)/read/$', 'apps.dds.views.dds_conf_read', name='url_read_dds_conf'),
#     url(r'^(?P<id_conf>-?\d+)/import/$', 'apps.dds.views.dds_conf_import', name='url_import_dds_conf'),
#     url(r'^(?P<id_conf>-?\d+)/export/$', 'apps.dds.views.dds_conf_export', name='url_export_dds_conf'),
#     url(r'^(?P<id_conf>-?\d+)/start/$', 'apps.dds.views.dds_conf_start', name='url_start_dds_conf'),
#     url(r'^(?P<id_conf>-?\d+)/stop/$', 'apps.dds.views.dds_conf_stop', name='url_stop_dds_conf'),
#     url(r'^(?P<id_conf>-?\d+)/status/$', 'apps.dds.views.dds_conf_status', name='url_status_dds_conf'),
)
