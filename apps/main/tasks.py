from __future__ import absolute_import

from radarsys.celery import app
from celery import Task
from datetime import timedelta, datetime

from .models import Experiment
from celery import Celery

from celery.utils.log import get_task_logger

from django.utils import timezone

logger = get_task_logger(__name__)

@Task
def task_start(id_exp):
    print("exp.id", id_exp)
    exp    = Experiment.objects.get(pk=id_exp)
    status = exp.status
    if status == 2:
        print('Experiment {} already running start task not executed'.format(exp))
        return 2
    if status == 3:
        now   = datetime.now()
        start = datetime.combine(now.date(), exp.start_time)
        end   = datetime.combine(now.date(), exp.end_time)
        print(now)
        print(start)
        print(end)
        if end < start:
            end += timedelta(1)
        try:
            print('Starting exp:{}'.format(exp))
            exp.status = exp.start()
        except:
            print('Error')
            exp.status = 0
        if exp.status == 2:
            #task = task_stop.apply_async((id_exp,),eta=end) #Antiguo eta=end+timedelta(hours=5))
            task = task_stop.apply_async((id_exp,),eta=end+timedelta(hours=5)) #Antiguo eta=end+timedelta(hours=5))
            exp.task = task.id

    #------------ new ----------------------
    if status == 4 or status == 1:
        now   = datetime.now()
        start = datetime.combine(now.date(), exp.start_time)
        end   = datetime.combine(now.date(), exp.end_time)
        print(now)
        print(start)
        print(end)
        if now >= start:
            print('Starting exp:{}'.format(exp))
            exp.status = exp.start()

    #---------------------------------------

    exp.save()
    return exp.status
    
@Task
def task_stop(id_exp):
    exp = Experiment.objects.get(pk=id_exp)
    if exp.status == 2:
        try:
            print('Stopping exp:{}'.format(exp))
            exp.status = exp.stop()
        except:
            print('Error')
            exp.status = 0

    now        = datetime.now()
    start      = datetime.combine(now.date()+timedelta(1), exp.start_time)
    task       = task_start.apply_async((id_exp, ), eta=start) #Antiguo eta=start+timedelta(hours=5))
    exp.task   = task.id
    exp.status = 3
    exp.save()
    return exp.status

#Task to get status
@Task
def task_status(id_exp):
    print ("task status"+str(id_exp))
    exp = Experiment.objects.get(pk=id_exp)
    if exp.status==2:
        run_every = timedelta(minutes=1)
        now       = datetime.utcnow()
        date      = now + run_every
        task_status.apply_async((id_exp,), eta=date)
        print ("Monitoring...")
        exp.get_status()
        return exp.status

    else:
        return exp.status


@Task
def task_test(id_exp):
    print("mm",id_exp)
    exp    = Experiment.objects.get(pk=id_exp)
    exp.status = exp.start()
    return exp.status