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
        print("\n\n")
        all_campaigns=Campaign.objects.all()
        campaigns = Campaign.objects.filter(start_date__lte=datetime.now(),
                                        end_date__gte=datetime.now()).order_by('-start_date')

        for campaign in all_campaigns:
            if campaign.start_date<datetime.now() and campaign.end_date > datetime.now():

                radar=campaign.get_experiments_by_radar(radar=None)
                for rad in radar:
                    # print("RADR", rad)
                    radar_id=rad["id"]
                    # print("RADR_",radar_id)
                    radar_start_scheduler(campaign.id,radar_id)
                print(campaign.name, "\t\t Campaign already running")    

            else:
                radar=campaign.get_experiments_by_radar(radar=None)
                radar_id=radar[0]["id"]
                if campaign.experiments.all()[0].status !=1:
                    print(campaign.name, "\t\t Stopping Campaign...")
                    a=radar_stop_scheduler(campaign.id,radar_id,campaign.experiments.all()[0].id)
                    print("New Status: ", a)
                else:
                    print(campaign.name,"\t\t\t Campaign already stooped")

def radar_start_scheduler(id_camp,id_radar):
    campaign    = get_object_or_404(Campaign, pk=id_camp)
    experiments = campaign.get_experiments_by_radar(id_radar)[0]['experiments']
    now         = datetime.now()
    # print(campaign)
    # print(experiments)
    for exp in experiments:
        exp = get_object_or_404(Experiment, pk=exp.id)
        # print("---------DEBUGG-------------")
        # print(exp)
        if exp.status == 2:
            print('\t\t\t {} \t\t  Experiment already runnnig'.format(exp))
        else:
            exp.status = exp.start()
            if exp.status == 0:
                print('\t\t\t {} \t\tExperiment not start'.format(exp))
            if exp.status == 2:
                print('\t\t\t {} \t\tExperiment started'.format(exp))
            if exp.status == 4:
                print('\t\t\t {} \t\tExperiment with state uknown, please reset'.format(exp))
            exp.save()

def radar_stop_scheduler(id_camp,id_radar,id_experiment):
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
                # print(conf)
                conf.stop_device()
                exp.status= 1
        except:
            exp.status= 0
        exp.save()

    return exp.status