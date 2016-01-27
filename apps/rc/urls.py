from django.conf.urls import url

urlpatterns = (
    url(r'^(?P<id>-?\d+)/$', 'apps.rc.views.conf', name='url_rc_conf'),
    url(r'^(?P<id>-?\d+)/edit/$', 'apps.rc.views.conf_edit', name='url_edit_rc_conf'),
    url(r'^(?P<conf_id>-?\d+)/add_line/$', 'apps.rc.views.add_line', name='url_add_rc_line'),
    url(r'^(?P<conf_id>-?\d+)/update_lines/$', 'apps.rc.views.update_lines', name='url_update_rc_lines'),
    url(r'^(?P<conf_id>-?\d+)/edit_lines/$', 'apps.rc.views.edit_lines', name='url_edit_rc_lines'),
    url(r'^(?P<conf_id>-?\d+)/add_line/(?P<line_type_id>-?\d+)/$', 'apps.rc.views.add_line', name='url_add_rc_line'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/delete/$', 'apps.rc.views.remove_line', name='url_remove_rc_line'),
)
