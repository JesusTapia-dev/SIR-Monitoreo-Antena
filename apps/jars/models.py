from django.db import models
from apps.main.models import Configuration
# Create your models here.

class JARSConfiguration(Configuration):
    

    class Meta:
        db_table = 'jars_configurations'
    