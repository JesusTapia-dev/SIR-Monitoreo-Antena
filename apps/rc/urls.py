from django.conf.urls import url

from apps.rc import views

urlpatterns = (
    url(r'^(?P<conf_id>-?\d+)/$', views.conf, name='url_rc_conf'),
    url(r'^(?P<conf_id>-?\d+)/import/$', views.import_file, name='url_import_rc_conf'),
    url(r'^(?P<conf_id>-?\d+)/edit/$', views.conf_edit, name='url_edit_rc_conf'),
    url(r'^(?P<conf_id>-?\d+)/plot/$', views.plot_pulses, name='url_plot_rc_pulses'),
    url(r'^(?P<conf_id>-?\d+)/plot2/$', views.plot_pulses2, name='url_plot_rc_pulses2'),
    #url(r'^(?P<id_conf>-?\d+)/write/$', 'apps.main.views.dev_conf_write', name='url_write_rc_conf'),
    #url(r'^(?P<id_conf>-?\d+)/read/$', 'apps.main.views.dev_conf_read', name='url_read_rc_conf'),
    url(r'^(?P<conf_id>-?\d+)/raw/$', views.conf_raw, name='url_raw_rc_conf'),
    url(r'^(?P<conf_id>-?\d+)/add_line/$', views.add_line, name='url_add_rc_line'),
    url(r'^(?P<conf_id>-?\d+)/add_line/(?P<line_type_id>-?\d+)/$', views.add_line, name='url_add_rc_line'),
    url(r'^(?P<conf_id>-?\d+)/add_line/(?P<line_type_id>-?\d+)/code/(?P<code_id>-?\d+)/$', views.add_line, name='url_add_rc_line_code'),
    url(r'^(?P<conf_id>-?\d+)/update_position/$', views.update_lines_position, name='url_update_rc_lines_position'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/delete/$', views.remove_line, name='url_remove_rc_line'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/add_subline/$', views.add_subline, name='url_add_rc_subline'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/codes/$', views.edit_codes, name='url_edit_rc_codes'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/codes/(?P<code_id>-?\d+)/$', views.edit_codes, name='url_edit_rc_codes'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/subline/(?P<subline_id>-?\d+)/delete/$', views.remove_subline, name='url_remove_rc_subline'),
)
