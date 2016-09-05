from django.conf.urls import url

from apps.dds import views

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', views.dds_conf, name='url_dds_conf'),
    url(r'^(?P<id_conf>-?\d+)/(?P<message>-?\d+)/$', views.dds_conf, name='url_dds_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', views.dds_conf_edit, name='url_edit_dds_conf'),
)
