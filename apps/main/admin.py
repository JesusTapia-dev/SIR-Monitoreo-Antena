from django.contrib import admin
from .models import Device, DeviceType, Experiment, Campaign, Location, RunningExperiment

# Register your models here.
admin.site.register(Campaign)
admin.site.register(Experiment)
admin.site.register(Device)
admin.site.register(DeviceType)
admin.site.register(Location)
admin.site.register(RunningExperiment)