from django.conf.urls import url

urlpatterns = (
    url(r'^(?P<id>-?\d+)/$', 'apps.jars.views.jars_config', name='jars'),
)
