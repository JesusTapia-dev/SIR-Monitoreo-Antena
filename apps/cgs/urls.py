from django.conf.urls import url

urlpatterns = (
    #url(r'^configuration/$', 'apps.cgs.views.configurate_frequencies', name='new_device'),
#     url(r'^(?P<id>-?\d+)/$', 'apps.cgs.views.configurate_frequencies', name='new_device'),
    url(r'^(?P<id_conf>-?\d+)/$', 'apps.main.views.dev_conf', name='url_cgs_conf'),
    url(r'^(?P<id_conf>-?\d+)/edit/$', 'apps.main.views.dev_conf_edit', name='url_edit_cgs_conf'),
)

