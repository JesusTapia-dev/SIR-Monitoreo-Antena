from django.conf.urls import url

from apps.cgs import views

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', views.cgs_conf, name='url_cgs_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', views.cgs_conf_edit, name='url_edit_cgs_conf'),
)
