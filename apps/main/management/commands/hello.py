from django.core.management.base import BaseCommand
from apps.main.models import Campaign, Location
from datetime import datetime,timedelta
from apps.main.views import radar_start
from django.shortcuts import render, redirect,get_object_or_404, HttpResponse
from django.urls import reverse
from django.utils.timezone import is_aware
from django.contrib import messages
from django.http import HttpResponseRedirect
from apps.main.views import experiment_start
from apps.main.models import Experiment, Configuration

class Command(BaseCommand):
    """
    Restart experiment every night at 05:00 am.
    Example:
        manage.py restart_experiment
    """
    def handle(self, *args, **options):
        print("")
        campaigns = Campaign.objects.filter(start_date__lte=datetime.now(),
                                        end_date__gte=datetime.now()).order_by('-start_date')

        if campaigns:

            for campaign in campaigns:
                print(campaign.name)
                print(campaign.start_date)
                print(campaign.end_date)
                print(campaign.experiments.all()[0].id)
                print("STATUS: ",campaign.experiments.all()[0].status)

                radar=campaign.get_experiments_by_radar(radar=None)
                radar_id=radar[0]["id"]
                print(radar_id)

                now = datetime.now()
                if now<campaign.end_date and now >campaign.start_date:
                    print("La campaña",campaign.name ,"se ejecuta!",flush=True)
                    radar_start_scheduler(campaign.id,radar_id)

        else:
            copy_campaigns=Campaign.objects.all()
            print("-------------Deteniendo procesos-------------")
            for campaign in copy_campaigns:
                print(campaign.name)
                print(campaign.start_date)
                print(campaign.end_date)
                print("ID: ",campaign.experiments.all()[0].id)
                print("STATUS: ",campaign.experiments.all()[0].status)
                print("----,,,---")
                radar=campaign.get_experiments_by_radar(radar=None)
                radar_id=radar[0]["id"]

                if campaign.experiments.all()[0].status !=1:
                    print("Estoy en :",campaign.experiments.all()[0].status)
                    print("Con ID: ",campaign.experiments.all()[0].id)
                    print("\n\n")
                    a=radar_stop_scheduler(campaign.id,radar_id,campaign.experiments.all()[0].id)
                    print("RETURN", a)


def radar_start_scheduler(id_camp,id_radar):
    print("-------------------")
    campaign    = get_object_or_404(Campaign, pk=id_camp)
    experiments = campaign.get_experiments_by_radar(id_radar)[0]['experiments']
    now         = datetime.now()
    
    for exp in experiments:
        exp = get_object_or_404(Experiment, pk=exp.id)

        if exp.status == 2:
            print('Experiment {} already runnnig'.format(exp))
        else:
            exp.status = exp.start()
            if exp.status == 0:
                print('Experiment {} not start'.format(exp))
            if exp.status == 2:
                print('Experiment {} started'.format(exp))
            exp.save()

def radar_stop_scheduler(id_camp,id_radar,id_experiment):
    print("-------------------")
    '''
    Stop experiments's devices
    DDS-JARS-RC-CGS-ABS
    '''
    exp=get_object_or_404(Experiment,pk=id_experiment)

    if exp.status == 2:
        confs = Configuration.objects.filter(experiment=id_experiment,type = 0).order_by('device__device_type__sequence')
        confs = confs.exclude(device__device_type__name='cgs')
        try:
            for conf in confs:
                print("Estoy en conf_scheduler")
                print(conf)
                conf.stop_device()
                exp.status= 1
        except:
            exp.status= 0
        exp.save()

    return exp.status