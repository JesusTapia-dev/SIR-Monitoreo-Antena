from django.db import models
from apps.main.models import Configuration
# Create your models here.

class ABSConfiguration(Configuration):
    

    class Meta:
        db_table = 'abs_configurations'
    