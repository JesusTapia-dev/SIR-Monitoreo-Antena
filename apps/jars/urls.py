from django.conf.urls import url

urlpatterns = (
#     url(r'^(?P<id>-?\d+)/$', 'apps.jars.views.jars_config', name='jars'),
    url(r'^(?P<id_conf>-?\d+)/$', 'apps.main.views.dev_conf', name='url_jars_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', 'apps.main.views.dev_conf_edit', name='url_edit_jars_conf'),
    url(r'^(?P<id_conf>-?\d+)/write/$', 'apps.main.views.dev_conf_write', name='url_write_jars_conf'),
    url(r'^(?P<id_conf>-?\d+)/read/$', 'apps.main.views.dev_conf_read', name='url_read_jars_conf'),
    url(r'^(?P<id_conf>-?\d+)/import/$', 'apps.main.views.dev_conf_import', name='url_import_jars_conf'),
    url(r'^(?P<id_conf>-?\d+)/export/$', 'apps.main.views.dev_conf_export', name='url_export_jars_conf'),
)
