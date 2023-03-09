from django.contrib import admin
from .models import ATRADConfiguration, ATRADData

# Register your models here.

admin.site.register(ATRADConfiguration)
admin.site.register(ATRADData)