from django.conf.urls import url

import views

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', views.abs_conf, name='url_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', views.abs_conf_edit, name='url_edit_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/read/$', views.dev_conf_read, name='url_read_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/import/$', views.dev_conf_import, name='url_import_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/export/$', views.dev_conf_export, name='url_export_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/plot/$', views.plot_patterns, name='url_plot_abs_patterns'),
    url(r'^(?P<id_conf>-?\d+)/add_beam/$', views.add_beam, name='url_add_abs_beam'),
    url(r'^(?P<id_conf>-?\d+)/beam/(?P<id_beam>-?\d+)/delete/$', views.remove_beam, name='url_remove_abs_beam'),
    url(r'^(?P<id_conf>-?\d+)/beam/(?P<id_beam>-?\d+)/edit/$', views.edit_beam, name='url_edit_abs_beam'),
)
