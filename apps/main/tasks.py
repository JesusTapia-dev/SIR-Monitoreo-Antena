from __future__ import absolute_import

from celery import task
from datetime import timedelta, datetime

from .models import Experiment

@task
def task_start(id_exp):

    exp = Experiment.objects.get(pk=id_exp)

    return exp.start()

@task
def task_stop(id_exp):

    exp = Experiment.objects.get(pk=id_exp)

    return exp.stop()


#Task to get status
@task
def task_status(id_exp):

    exp = Experiment.objects.get(pk=id_exp)
    if exp.status==2:
        run_every = timedelta(minutes=1)
        now = datetime.utcnow()
        date = now + run_every
        task_status.apply_async((id_exp,), eta=date)
        print "Monitoring..."
        exp.get_status()
        return exp.status

    else:
        return exp.status
