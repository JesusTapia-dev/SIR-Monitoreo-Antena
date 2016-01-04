from django.conf.urls import url

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', 'apps.dds.views.dds_conf', name='url_dds_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', 'apps.dds.views.dds_conf_edit', name='url_edit_dds_conf'),
)
