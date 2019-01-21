from django.contrib import admin
from .models import JARSConfiguration, JARSFilter

# Register your models here.

admin.site.register(JARSConfiguration)
admin.site.register(JARSFilter)
