from django.conf.urls import url

from apps.main import views

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', views.dev_conf, name='url_usrp_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', views.dev_conf_edit, name='url_edit_usrp_conf'),
    url(r'^(?P<id_conf>-?\d+)/write/$', views.dev_conf_write, name='url_write_usrp_conf'),
    url(r'^(?P<id_conf>-?\d+)/read/$', views.dev_conf_read, name='url_read_usrp_conf'),
    url(r'^(?P<id_conf>-?\d+)/import/$', views.dev_conf_import, name='url_import_usrp_conf'),
    url(r'^(?P<id_conf>-?\d+)/export/$', views.dev_conf_export, name='url_export_usrp_conf'),
)
