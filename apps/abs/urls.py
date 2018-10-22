from django.conf.urls import url

from apps.abs import views

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', views.abs_conf, name='url_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', views.abs_conf_edit, name='url_edit_abs_conf'),
    url(r'^alert/$', views.abs_conf_alert, name='url_alert_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/import/$', views.import_file, name='url_import_abs_conf'),
    #url(r'^(?P<id_conf>-?\d+)/status/', views.abs_conf, {'status_request':True},name='url_status_abs_conf'),
    url(r'^(?P<id_conf>-?\d+)/change_beam/(?P<id_beam>-?\d+)/$', views.send_beam, name='url_send_beam'),
    url(r'^(?P<id_conf>-?\d+)/plot/$', views.plot_patterns, name='url_plot_abs_patterns'),
    url(r'^(?P<id_conf>-?\d+)/plot/(?P<id_beam>-?\d+)/$', views.plot_patterns, name='url_plot_abs_patterns'),
    url(r'^(?P<id_conf>-?\d+)/plot/(?P<id_beam>-?\d+)/(?P<antenna>[\w\-]+)/pattern.png$', views.plot_pattern, name='url_plot_beam'),
    url(r'^(?P<id_conf>-?\d+)/add_beam/$', views.add_beam, name='url_add_abs_beam'),
    url(r'^(?P<id_conf>-?\d+)/beam/(?P<id_beam>-?\d+)/delete/$', views.remove_beam, name='url_remove_abs_beam'),
    url(r'^(?P<id_conf>-?\d+)/beam/(?P<id_beam>-?\d+)/edit/$', views.edit_beam, name='url_edit_abs_beam'),
)
