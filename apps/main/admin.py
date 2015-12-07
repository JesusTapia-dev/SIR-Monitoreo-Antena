from django.contrib import admin
from .models import Device, DeviceType, Experiment

# Register your models here.

admin.site.register(Experiment)
admin.site.register(Device)
admin.site.register(DeviceType)