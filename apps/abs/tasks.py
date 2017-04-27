from __future__ import absolute_import

from apps.main.models import Configuration
from .models import ABSBeam
import json
from datetime import timedelta, datetime
from celery.task import task

@task(name='task_change_beam')
def task_change_beam(id_conf):

    abs_conf = Configuration.objects.get(pk=id_conf)
    beams_list = ABSBeam.objects.filter(abs_conf=abs_conf)
    active_beam = json.loads(abs_conf.active_beam)

    run_every = timedelta(seconds=abs_conf.operation_value)
    now = datetime.utcnow()
    date = now + run_every

    if abs_conf.device.status != 3:
        return abs_conf.device.status

    if abs_conf.operation_mode == 0:  #Manual Mode
        return 1

    if active_beam:
        current_beam = ABSBeam.objects.get(pk=active_beam['active_beam'])
        i=0
        for beam in beams_list:
            if beam == current_beam:
                i+=1
                break
            i+=1

        if i < len(beams_list):
            next_beam = beams_list[i]
            abs_conf.send_beam_num(i+1)
            next_beam.set_as_activebeam()
            task = task_change_beam.apply_async((abs_conf.pk,), eta=date)
            print next_beam
        else:
            abs_conf.send_beam_num(1)
            beams_list[0].set_as_activebeam()
            task = task_change_beam.apply_async((abs_conf.pk,), eta=date)
            print beams_list[0]
            i=0

    else:
        abs_conf.send_beam_num(1)
        beams_list[0].set_as_activebeam()
        task = task_change_beam.apply_async((abs_conf.pk,), eta=date)


    return 2


@task(name='status_absdevice')
def status_absdevice(id_conf):

    abs_conf = Configuration.objects.get(pk=id_conf)
    abs_conf.absmodule_status()

    return
