from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from datetime import datetime
import urllib

from .forms import CampaignForm, ExperimentForm, DeviceForm, ConfigurationForm, LocationForm, UploadFileForm, DownloadFileForm, OperationForm, NewForm
from .forms import OperationSearchForm, FilterForm
from apps.cgs.forms import CGSConfigurationForm
from apps.jars.forms import JARSConfigurationForm
from apps.usrp.forms import USRPConfigurationForm
from apps.abs.forms import ABSConfigurationForm
from apps.rc.forms import RCConfigurationForm, RCMixConfigurationForm
from apps.dds.forms import DDSConfigurationForm

from .models import Campaign, Experiment, Device, Configuration, Location, RunningExperiment
from apps.cgs.models import CGSConfiguration
from apps.jars.models import JARSConfiguration, EXPERIMENT_TYPE
from apps.usrp.models import USRPConfiguration
from apps.abs.models import ABSConfiguration
from apps.rc.models import RCConfiguration, RCLine, RCLineType
from apps.dds.models import DDSConfiguration
from django.http.request import QueryDict
#from __builtin__ import False

# Create your views here.

CONF_FORMS = {
    'rc': RCConfigurationForm,
    'dds': DDSConfigurationForm,
    'jars': JARSConfigurationForm,
    'cgs': CGSConfigurationForm,
    'abs': ABSConfigurationForm,
    'usrp': USRPConfigurationForm,
}

CONF_MODELS = {
    'rc': RCConfiguration,
    'dds': DDSConfiguration,
    'jars': JARSConfiguration,
    'cgs': CGSConfiguration,
    'abs': ABSConfiguration,
    'usrp': USRPConfiguration,
}

MIX_MODES = {
    '0': 'P',
    '1': 'S',
}

MIX_OPERATIONS = {
    '0': 'OR',
    '1': 'XOR',
    '2': 'AND',
    '3': 'NAND',
}


def index(request):
    kwargs = {}
    
    return render(request, 'index.html', kwargs)


def locations(request):
    
    page = request.GET.get('page')
    order = ('name',)
        
    kwargs = get_paginator(Location, page, order)      
    
    kwargs['keys'] = ['name', 'description']
    kwargs['title'] = 'Radar System'
    kwargs['suptitle'] = 'List'
    
    return render(request, 'base_list.html', kwargs)


def location(request, id_loc):
    
    location = get_object_or_404(Location, pk=id_loc)
    
    kwargs = {}
    kwargs['location'] = location
    kwargs['location_keys'] = ['name', 'description']
    
    kwargs['title'] = 'Location'
    kwargs['suptitle'] = 'Details'
    
    return render(request, 'location.html', kwargs)


def location_new(request):
    
    if request.method == 'GET':
        form = LocationForm()
        
    if request.method == 'POST':
        form = LocationForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('url_locations')
        
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Radar System'
    kwargs['suptitle'] = 'New'
    kwargs['button'] = 'Create'
        
    return render(request, 'base_edit.html', kwargs)


def location_edit(request, id_loc):
    
    location = get_object_or_404(Location, pk=id_loc)
    
    if request.method=='GET':
        form = LocationForm(instance=location)
         
    if request.method=='POST':
        form = LocationForm(request.POST, instance=location)
        
        if form.is_valid():
            form.save()
            return redirect('url_locations')
          
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Location'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Update'
    
    return render(request, 'base_edit.html', kwargs)


def location_delete(request, id_loc):
    
    location = get_object_or_404(Location, pk=id_loc)
    
    if request.method=='POST':
        
        if request.user.is_staff:
            location.delete()
            return redirect('url_locations')
        
        messages.error(request, 'Not enough permission to delete this object')
        return redirect(location.get_absolute_url())
    
    kwargs = {
              'title': 'Delete',
              'suptitle': 'Location',
              'object': location, 
              'previous': location.get_absolute_url(),
              'delete': True
              }
    
    return render(request, 'confirm.html', kwargs)


def devices(request):
    
    page = request.GET.get('page')
    order = ('device_type', 'name')
        
    kwargs = get_paginator(Device, page, order)        
    kwargs['keys'] = ['name', 'ip_address', 'port_address', 'device_type'] 
    kwargs['title'] = 'Device'
    kwargs['suptitle'] = 'List'
    
    return render(request, 'base_list.html', kwargs)


def device(request, id_dev):
    
    device = get_object_or_404(Device, pk=id_dev)
    
    kwargs = {}
    kwargs['device'] = device
    kwargs['device_keys'] = ['device_type', 'name', 'ip_address', 'port_address', 'description']
    
    kwargs['title'] = 'Device'
    kwargs['suptitle'] = 'Details'
    
    return render(request, 'device.html', kwargs)


def device_new(request):
    
    if request.method == 'GET':
        form = DeviceForm()
        
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('url_devices')
        
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Device'
    kwargs['suptitle'] = 'New'
    kwargs['button'] = 'Create'
        
    return render(request, 'base_edit.html', kwargs)


def device_edit(request, id_dev):
    
    device = get_object_or_404(Device, pk=id_dev)
    
    if request.method=='GET':
        form = DeviceForm(instance=device)
         
    if request.method=='POST':
        form = DeviceForm(request.POST, instance=device)
        
        if form.is_valid():
            form.save()
            return redirect(device.get_absolute_url())
          
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Device'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Update'
    
    return render(request, 'base_edit.html', kwargs)


def device_delete(request, id_dev):
    
    device = get_object_or_404(Device, pk=id_dev)
    
    if request.method=='POST':
        
        if request.user.is_staff:
            device.delete()
            return redirect('url_devices')
        
        messages.error(request, 'Not enough permission to delete this object')
        return redirect(device.get_absolute_url())
    
    kwargs = {
              'title': 'Delete',
              'suptitle': 'Device',
              'object': device, 
              'previous': device.get_absolute_url(),
              'delete': True
              }
    
    return render(request, 'confirm.html', kwargs)

    
def campaigns(request):
    
    page = request.GET.get('page')
    order = ('start_date',)
    filters = request.GET.copy()

    kwargs = get_paginator(Campaign, page, order, filters)
    
    form = FilterForm(initial=request.GET, extra_fields=['range_date', 'tags','template'])
    kwargs['keys'] = ['name', 'start_date', 'end_date']    
    kwargs['title'] = 'Campaign'
    kwargs['suptitle'] = 'List'
    kwargs['form'] = form    
    filters.pop('page', None)
    kwargs['q'] = urllib.urlencode(filters)
    
    return render(request, 'base_list.html', kwargs)


def campaign(request, id_camp):
    
    campaign = get_object_or_404(Campaign, pk=id_camp)
    experiments = Experiment.objects.filter(campaign=campaign)
    
    form = CampaignForm(instance=campaign)
    
    kwargs = {}
    kwargs['campaign'] = campaign
    kwargs['campaign_keys'] = ['template', 'name', 'start_date', 'end_date', 'tags', 'description']
    
    kwargs['experiments'] = experiments
    kwargs['experiment_keys'] = ['name', 'radar_system', 'start_time', 'end_time']
    
    kwargs['title'] = 'Campaign'
    kwargs['suptitle'] = 'Details'
    
    kwargs['form'] = form
    kwargs['button'] = 'Add Experiment'
    
    return render(request, 'campaign.html', kwargs)


def campaign_new(request):
    
    kwargs = {}
    
    if request.method == 'GET':
                    
        if 'template' in request.GET:
            if request.GET['template']=='0':
                form = NewForm(initial={'create_from':2},
                               template_choices=Campaign.objects.filter(template=True).values_list('id', 'name'))
            else:
                kwargs['button'] = 'Create'
                kwargs['experiments'] = Configuration.objects.filter(experiment=request.GET['template'])                
                kwargs['experiment_keys'] = ['name', 'start_time', 'end_time']
                camp = Campaign.objects.get(pk=request.GET['template'])
                form = CampaignForm(instance=camp,
                                    initial={'name':'{} [{:%Y/%m/%d}]'.format(camp.name, datetime.now()),
                                             'template':False})                
        elif 'blank' in request.GET:
            kwargs['button'] = 'Create'
            form = CampaignForm()
        else:
            form = NewForm()
        
    if request.method == 'POST':
        kwargs['button'] = 'Create'
        post = request.POST.copy()
        experiments = []
        
        for id_exp in post.getlist('experiments'):
            exp = Experiment.objects.get(pk=id_exp)
            new_exp = exp.clone(template=False)
            experiments.append(new_exp)
        
        post.setlist('experiments', [])
        
        form = CampaignForm(post)
        
        if form.is_valid():
            campaign = form.save()
            for exp in experiments:
                campaign.experiments.add(exp)
            campaign.save()
            return redirect('url_campaign', id_camp=campaign.id)
        
    kwargs['form'] = form
    kwargs['title'] = 'Campaign'
    kwargs['suptitle'] = 'New'
        
    return render(request, 'campaign_edit.html', kwargs)


def campaign_edit(request, id_camp):
    
    campaign = get_object_or_404(Campaign, pk=id_camp)
    
    if request.method=='GET':
        form = CampaignForm(instance=campaign)
         
    if request.method=='POST':
        exps = campaign.experiments.all().values_list('pk', flat=True)
        post = request.POST.copy()
        new_exps = post.getlist('experiments')
        post.setlist('experiments', [])
        form = CampaignForm(post, instance=campaign)
        
        if form.is_valid():
            camp = form.save()
            for id_exp in new_exps:
                if int(id_exp) in exps:
                    exps.pop(id_exp)
                else:
                    exp = Experiment.objects.get(pk=id_exp)
                    if exp.template:
                        camp.experiments.add(exp.clone(template=False))
                    else:
                        camp.experiments.add(exp)
            
            for id_exp in exps:
                camp.experiments.remove(Experiment.objects.get(pk=id_exp))
            
            return redirect('url_campaign', id_camp=id_camp)
          
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Campaign'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Update'
    
    return render(request, 'campaign_edit.html', kwargs)


def campaign_delete(request, id_camp):
     
    campaign = get_object_or_404(Campaign, pk=id_camp)
    
    if request.method=='POST':
        if request.user.is_staff:
            
            for exp in campaign.experiments.all():
                for conf in Configuration.objects.filter(experiment=exp):
                    conf.delete()
                exp.delete()
            campaign.delete()
            
            return redirect('url_campaigns')
        
        messages.error(request, 'Not enough permission to delete this object')
        return redirect(campaign.get_absolute_url())
    
    kwargs = {
              'title': 'Delete',
              'suptitle': 'Campaign',
              'object': campaign, 
              'previous': campaign.get_absolute_url(),
              'delete': True
              }
    
    return render(request, 'confirm.html', kwargs)

def campaign_export(request, id_camp):
    
    campaign = get_object_or_404(Campaign, pk=id_camp)
    content = campaign.parms_to_dict()            
    content_type = 'application/json'
    filename     =  '%s_%s.json' %(campaign.name, campaign.id)
    
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="%s"' %filename
    response.write(content)
    
    return response


def campaign_import(request, id_camp):
    
    campaign = get_object_or_404(Campaign, pk=id_camp)
    
    if request.method == 'GET':
        file_form = UploadFileForm()
        
    if request.method == 'POST':
        file_form = UploadFileForm(request.POST, request.FILES)
        
        if file_form.is_valid():
            
            parms = campaign.import_from_file(request.FILES['file'])
            
            if parms:
                parms['name'] = parms['campaign']
                
                new_camp = campaign.dict_to_parms(parms, CONF_MODELS)
            
                messages.success(request, "Parameters imported from: '%s'." %request.FILES['file'].name)
                
                return redirect(new_camp.get_absolute_url_edit())
        
        messages.error(request, "Could not import parameters from file")
    
    kwargs = {}
    kwargs['title'] = 'Campaign'
    kwargs['form'] = file_form
    kwargs['suptitle'] = 'Importing file'
    kwargs['button'] = 'Import'
    
    return render(request, 'campaign_import.html', kwargs)


def experiments(request):
    
    page = request.GET.get('page')
    order = ('location',)
    filters = request.GET.copy()

    kwargs = get_paginator(Experiment, page, order, filters)
    
    form = FilterForm(initial=request.GET, extra_fields=['tags','template']) 
    
    kwargs['keys'] = ['name', 'radar_system', 'start_time', 'end_time']    
    kwargs['title'] = 'Experiment'
    kwargs['suptitle'] = 'List'
    kwargs['form'] = form
    filters.pop('page', None)
    kwargs['q'] = urllib.urlencode(filters)
    
    return render(request, 'base_list.html', kwargs)


def experiment(request, id_exp):
    
    experiment = get_object_or_404(Experiment, pk=id_exp)
    
    configurations = Configuration.objects.filter(experiment=experiment, type=0)
    
    kwargs = {}
    
    kwargs['experiment_keys'] = ['template', 'radar_system', 'name', 'start_time', 'end_time']
    kwargs['experiment'] = experiment
    
    kwargs['configuration_keys'] = ['name', 'device__ip_address', 'device__port_address', 'device__status']
    kwargs['configurations'] = configurations
    
    kwargs['title'] = 'Experiment'
    kwargs['suptitle'] = 'Details'
    
    kwargs['button'] = 'Add Configuration'
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(experiment=experiment))
    
    return render(request, 'experiment.html', kwargs)


def experiment_new(request, id_camp=None):
    
    kwargs = {}
    
    if request.method == 'GET':
        if 'template' in request.GET:
            if request.GET['template']=='0':
                form = NewForm(initial={'create_from':2},
                               template_choices=Experiment.objects.filter(template=True).values_list('id', 'name'))
            else:
                kwargs['button'] = 'Create'
                kwargs['configurations'] = Configuration.objects.filter(experiment=request.GET['template'])                
                kwargs['configuration_keys'] = ['name', 'device__name', 'device__ip_address', 'device__port_address']
                exp=Experiment.objects.get(pk=request.GET['template'])
                form = ExperimentForm(instance=exp, 
                                      initial={'name': '{} [{:%Y/%m/%d}]'.format(exp.name, datetime.now()),
                                               'template': False})                
        elif 'blank' in request.GET:
            kwargs['button'] = 'Create'
            form = ExperimentForm()
        else:
            form = NewForm()
        
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        print form.data      
        if form.is_valid():
            experiment = form.save()

            if 'template' in request.GET:
                configurations = Configuration.objects.filter(experiment=request.GET['template'], type=0)            
                for conf in configurations:
                    conf.clone(experiment=experiment, template=False)
            
            return redirect('url_experiment', id_exp=experiment.id)
            
    kwargs['form'] = form
    kwargs['title'] = 'Experiment'
    kwargs['suptitle'] = 'New'
    
    return render(request, 'experiment_edit.html', kwargs)


def experiment_edit(request, id_exp):
    
    experiment = get_object_or_404(Experiment, pk=id_exp)
    
    if request.method == 'GET':
        form = ExperimentForm(instance=experiment)
        
    if request.method=='POST':
        form = ExperimentForm(request.POST, instance=experiment)
        
        if form.is_valid():
            experiment = form.save()
            return redirect('url_experiment', id_exp=experiment.id)
            
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Experiment'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Update'
        
    return render(request, 'experiment_edit.html', kwargs)


def experiment_delete(request, id_exp):
     
    experiment = get_object_or_404(Experiment, pk=id_exp)
    
    if request.method=='POST':
        if request.user.is_staff:
            for conf in Configuration.objects.filter(experiment=experiment):
                conf.delete()                
            experiment.delete()
            return redirect('url_experiments')
        
        messages.error(request, 'Not enough permission to delete this object')
        return redirect(experiment.get_absolute_url())    
    
    kwargs = {
              'title': 'Delete',
              'suptitle': 'Experiment',
              'object': experiment, 
              'previous': experiment.get_absolute_url(),
              'delete': True
              }
    
    return render(request, 'confirm.html', kwargs)


def experiment_export(request, id_exp):
    
    experiment = get_object_or_404(Experiment, pk=id_exp)
    content = experiment.parms_to_dict()            
    content_type = 'application/json'
    filename     =  '%s_%s.json' %(experiment.name, experiment.id)
    
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="%s"' %filename
    response.write(content)
    
    return response

def experiment_import(request, id_exp):
    
    experiment     = get_object_or_404(Experiment, pk=id_exp)
    configurations = Configuration.objects.filter(experiment=experiment)
    
    if request.method == 'GET':
        file_form = UploadFileForm()
        
    if request.method == 'POST':
        file_form = UploadFileForm(request.POST, request.FILES)
        
        if file_form.is_valid():
            
            parms = experiment.import_from_file(request.FILES['file'])
            
            if parms:
                
                new_exp = experiment.dict_to_parms(parms, CONF_MODELS)
            
                messages.success(request, "Parameters imported from: '%s'." %request.FILES['file'].name)
                
                return redirect(new_exp.get_absolute_url_edit()) 

        messages.error(request, "Could not import parameters from file")
    
    kwargs = {}
    kwargs['title'] = 'Experiment'
    kwargs['form'] = file_form
    kwargs['suptitle'] = 'Importing file'
    kwargs['button'] = 'Import'
    
    kwargs.update(sidebar(experiment=experiment))
    
    return render(request, 'experiment_import.html', kwargs)

def experiment_mix(request, id_exp):
    
    experiment = get_object_or_404(Experiment, pk=id_exp)
    rc_confs = [conf for conf in RCConfiguration.objects.filter(experiment=id_exp,
                                                                mix=False)]
    
    if len(rc_confs)<2:
        messages.warning(request, 'You need at least two RC Configurations to make a mix')
        return redirect(experiment.get_absolute_url())
    
    mix_confs = RCConfiguration.objects.filter(experiment=id_exp, mix=True)
    
    if mix_confs:
        mix = mix_confs[0]
    else:
        mix = RCConfiguration(experiment=experiment,
                              device=rc_confs[0].device,
                              ipp=rc_confs[0].ipp,
                              clock_in=rc_confs[0].clock_in,
                              clock_divider=rc_confs[0].clock_divider,
                              mix=True, 
                              parameters='')
        mix.save()

        line_type = RCLineType.objects.get(name='mix')
        for i in range(len(rc_confs[0].get_lines())):
            line = RCLine(rc_configuration=mix, line_type=line_type, channel=i)
            line.save()
    
    initial = {'name': mix.name,
               'result': parse_mix_result(mix.parameters),
               'delay': 0,
               'mask': [0,1,2,3,4,5,6,7]
               }
    
    if request.method=='GET':     
        form = RCMixConfigurationForm(confs=rc_confs, initial=initial)
    
    if request.method=='POST':
        result = mix.parameters

        if '{}|'.format(request.POST['experiment']) in result:
            messages.error(request, 'Configuration already added')
        else:
            if 'operation' in request.POST:
                operation = MIX_OPERATIONS[request.POST['operation']]
            else:
                operation = '   '
            
            mode = MIX_MODES[request.POST['mode']]
            
            if result:
                result = '{}-{}|{}|{}|{}|{}'.format(mix.parameters,
                                            request.POST['experiment'],
                                            mode,
                                            operation,
                                            float(request.POST['delay']),
                                            parse_mask(request.POST.getlist('mask'))
                                            )
            else:
                result = '{}|{}|{}|{}|{}'.format(request.POST['experiment'],
                                        mode,
                                        operation,
                                        float(request.POST['delay']),
                                        parse_mask(request.POST.getlist('mask'))
                                        )
            
            mix.parameters = result
            mix.name = request.POST['name']
            mix.save()
            mix.update_pulses()
                    
        initial['result'] = parse_mix_result(result)
        initial['name'] = mix.name
        
        form = RCMixConfigurationForm(initial=initial, confs=rc_confs)
            
    
    kwargs = {
              'title': 'Experiment',
              'suptitle': 'Mix Configurations',
              'form' : form,
              'extra_button': 'Delete',
              'button': 'Add',
              'cancel': 'Back',
              'previous': experiment.get_absolute_url(),
              'id_exp':id_exp,

              }
    
    return render(request, 'experiment_mix.html', kwargs)


def experiment_mix_delete(request, id_exp):
    
    conf = RCConfiguration.objects.get(experiment=id_exp, mix=True)
    values = conf.parameters.split('-')
    conf.parameters = '-'.join(values[:-1])
    conf.save()
    
    return redirect('url_mix_experiment', id_exp=id_exp)


def experiment_summary(request, id_exp):
    
    import json
    import ast
    
    experiment      = get_object_or_404(Experiment, pk=id_exp)
    experiment_data = json.loads(experiment.parms_to_dict())
    configurations  = Configuration.objects.filter(experiment=experiment, type=0)
    
    kwargs = {}
    
    kwargs['experiment_keys'] = ['template', 'radar_system', 'name', 'start_time', 'end_time']
    kwargs['experiment'] = experiment
    
    kwargs['configuration_keys'] = ['name', 'device__ip_address', 'device__port_address', 'device__status']
    kwargs['configurations'] = configurations
    kwargs['experiment_data'] = experiment_data
    
    kwargs['title'] = 'Experiment Summary'
    kwargs['suptitle'] = 'Details'
    
    kwargs['button'] = 'Verify Parameters'
    
    jars_conf = False
    rc_conf   = False
    
    for configuration in configurations:
        #-------------------- JARS -----------------------:
        if configuration.device.device_type.name == 'jars':
            jars_conf = True
            kwargs['jars_conf'] = jars_conf
            kwargs['exp_type']  = EXPERIMENT_TYPE[configuration.exp_type][1]
            channels_number     = configuration.channels_number
            exp_type            = configuration.exp_type
            fftpoints           = configuration.fftpoints
            filter_parms        = configuration.filter_parms
            filter_parms        = ast.literal_eval(filter_parms)
            spectral_number     = configuration.spectral_number
            
        #--------------------- RC ----------------------:
        if configuration.device.device_type.name == 'rc':
            rc_conf = True
            kwargs['rc_conf'] = rc_conf
            rc_lines = experiment_data['configurations']['rc']['lines']
            ipp = configuration.ipp
            if experiment_data['configurations']['rc']['mix'] == 'True':
                tx = ''
                code = ''
                window = ''
            else:
                code = rc_lines[3]['code']
                
                window_data = rc_lines[6]['params'][0]
                h0  = str(window_data['first_height'])
                dh  = str(window_data['resolution'])
                nsa = str(window_data['number_of_samples'])
                window = 'Ho='+h0+'km\nDH='+dh+'km\nNSA='+nsa
                
                tx = ''
                if float(rc_lines[1]['delays']) == 0:
                    tx = rc_lines[2]['pulse_width']
                elif float(rc_lines[2]['delays']) == 0:
                    tx = rc_lines[1]['pulse_width']
                else:
                    tx = rc_lines[1]['pulse_width']+' | '+rc_lines[2]['pulse_width']
            
            kwargs['tx']   = tx
            kwargs['code'] = code
            kwargs['window'] = window
            
        #-------------------- DDS -----------------------:
        if configuration.device.device_type.name == 'dds':
            dds_conf = True
            kwargs['dds_conf'] = dds_conf
        
        #------ RC & JARS ------:
        ipp = 937.5 #
        nsa = 200#
        dh = 1.5             #
        channels_number = 5 #
        
        if rc_conf and jars_conf:
            if exp_type  == 0: #Short
                bytes    = 2
                b        = nsa*2*bytes*channels_number
            else:              #Float
                bytes    = 4
                channels = channels_number + spectral_number
                b        = nsa*2*bytes*fftpoints*channels
               
            ipps           = (ipp*pow(10,-6))/0.15
            GB             = 1048576.0*1024.0
            Hour           = 3600
            rate           = b/ipps
            rate           = rate *(1/GB)*(Hour)
            kwargs['rate'] = str(rate)+" GB/h"
        else:
            kwargs['rate'] = ''
            
    ###### SIDEBAR ######
    kwargs.update(sidebar(experiment=experiment))
    
    return render(request, 'experiment_summary.html', kwargs)

def experiment_verify(request, id_exp):
    
    import json    
    import ast
    
    experiment      = get_object_or_404(Experiment, pk=id_exp)
    experiment_data = json.loads(experiment.parms_to_dict())
    configurations  = Configuration.objects.filter(experiment=experiment, type=0)
    
    kwargs = {}
    
    kwargs['experiment_keys'] = ['template', 'radar_system', 'name', 'start_time', 'end_time']
    kwargs['experiment'] = experiment
    
    kwargs['configuration_keys'] = ['name', 'device__ip_address', 'device__port_address', 'device__status']
    kwargs['configurations'] = configurations
    kwargs['experiment_data'] = experiment_data
    
    kwargs['title'] = 'Verify Experiment'
    kwargs['suptitle'] = 'Parameters'
    
    kwargs['button'] = 'Update'
    
    jars_conf = False
    rc_conf   = False
    dds_conf   = False
    
    for configuration in configurations:
        #-------------------- JARS -----------------------:
        if configuration.device.device_type.name == 'jars':
            jars_conf = True
            kwargs['jars_conf']    = jars_conf
            filter_parms           = configuration.filter_parms
            filter_parms           = ast.literal_eval(filter_parms)
            kwargs['filter_parms'] = filter_parms
            #--Sampling Frequency
            clock          = filter_parms['clock']
            filter_2       = filter_parms['filter_2']
            filter_5       = filter_parms['filter_5']
            filter_fir     = filter_parms['filter_fir']
            samp_freq_jars = clock/filter_2/filter_5/filter_fir
            
            kwargs['samp_freq_jars'] = samp_freq_jars
            kwargs['jars']           = configuration
        
        #--------------------- RC ----------------------:
        if configuration.device.device_type.name == 'rc':
            rc_conf = True
            rc_parms = configuration.parms_to_dict()
            if rc_parms['mix'] == 'True':
                pass
            else:            
                rc_lines     = rc_parms['lines']
                dh           = rc_lines[6]['params'][0]['resolution']
                #--Sampling Frequency
                samp_freq_rc = 0.15/dh 
                kwargs['samp_freq_rc'] = samp_freq_rc
            
            kwargs['rc_conf'] = rc_conf
            kwargs['rc']      = configuration
        
        #-------------------- DDS ----------------------:
        if configuration.device.device_type.name == 'dds':
            dds_conf = True
            dds_parms = configuration.parms_to_dict()
            
            kwargs['dds_conf'] = dds_conf
            kwargs['dds']      = configuration
    
    
    #------------Validation------------:
    #Clock
    if dds_conf and rc_conf and jars_conf:
        if filter_parms['clock'] != rc_parms['clock_in'] and rc_parms['clock_in'] != dds_parms['clock']:
            messages.warning(request, "Devices don't have the same clock.")
    elif rc_conf and jars_conf:
        if filter_parms['clock'] != rc_parms['clock_in']:
            messages.warning(request, "Devices don't have the same clock.")
    elif rc_conf and dds_conf:
        if rc_parms['clock_in'] != dds_parms['clock']:
            messages.warning(request, "Devices don't have the same clock.")
        if float(samp_freq_rc) != float(dds_parms['frequencyA']):
            messages.warning(request, "Devices don't have the same Frequency A.")
                
    
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(experiment=experiment))
    
    
    
    
    
    return render(request, 'experiment_verify.html', kwargs)


def parse_mix_result(s):
    
    values = s.split('-')
    html = 'EXP                MOD OPE DELAY         MASK\r\n'    
    
    if not values or values[0] in ('', ' '):
        return mark_safe(html)
    
    for i, value in enumerate(values):
        if not value:
            continue
        pk, mode, operation, delay, mask = value.split('|')
        conf = RCConfiguration.objects.get(pk=pk)
        if i==0:
            html += '{:20.18}{:3}{:4}{:9}km{:>6}\r\n'.format( 
                                conf.name,
                                mode,
                                '   ',
                                delay,
                                mask)
        else:
            html += '{:20.18}{:3}{:4}{:9}km{:>6}\r\n'.format(
                                conf.name,
                                mode,
                                operation,
                                delay,
                                mask)
    
    return mark_safe(html)

def parse_mask(l):
    
    values = []
    
    for x in range(8):
        if '{}'.format(x) in l:
            values.append(1)
        else:
            values.append(0)
    
    values.reverse()
    
    return int(''.join([str(x) for x in values]), 2)
    

def dev_confs(request):
    
    
    page = request.GET.get('page')
    order = ('type', 'device__device_type', 'experiment')
    filters = request.GET.copy()

    kwargs = get_paginator(Configuration, page, order, filters)
    
    form = FilterForm(initial=request.GET, extra_fields=['tags','template'])
    kwargs['keys'] = ['name', 'experiment', 'type', 'programmed_date']        
    kwargs['title'] = 'Configuration'
    kwargs['suptitle'] = 'List'
    kwargs['form'] = form    
    filters.pop('page', None)
    kwargs['q'] = urllib.urlencode(filters)
    
    return render(request, 'base_list.html', kwargs)


def dev_conf(request, id_conf):
    
    conf = get_object_or_404(Configuration, pk=id_conf)
    
    return redirect(conf.get_absolute_url())
    

def dev_conf_new(request, id_exp=0, id_dev=0):
    
    initial = {}
    kwargs = {}
    
    if id_exp<>0:
        initial['experiment'] = id_exp
    
    if id_dev<>0:
        initial['device'] = id_dev

    if request.method == 'GET':
        
        if id_dev:
            kwargs['button'] = 'Create'
            device = Device.objects.get(pk=id_dev)
            DevConfForm = CONF_FORMS[device.device_type.name]
            initial['name'] = request.GET['name']                                          
            form = DevConfForm(initial=initial)            
        else:
            if 'template' in request.GET:
                if request.GET['template']=='0':
                    choices = [(conf.pk, '{}'.format(conf)) for conf in Configuration.objects.filter(template=True)]
                    form = NewForm(initial={'create_from':2},
                                   template_choices=choices)
                else:
                    kwargs['button'] = 'Create'                    
                    conf = Configuration.objects.get(pk=request.GET['template'])
                    id_dev = conf.device.pk
                    DevConfForm = CONF_FORMS[conf.device.device_type.name]
                    form = DevConfForm(instance=conf, 
                                       initial={'name': '{} [{:%Y/%m/%d}]'.format(conf.name, datetime.now()),
                                                'template': False,
                                                'experiment':id_exp})                
            elif 'blank' in request.GET:
                kwargs['button'] = 'Create'                    
                form = ConfigurationForm(initial=initial)
            else:
                form = NewForm()                                                               
        
    if request.method == 'POST':
        
        device = Device.objects.get(pk=request.POST['device'])
        DevConfForm = CONF_FORMS[device.device_type.name]
                                        
        form = DevConfForm(request.POST)
        kwargs['button'] = 'Create'
        if form.is_valid():
            conf = form.save()
    
            if 'template' in request.GET and conf.device.device_type.name=='rc':
                lines = RCLine.objects.filter(rc_configuration=request.GET['template'])
                for line in lines:
                    line.clone(rc_configuration=conf)
                    
            if conf.device.device_type.name=='jars':       
                conf.add_parms_to_filter()
    
            return redirect('url_dev_conf', id_conf=conf.pk)                
    
    kwargs['id_exp'] = id_exp
    kwargs['form'] = form
    kwargs['title'] = 'Configuration'
    kwargs['suptitle'] = 'New'
    
    
    if id_dev != 0:
        device = Device.objects.get(pk=id_dev)
        kwargs['device'] = device.device_type.name
    
    return render(request, 'dev_conf_edit.html', kwargs)


def dev_conf_edit(request, id_conf):
    
    conf = get_object_or_404(Configuration, pk=id_conf)
    
    DevConfModel = CONF_MODELS[conf.device.device_type.name]
    DevConfForm = CONF_FORMS[conf.device.device_type.name]
    
    dev_conf = DevConfModel.objects.get(pk=id_conf)
    
    if request.method=='GET':
        form = DevConfForm(instance=dev_conf)
        
    if request.method=='POST':
        form = DevConfForm(request.POST, instance=dev_conf)
        
        if form.is_valid():
            form.save()
            return redirect('url_dev_conf', id_conf=id_conf)
          
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Update'
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf=conf))
    
    return render(request, '%s_conf_edit.html' % conf.device.device_type.name, kwargs)


def dev_conf_start(request, id_conf):
    
    conf = get_object_or_404(Configuration, pk=id_conf)
    
    DevConfModel = CONF_MODELS[conf.device.device_type.name]
    
    conf = DevConfModel.objects.get(pk=id_conf)
    
    if conf.start_device():
        messages.success(request, conf.message)
    else:
        messages.error(request, conf.message)
    
    conf.status_device()
    
    return redirect(conf.get_absolute_url())


def dev_conf_stop(request, id_conf):
    
    conf = get_object_or_404(Configuration, pk=id_conf)
    
    DevConfModel = CONF_MODELS[conf.device.device_type.name]
    
    conf = DevConfModel.objects.get(pk=id_conf)
    
    if conf.stop_device():
        messages.success(request, conf.message)
    else:
        messages.error(request, conf.message)
    
    conf.status_device()
    
    return redirect(conf.get_absolute_url())


def dev_conf_status(request, id_conf):
    
    conf = get_object_or_404(Configuration, pk=id_conf)
    
    DevConfModel = CONF_MODELS[conf.device.device_type.name]
    
    conf = DevConfModel.objects.get(pk=id_conf)
    
    if conf.status_device():
        messages.success(request, conf.message)
    else:
        messages.error(request, conf.message)
    
    return redirect(conf.get_absolute_url())


def dev_conf_write(request, id_conf):
    
    conf = get_object_or_404(Configuration, pk=id_conf)
    
    DevConfModel = CONF_MODELS[conf.device.device_type.name]
    
    conf = DevConfModel.objects.get(pk=id_conf)
    
    answer = conf.write_device()
    conf.status_device()
    
    if answer:
        messages.success(request, conf.message)
        
        #Creating a historical configuration        
        conf.clone(type=1, template=False)
        
        #Original configuration
        conf = DevConfModel.objects.get(pk=id_conf)
    else:
        messages.error(request, conf.message)
    
    return redirect(conf.get_absolute_url())


def dev_conf_read(request, id_conf):
    
    conf = get_object_or_404(Configuration, pk=id_conf)
    
    DevConfModel = CONF_MODELS[conf.device.device_type.name]
    DevConfForm = CONF_FORMS[conf.device.device_type.name]
    
    conf = DevConfModel.objects.get(pk=id_conf)
    
    if request.method=='GET':
        
        parms = conf.read_device()
        conf.status_device()
        
        if not parms:
            messages.error(request, conf.message)
            return redirect(conf.get_absolute_url())
        
        form = DevConfForm(initial=parms, instance=conf)
    
    if request.method=='POST':
        form = DevConfForm(request.POST, instance=conf)
        
        if form.is_valid():
            form.save()
            return redirect(conf.get_absolute_url())
        
        messages.error(request, "Parameters could not be saved")
        
    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Parameters read from device'
    kwargs['button'] = 'Save'
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf=conf))
    
    return render(request, '%s_conf_edit.html' %conf.device.device_type.name, kwargs)


def dev_conf_import(request, id_conf):
    
    conf = get_object_or_404(Configuration, pk=id_conf)
    
    DevConfModel = CONF_MODELS[conf.device.device_type.name]
    DevConfForm = CONF_FORMS[conf.device.device_type.name]    
    conf = DevConfModel.objects.get(pk=id_conf)
    
    if request.method == 'GET':
        file_form = UploadFileForm()
        
    if request.method == 'POST':
        file_form = UploadFileForm(request.POST, request.FILES)
        
        if file_form.is_valid():
            
            parms = conf.import_from_file(request.FILES['file'])
        
            if parms:
                messages.success(request, "Parameters imported from: '%s'." %request.FILES['file'].name)
                form = DevConfForm(initial=parms, instance=conf)
                
                kwargs = {}
                kwargs['id_dev'] = conf.id
                kwargs['form'] = form
                kwargs['title'] = 'Device Configuration'
                kwargs['suptitle'] = 'Parameters imported'
                kwargs['button'] = 'Save'
                kwargs['action'] = conf.get_absolute_url_edit()
                kwargs['previous'] = conf.get_absolute_url()
                
                ###### SIDEBAR ######
                kwargs.update(sidebar(conf=conf))
                
                return render(request, '%s_conf_edit.html' % conf.device.device_type.name, kwargs)

        messages.error(request, "Could not import parameters from file")
    
    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['title'] = 'Device Configuration'
    kwargs['form'] = file_form
    kwargs['suptitle'] = 'Importing file'
    kwargs['button'] = 'Import'
    
    kwargs.update(sidebar(conf=conf))
    
    return render(request, 'dev_conf_import.html', kwargs)


def dev_conf_export(request, id_conf):
    
    conf = get_object_or_404(Configuration, pk=id_conf)
    
    DevConfModel = CONF_MODELS[conf.device.device_type.name]
    
    conf = DevConfModel.objects.get(pk=id_conf)
    
    if request.method == 'GET':
        file_form = DownloadFileForm(conf.device.device_type.name)
        
    if request.method == 'POST':
        file_form = DownloadFileForm(conf.device.device_type.name, request.POST)
    
        if file_form.is_valid():
            fields = conf.export_to_file(format = file_form.cleaned_data['format'])
            
            response = HttpResponse(content_type=fields['content_type'])
            response['Content-Disposition'] = 'attachment; filename="%s"' %fields['filename']
            response.write(fields['content'])
        
            return response
        
        messages.error(request, "Could not export parameters")
    
    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['title'] = 'Device Configuration'
    kwargs['form'] = file_form
    kwargs['suptitle'] = 'Exporting file'
    kwargs['button'] = 'Export'
    
    return render(request, 'dev_conf_export.html', kwargs)


def dev_conf_delete(request, id_conf):
     
    conf = get_object_or_404(Configuration, pk=id_conf)
    
    if request.method=='POST':
        if request.user.is_staff:
            conf.delete()
            return redirect('url_dev_confs')
        
        messages.error(request, 'Not enough permission to delete this object')
        return redirect(conf.get_absolute_url())    
    
    kwargs = {
              'title': 'Delete',
              'suptitle': 'Experiment',
              'object': conf, 
              'previous': conf.get_absolute_url(),
              'delete': True
              }
    
    return render(request, 'confirm.html', kwargs)


def sidebar(**kwargs):
    
    side_data = {}
    
    conf = kwargs.get('conf', None)
    experiment = kwargs.get('experiment', None)
    
    if not experiment:
        experiment = conf.experiment
    
    if experiment:
        side_data['experiment'] = experiment
        campaign = experiment.campaign_set.all()
        if campaign:
            side_data['campaign'] = campaign[0]
            experiments = campaign[0].experiments.all()
        else:
            experiments = [experiment]
        configurations = experiment.configuration_set.filter(type=0)
        side_data['side_experiments'] = experiments
        side_data['side_configurations'] = configurations
    
    return side_data

def get_paginator(model, page, order, filters={}, n=10):
    
    kwargs = {}
    query = Q()
    if isinstance(filters, QueryDict):
        filters = filters.dict()
    [filters.pop(key) for key in filters.keys() if filters[key] in ('', ' ')]
    filters.pop('page', None)
    
    if 'start_date' in filters:
        filters['start_date__gte'] = filters.pop('start_date')
    if 'end_date' in filters:
        filters['start_date__lte'] = filters.pop('end_date')
    if 'tags' in filters:
        tags = filters.pop('tags')        
        if 'tags' in model._meta.get_all_field_names():
            query = query | Q(tags__icontains=tags)  
        if 'name' in model._meta.get_all_field_names():
            query = query | Q(name__icontains=tags)  
        if 'location' in model._meta.get_all_field_names():
            query = query | Q(location__name__icontains=tags)
        if 'device' in model._meta.get_all_field_names():
            query = query | Q(device__name__icontains=tags) 

    object_list = model.objects.filter(query, **filters).order_by(*order)
    paginator = Paginator(object_list, n)
    
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    
    kwargs['objects'] = objects
    kwargs['offset'] = (int(page)-1)*n if page else 0
    
    return kwargs

def operation(request, id_camp=None):
    
    if not id_camp:
        campaigns = Campaign.objects.all().order_by('-start_date')
        
        if not campaigns:
            kwargs = {}
            kwargs['title'] = 'No Campaigns'
            kwargs['suptitle'] = 'Empty'
            return render(request, 'operation.html', kwargs)
        
        id_camp = campaigns[0].id
    
    campaign = get_object_or_404(Campaign, pk = id_camp)
    
    if request.method=='GET':
        form = OperationForm(initial={'campaign': campaign.id}, length = 5)
        
    if request.method=='POST':
        form = OperationForm(request.POST, initial={'campaign':campaign.id}, length = 5)
        
        if form.is_valid():
            return redirect('url_operation', id_camp=campaign.id)
    #locations = Location.objects.filter(experiment__campaign__pk = campaign.id).distinct()
    experiments = Experiment.objects.filter(campaign__pk=campaign.id)
    #for exs in experiments:
    #    exs.get_status()
    locations= Location.objects.filter(experiment=experiments).distinct()
    #experiments = [Experiment.objects.filter(location__pk=location.id).filter(campaign__pk=campaign.id) for location in locations]
    kwargs = {}
    #---Campaign
    kwargs['campaign'] = campaign
    kwargs['campaign_keys'] = ['name', 'start_date', 'end_date', 'tags', 'description']
    #---Experiment
    keys = ['id', 'name', 'start_time', 'end_time', 'status']
    kwargs['experiment_keys'] = keys[1:]
    kwargs['experiments'] = experiments
    #---Radar
    kwargs['locations'] = locations
    #---Else
    kwargs['title'] = 'Campaign'
    kwargs['suptitle'] = campaign.name
    kwargs['form'] = form
    kwargs['button'] = 'Search'
    kwargs['details'] = True
    kwargs['search_button'] = True
    
    return render(request, 'operation.html', kwargs)


def operation_search(request, id_camp=None):
    
    
    if not id_camp:
        campaigns = Campaign.objects.all().order_by('-start_date')
        
        if not campaigns:
            return render(request, 'operation.html', {})
        
        id_camp = campaigns[0].id
    campaign = get_object_or_404(Campaign, pk = id_camp)
    
    if request.method=='GET':
        form = OperationSearchForm(initial={'campaign': campaign.id})
        
    if request.method=='POST':
        form = OperationSearchForm(request.POST, initial={'campaign':campaign.id})
        
        if form.is_valid():
            return redirect('url_operation', id_camp=campaign.id)
        
    #locations = Location.objects.filter(experiment__campaign__pk = campaign.id).distinct()
    experiments = Experiment.objects.filter(campaign__pk=campaign.id)
    #for exs in experiments:
    #    exs.get_status()
    locations= Location.objects.filter(experiment=experiments).distinct()
    form = OperationSearchForm(initial={'campaign': campaign.id})
        
    kwargs = {}
    #---Campaign
    kwargs['campaign'] = campaign
    kwargs['campaign_keys'] = ['name', 'start_date', 'end_date', 'tags', 'description']
    #---Experiment
    keys = ['id', 'name', 'start_time', 'end_time', 'status']
    kwargs['experiment_keys'] = keys[1:]
    kwargs['experiments'] = experiments
    #---Radar
    kwargs['locations'] = locations
    #---Else
    kwargs['title'] = 'Campaign'
    kwargs['suptitle'] = campaign.name
    kwargs['form'] = form
    kwargs['button'] = 'Select'
    kwargs['details'] = True
    kwargs['search_button'] = False
     
    return render(request, 'operation.html', kwargs)


def radar_play(request, id_camp, id_radar):
    campaign = get_object_or_404(Campaign, pk = id_camp)
    radar = get_object_or_404(Location, pk = id_radar)
    today = datetime.today()
    now = today.time()
    
    #--Clear Old Experiments From RunningExperiment Object
    running_experiment = RunningExperiment.objects.filter(radar=radar)
    if running_experiment:
        running_experiment = running_experiment[0]
        running_experiment.running_experiment.clear()
        running_experiment.save()
    
    #--If campaign datetime is ok:
    if today >= campaign.start_date and today <= campaign.end_date:
        experiments = Experiment.objects.filter(campaign=campaign).filter(location=radar)
        for exp in experiments:
            #--If experiment time is ok:
            if now >= exp.start_time and now <= exp.end_time:
                configurations =  Configuration.objects.filter(experiment = exp)
                for conf in configurations:
                    if 'cgs' in conf.device.device_type.name:
                        conf.status_device()
                    else:
                        answer = conf.start_device()
                        conf.status_device()
                        #--Running Experiment
                        old_running_experiment = RunningExperiment.objects.filter(radar=radar)
                        #--If RunningExperiment element exists
                        if old_running_experiment:
                            old_running_experiment = old_running_experiment[0]
                            old_running_experiment.running_experiment.add(exp)
                            old_running_experiment.status = 3
                            old_running_experiment.save()
                        #--Create a new Running_Experiment Object
                        else:
                            new_running_experiment = RunningExperiment(
                                                                   radar = radar,
                                                                   status = 3,
                                                                   )
                            new_running_experiment.save()
                            new_running_experiment.running_experiment.add(exp)
                            new_running_experiment.save()
                        
                        if answer:
                            messages.success(request, conf.message)
                            exp.status=2
                            exp.save()
                        else:
                            messages.error(request, conf.message)
            else:
                if exp.status == 1 or exp.status == 3:
                    exp.status=3
                    exp.save()
   
    
    route = request.META['HTTP_REFERER']
    route = str(route)
    if 'search' in route:
        return HttpResponseRedirect(reverse('url_operation_search', args=[id_camp]))
    else:
        return HttpResponseRedirect(reverse('url_operation', args=[id_camp]))


def radar_stop(request, id_camp, id_radar):
    campaign = get_object_or_404(Campaign, pk = id_camp)
    radar = get_object_or_404(Location, pk = id_radar)
    experiments = Experiment.objects.filter(campaign=campaign).filter(location=radar)
    
    for exp in experiments:
        configurations =  Configuration.objects.filter(experiment = exp)
        for conf in configurations:
            if 'cgs' in conf.device.device_type.name:
                conf.status_device()
            else:
                answer = conf.stop_device()
                conf.status_device()
                
                if answer:
                    messages.success(request, conf.message)
                    exp.status=1
                    exp.save()
                else:
                    messages.error(request, conf.message)
        

    route = request.META['HTTP_REFERER']
    route = str(route)
    if 'search' in route:
        return HttpResponseRedirect(reverse('url_operation_search', args=[id_camp]))
    else:
        return HttpResponseRedirect(reverse('url_operation', args=[id_camp]))
    

def radar_refresh(request, id_camp, id_radar):
    
    campaign = get_object_or_404(Campaign, pk = id_camp)
    radar = get_object_or_404(Location, pk = id_radar)
    experiments = Experiment.objects.filter(campaign=campaign).filter(location=radar)
    for exs in experiments:
        exs.get_status()

    route = request.META['HTTP_REFERER']
    route = str(route)
    if 'search' in route:
        return HttpResponseRedirect(reverse('url_operation_search', args=[id_camp]))
    else:
        return HttpResponseRedirect(reverse('url_operation', args=[id_camp]))
