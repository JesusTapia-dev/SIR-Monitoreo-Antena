from django.conf.urls import url

urlpatterns = (
    url(r'^(?P<id_conf>-?\d+)/$', 'apps.main.views.dev_conf', name='url_usrp_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', 'apps.main.views.edit_dev_conf', name='url_edit_usrp_conf'),
)
