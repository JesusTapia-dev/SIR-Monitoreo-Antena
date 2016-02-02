from django.conf.urls import url

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', 'apps.dds.views.dds_conf', name='url_dds_conf'),
    url(r'^(?P<id_conf>-?\d+)/(?P<message>-?\d+)/$', 'apps.dds.views.dds_conf', name='url_dds_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', 'apps.dds.views.dds_conf_edit', name='url_edit_dds_conf'),
    url(r'^(?P<id_conf>-?\d+)/write/$', 'apps.dds.views.dds_conf_write', name='url_dds_conf_write'),
    url(r'^(?P<id_conf>-?\d+)/read/$', 'apps.dds.views.dds_conf_read', name='url_dds_conf_read'),
)
