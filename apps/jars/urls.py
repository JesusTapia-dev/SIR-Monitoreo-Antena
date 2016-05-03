from django.conf.urls import url

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', 'apps.jars.views.jars_conf', name='url_jars_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', 'apps.jars.views.jars_conf_edit', name='url_edit_jars_conf'),
)
