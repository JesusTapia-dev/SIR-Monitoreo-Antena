from django.conf.urls import url

urlpatterns = (
    #url(r'^configuration/$', 'apps.cgs.views.configurate_frequencies', name='new_device'),
#     url(r'^(?P<id>-?\d+)/$', 'apps.cgs.views.configurate_frequencies', name='new_device'),
    url(r'^(?P<id_conf>-?\d+)/$', 'apps.main.views.dev_conf', name='url_cgs_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', 'apps.main.views.dev_conf_edit', name='url_edit_cgs_conf'),
    url(r'^(?P<id_conf>-?\d+)/write/$', 'apps.main.views.dev_conf_write', name='url_write_cgs_conf'),
    url(r'^(?P<id_conf>-?\d+)/read/$', 'apps.main.views.dev_conf_read', name='url_read_cgs_conf'),
    url(r'^(?P<id_conf>-?\d+)/import/$', 'apps.main.views.dev_conf_import', name='url_import_cgs_conf'),
    url(r'^(?P<id_conf>-?\d+)/export/$', 'apps.main.views.dev_conf_export', name='url_export_cgs_conf'),
)

