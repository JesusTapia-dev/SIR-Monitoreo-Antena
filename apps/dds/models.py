from django.db import models
from apps.main.models import Configuration
# Create your models here.

class DDSConfiguration(Configuration):
    

    class Meta:
        db_table = 'dds_configurations'
    