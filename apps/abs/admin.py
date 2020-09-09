from django.contrib import admin
from .models import ABSConfiguration, ABSBeam, ABSActive

# Register your models here.

admin.site.register(ABSConfiguration)
admin.site.register(ABSBeam)
admin.site.register(ABSActive)