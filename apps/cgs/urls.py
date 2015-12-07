from django.conf.urls import url

urlpatterns = (
    #url(r'^configuration/$', 'apps.cgs.views.configurate_frequencies', name='new_device'),
    url(r'^(?P<id>-?\d+)/$', 'apps.cgs.views.configurate_frequencies', name='new_device'),
)

