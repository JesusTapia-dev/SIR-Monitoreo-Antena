from django.contrib import admin
from .models import JARSConfiguration, JARSfilter

# Register your models here.

admin.site.register(JARSConfiguration)
admin.site.register(JARSfilter)
