from django.conf.urls import url

from apps.jars import views

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', views.jars_conf, name='url_jars_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', views.jars_conf_edit, name='url_edit_jars_conf'),    
    url(r'^(?P<conf_id>-?\d+)/change_filter/$', views.change_filter, name='url_change_jars_filter'),
    url(r'^(?P<conf_id>-?\d+)/change_filter/(?P<filter_id>-?\d+)/$', views.change_filter, name='url_change_jars_filter'),
    url(r'^(?P<conf_id>-?\d+)/import/$', views.import_file, name='url_import_jars_conf'),
    url(r'^(?P<conf_id>-?\d+)/read/$', views.read_conf, name='url_read_jars_conf'),
    url(r'^(?P<conf_id>-?\d+)/get_log/$', views.get_log, name='url_get_jars_log'),
)
