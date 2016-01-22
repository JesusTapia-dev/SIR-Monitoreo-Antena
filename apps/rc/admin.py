from django.contrib import admin
from .models import RCConfiguration, RCLine, RCLineType

# Register your models here.

admin.site.register(RCConfiguration)
admin.site.register(RCLine)
admin.site.register(RCLineType)
