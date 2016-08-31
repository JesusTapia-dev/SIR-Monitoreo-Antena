from django.contrib import admin
from .models import ABSConfiguration, ABSBeam

# Register your models here.

admin.site.register(ABSConfiguration)
admin.site.register(ABSBeam)
