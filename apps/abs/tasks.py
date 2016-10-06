from __future__ import absolute_import
from celery import task
from .models import Experiment

#@task
#def task_start(id_exp):

#    exp = Experiment.objects.get(pk=id_exp)

#    return exp.start()



#@task
#def task_stop(id_exp):

#    exp = Experiment.objects.get(pk=id_exp)

#    return exp.stop()
