from django.conf.urls import patterns, url

urlpatterns = patterns('apps.main.views',
    url(r'^$', 'index', name="index"),
)
