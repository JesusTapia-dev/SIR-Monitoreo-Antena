from django.conf.urls import url

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', 'apps.abs.views.abs_conf', name='url_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', 'apps.abs.views.abs_conf_edit', name='url_edit_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/read/$', 'apps.main.views.dev_conf_read', name='url_read_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/import/$', 'apps.main.views.dev_conf_import', name='url_import_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/export/$', 'apps.main.views.dev_conf_export', name='url_export_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/plot/$', 'apps.abs.views.plot_patterns', name='url_plot_abs_patterns'),
    url(r'^(?P<id_conf>-?\d+)/add_beam/$', 'apps.abs.views.add_beam', name='url_add_abs_beam'),
    url(r'^(?P<id_conf>-?\d+)/beam/(?P<id_beam>-?\d+)/delete/$', 'apps.abs.views.remove_beam', name='url_remove_abs_beam'),
    url(r'^(?P<id_conf>-?\d+)/beam/(?P<id_beam>-?\d+)/edit/$', 'apps.abs.views.edit_beam', name='url_edit_abs_beam'),
)
