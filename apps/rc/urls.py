from django.conf.urls import url

urlpatterns = (
    url(r'^(?P<id>-?\d+)/$', 'apps.rc.views.conf', name='url_rc_conf'),
    url(r'^(?P<id>-?\d+)/edit/$', 'apps.rc.views.conf_edit', name='url_edit_rc_conf'),
    url(r'^(?P<id>-?\d+)/add_line/$', 'apps.rc.views.add_line', name='url_add_rc_line'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/delete/$', 'apps.rc.views.remove_line', name='url_remove_rc_line'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/up/$', 'apps.rc.views.line_up', name='url_rc_line_up'),
    url(r'^(?P<conf_id>-?\d+)/line/(?P<line_id>-?\d+)/down/$', 'apps.rc.views.line_down', name='url_rc_line_down'),
)
