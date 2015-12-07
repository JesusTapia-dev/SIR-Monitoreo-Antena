from django.db import models
from apps.main.models import Configuration
# Create your models here.

class RCConfiguration(Configuration):
    

    class Meta:
        db_table = 'rc_configurations'
    