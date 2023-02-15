from django.urls import include, path
from django.contrib import admin
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/',admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.main.urls')),
    path('rc/', include('apps.rc.urls')),
    path('dds/', include('apps.dds.urls')),
    path('cgs/', include('apps.cgs.urls')),
    path('jars/',include('apps.jars.urls')),
    path('usrp/', include('apps.usrp.urls')),
    path('abs/', include('apps.abs.urls')),
    path('misc/',include('apps.misc.urls')),
    path('dds_rest/', include('apps.dds_rest.urls')),
    path('atrad/', include('apps.atrad.urls')),
]

#urlpatterns += staticfiles_urlpatterns()
