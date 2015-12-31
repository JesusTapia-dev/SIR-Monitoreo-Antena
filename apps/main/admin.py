from django.contrib import admin
from .models import Device, DeviceType, Experiment, Campaign

# Register your models here.
admin.site.register(Campaign)
admin.site.register(Experiment)
admin.site.register(Device)
admin.site.register(DeviceType)