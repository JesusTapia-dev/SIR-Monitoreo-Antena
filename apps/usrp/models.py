from django.db import models
from apps.main.models import Configuration
# Create your models here.

class USRPConfiguration(Configuration):


    class Meta:
        db_table = 'usrp_configurations'
