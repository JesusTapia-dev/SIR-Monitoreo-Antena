from django.conf.urls import url

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', 'apps.dds.views.config_dds', name='url_conf_dds'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', 'apps.dds.views.config_dds_edit', name='url_conf_dds_edit'),
)
