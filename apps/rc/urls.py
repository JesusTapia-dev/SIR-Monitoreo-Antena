from django.conf.urls import url

urlpatterns = (
    url(r'^(?P<conf_id>-?\d+)/$', 'apps.rc.views.conf', name='url_rc_conf'),
    url(r'^(?P<conf_id>-?\d+)/import/$', 'apps.rc.views.import_file', name='url_import_rc_conf'),
    url(r'^(?P<conf_id>-?\d+)/edit/$', 'apps.rc.views.conf_edit', name='url_edit_rc_conf'),
    url(r'^(?P<conf_id>-?\d+)/plot/$', 'apps.rc.views.view_pulses', name='url_plot_rc_pulses'),
    url(r'^(?P<id_conf>-?\d+)/write/$', 'apps.main.views.dev_conf_write', name='url_write_rc_conf'),
    url(r'^(?P<id_conf>-?\d+)/read/$', 'apps.main.views.dev_conf_read', name='url_read_rc_conf'),
    
    url(r'^(?P<conf_id>-?\d+)/add_line/$', 'apps.rc.views.add_line', name='url_add_rc_line'),
    url(r'^(?P<conf_id>-?\d+)/add_line/(?P<line_type_id>-?\d+)/$', 'apps.rc.views.add_line', name='url_add_rc_line'),
    url(r'^(?P<conf_id>-?\d+)/add_line/(?P<line_type_id>-?\d+)/code/(?P<code_id>-?\d+)/$', 'apps.rc.views.add_line', name='url_add_rc_line_code'),
    url(r'^(?P<conf_id>-?\d+)/update_position/$', 'apps.rc.views.update_lines_position', name='url_update_rc_lines_position'),    
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/delete/$', 'apps.rc.views.remove_line', name='url_remove_rc_line'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/add_subline/$', 'apps.rc.views.add_subline', name='url_add_rc_subline'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/codes/$', 'apps.rc.views.edit_codes', name='url_edit_rc_codes'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/codes/(?P<code_id>-?\d+)/$', 'apps.rc.views.edit_codes', name='url_edit_rc_codes'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/subline/(?P<subline_id>-?\d+)/delete/$', 'apps.rc.views.remove_subline', name='url_remove_rc_subline'),
)
