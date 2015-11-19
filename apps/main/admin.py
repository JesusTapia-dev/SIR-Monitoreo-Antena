from django.contrib import admin
from .models import Device, DeviceType, Experiment, ExperimentDetail, ExperimentTemplate, Configuration

# Register your models here.

admin.site.register(Experiment)
admin.site.register(ExperimentDetail)
admin.site.register(ExperimentTemplate)
admin.site.register(Device)
admin.site.register(Configuration)
admin.site.register(DeviceType)