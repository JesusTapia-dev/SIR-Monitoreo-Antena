from django.conf.urls import url

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', 'apps.cgs.views.cgs_conf', name='url_cgs_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', 'apps.cgs.views.cgs_conf_edit', name='url_edit_cgs_conf'),
    #url(r'^(?P<id_conf>-?\d+)/(?P<message>-?\d+)/$', 'apps.cgs.views.cgs_conf', name='url_cgs_conf'),
#     url(r'^(?P<id_conf>-?\d+)/edit/$', 'apps.cgs.views.cgs_conf_edit', name='url_edit_cgs_conf'),
#     url(r'^(?P<id_conf>-?\d+)/write/$', 'apps.cgs.views.cgs_conf_write', name='url_write_cgs_conf'),
#     url(r'^(?P<id_conf>-?\d+)/read/$', 'apps.cgs.views.cgs_conf_read', name='url_read_cgs_conf'),
#     url(r'^(?P<id_conf>-?\d+)/import/$', 'apps.cgs.views.cgs_conf_import', name='url_import_cgs_conf'),
#     url(r'^(?P<id_conf>-?\d+)/export/$', 'apps.cgs.views.cgs_conf_export', name='url_export_cgs_conf'),
    #url(r'^(?P<id_conf>-?\d+)/export/$', 'apps.main.views.dev_conf_export', name='url_export_cgs_conf'),
)

