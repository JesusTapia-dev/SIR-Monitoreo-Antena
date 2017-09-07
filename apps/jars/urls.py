from django.conf.urls import url

from apps.jars import views

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', views.jars_conf, name='url_jars_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', views.jars_conf_edit, name='url_edit_jars_conf'),
    url(r'^(?P<conf_id>-?\d+)/new_filter/$', views.new_filter, name='url_new_jars_filter'),
    url(r'^(?P<conf_id>-?\d+)/change_filter/$', views.change_filter, name='url_change_jars_filter'),
    url(r'^(?P<conf_id>-?\d+)/change_filter/(?P<filter_id>-?\d+)/$', views.change_filter, name='url_change_jars_filter'),
    url(r'^(?P<conf_id>-?\d+)/view_filter/(?P<filter_id>-?\d+)/$', views.view_filter, name='url_jars_filter'),
    url(r'^(?P<conf_id>-?\d+)/view_filter/(?P<filter_id>-?\d+)/edit$', views.edit_filter, name='url_edit_jars_filter'),
    url(r'^(?P<conf_id>-?\d+)/import/$', views.import_file, name='url_import_jars_conf'),
    url(r'^(?P<conf_id>-?\d+)/read/$', views.read_conf, name='url_read_jars_conf'),
)
