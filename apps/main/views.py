from django.shortcuts import render, redirect, HttpResponse

from .forms import CampaignForm, ExperimentForm, DeviceForm, ConfigurationForm
from apps.cgs.forms import CGSConfigurationForm
from apps.jars.forms import JARSConfigurationForm
from apps.usrp.forms import USRPConfigurationForm
from apps.abs.forms import ABSConfigurationForm
from apps.rc.forms import RCConfigurationForm
from apps.dds.forms import DDSConfigurationForm

from .models import Campaign, Experiment, Device, Configuration
from apps.cgs.models import CGSConfiguration
from apps.jars.models import JARSConfiguration
from apps.usrp.models import USRPConfiguration
from apps.abs.models import ABSConfiguration
from apps.rc.models import RCConfiguration
from apps.dds.models import DDSConfiguration

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

def index(request):
    kwargs = {}
    
    return render(request, 'index.html', kwargs)

def devices(request):
    
    devices = Device.objects.all().order_by('device_type__name')
    
    keys = ['id', 'device_type__name', 'name', 'ip_address']
    
    kwargs = {}
    kwargs['device_keys'] = keys[1:]
    kwargs['devices'] = devices.values(*keys)
    kwargs['title'] = 'Device'
    kwargs['suptitle'] = 'List'
    kwargs['button'] = 'New Device'
    
    return render(request, 'devices.html', kwargs)

def device(request, id_dev):
    
    device = Device.objects.get(pk=id_dev)
    
    kwargs = {}
    kwargs['device'] = device
    kwargs['device_keys'] = ['device_type', 'name', 'ip_address', 'port_address', 'description']
    
    kwargs['title'] = 'Device'
    kwargs['suptitle'] = 'Details'
    
    kwargs['button'] = 'Add Device'
    
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
        
    return render(request, 'device_edit.html', kwargs)

def device_edit(request, id_dev):
    
    device = Device.objects.get(pk=id_dev)
    
    if request.method=='GET':
        form = DeviceForm(instance=device)
         
    if request.method=='POST':
        form = DeviceForm(request.POST, instance=device)
        
        if form.is_valid():
            form.save()
            return redirect('url_devices')
          
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Device'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Update'
    
    return render(request, 'device_edit.html', kwargs)

def device_delete(request, id_dev):
    
    device = Device.objects.get(pk=id_dev)
    
    if request.method=='POST':
        
        if request.user.is_staff:
            device.delete()
            return redirect('url_devices')
        
        return HttpResponse("Not enough permission to delete this object")
    
    kwargs = {'object':device, 'dev_active':'active',
              'url_cancel':'url_device', 'id_item':id_dev}
    
    return render(request, 'item_delete.html', kwargs)
    
def campaigns(request):
    
    campaigns = Campaign.objects.all().order_by('start_date')
    
    keys = ['id', 'name', 'start_date', 'end_date']
    
    kwargs = {}
    kwargs['campaign_keys'] = keys[1:]
    kwargs['campaigns'] = campaigns.values(*keys)
    kwargs['title'] = 'Campaign'
    kwargs['suptitle'] = 'List'
    kwargs['button'] = 'New Campaign'
    
    return render(request, 'campaigns.html', kwargs)

def campaign(request, id_camp):
    
    campaign = Campaign.objects.get(pk=id_camp)
    experiments = Experiment.objects.filter(campaign=campaign)
    
    form = CampaignForm(instance=campaign)
    
    kwargs = {}
    kwargs['campaign'] = campaign
    kwargs['campaign_keys'] = ['name', 'start_date', 'end_date', 'tags', 'description']
    
    keys = ['id', 'name', 'start_time', 'end_time']
    
    kwargs['experiment_keys'] = keys[1:]
    kwargs['experiments'] = experiments.values(*keys)
    
    kwargs['title'] = 'Campaign'
    kwargs['suptitle'] = 'Details'
    
    kwargs['form'] = form
    kwargs['button'] = 'Add Experiment'
    
    return render(request, 'campaign.html', kwargs)

def campaign_new(request):
    
    if request.method == 'GET':
        form = CampaignForm()
        
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        
        if form.is_valid():
            campaign = form.save()
            return redirect('url_campaign', id_camp=campaign.id)
        
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Campaign'
    kwargs['suptitle'] = 'New'
    kwargs['button'] = 'Create'
        
    return render(request, 'campaign_edit.html', kwargs)

def campaign_edit(request, id_camp):
    
    campaign = Campaign.objects.get(pk=id_camp)
    
    if request.method=='GET':
        form = CampaignForm(instance=campaign)
         
    if request.method=='POST':
        form = CampaignForm(request.POST, instance=campaign)
        
        if form.is_valid():
            form.save()
            return redirect('url_campaign', id_camp=id_camp)
          
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Campaign'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Update'
    
    return render(request, 'campaign_edit.html', kwargs)

def campaign_delete(request, id_camp):
     
    campaign = Campaign.objects.get(pk=id_camp)
    
    if request.method=='POST':
        if request.user.is_staff:
            campaign.delete()
            return redirect('url_campaigns')
        
        return HttpResponse("Not enough permission to delete this object")
    
    kwargs = {'object':campaign, 'camp_active':'active',
              'url_cancel':'url_campaign', 'id_item':id_camp}
    
    return render(request, 'item_delete.html', kwargs)

def experiments(request):
    
    campaigns = Experiment.objects.all().order_by('start_time')
    
    keys = ['id', 'campaign__name', 'name', 'start_time', 'end_time']
    
    kwargs = {}
    
    kwargs['experiment_keys'] = keys[1:]
    kwargs['experiments'] = campaigns.values(*keys)
    
    kwargs['title'] = 'Experiment'
    kwargs['suptitle'] = 'List'
    kwargs['button'] = 'New Experiment'
    
    return render(request, 'experiments.html', kwargs)

def experiment(request, id_exp):
    
    experiment = Experiment.objects.get(pk=id_exp)
    
    experiments = Experiment.objects.filter(campaign=experiment.campaign)
    configurations = Configuration.objects.filter(experiment=experiment)
    
    kwargs = {}
    
    exp_keys = ['id', 'campaign', 'name', 'start_time', 'end_time']
    conf_keys = ['id', 'device__name', 'device__device_type__name', 'device__ip_address']
    
    
    kwargs['experiment_keys'] = exp_keys[1:]
    kwargs['experiment'] = experiment
    
    kwargs['experiments'] = experiments.values(*exp_keys)
    
    kwargs['configuration_keys'] = conf_keys[1:]
    kwargs['configurations'] = configurations.values(*conf_keys)
    
    kwargs['title'] = 'Experiment'
    kwargs['suptitle'] = 'Details'
    
    kwargs['button'] = 'Add Device'
    
    return render(request, 'experiment.html', kwargs)

def experiment_new(request, id_camp=0):
    
    if request.method == 'GET':
        form = ExperimentForm(initial={'campaign':id_camp})
        
    if request.method == 'POST':
        form = ExperimentForm(request.POST, initial={'campaign':id_camp})
        
        if form.is_valid():
            experiment = form.save()
            return redirect('url_experiment', id_exp=experiment.id)
        
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Experiment'
    kwargs['suptitle'] = 'New'
    kwargs['button'] = 'Create'
    
    return render(request, 'experiment_edit.html', kwargs)

def experiment_edit(request, id_exp):
    
    experiment = Experiment.objects.get(pk=id_exp)
    
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
     
    experiment = Experiment.objects.get(pk=id_exp)
    
    if request.method=='POST':
        if request.user.is_staff:
            id_camp = experiment.campaign.id
            experiment.delete()
            return redirect('url_campaign', id_camp=id_camp)
        
        return HttpResponse("Not enough permission to delete this object")
    
    kwargs = {'object':experiment, 'exp_active':'active',
              'url_cancel':'url_experiment', 'id_item':id_exp}
    
    return render(request, 'item_delete.html', kwargs)

def dev_confs(request):
    
    configurations = Configuration.objects.all().order_by('device__device_type')
    
    keys = ['id', 'device__device_type__name', 'device__name', 'experiment__campaign__name', 'experiment__name']
    
    kwargs = {}
    
    kwargs['configuration_keys'] = keys[1:]
    kwargs['configurations'] = configurations.values(*keys)
    
    kwargs['title'] = 'Configuration'
    kwargs['suptitle'] = 'List'
    kwargs['button'] = 'New Configuration'
    
    return render(request, 'dev_confs.html', kwargs)

def dev_conf(request, id_conf):
    
    conf = Configuration.objects.get(pk=id_conf)
    
    DevConfModel = CONF_MODELS[conf.device.device_type.name]
    dev_conf = DevConfModel.objects.get(pk=id_conf)
    
    kwargs = {}
    kwargs['dev_conf'] = dev_conf
    kwargs['dev_conf_keys'] = ['experiment', 'device']
    
    kwargs['title'] = 'Configuration'
    kwargs['suptitle'] = 'Details'
    
    kwargs['button'] = 'Edit Configuration'
    
    ###### SIDEBAR ######
    experiments = Experiment.objects.filter(campaign=conf.experiment.campaign)
    configurations = Configuration.objects.filter(experiment=conf.experiment)
    
    exp_keys = ['id', 'campaign', 'name', 'start_time', 'end_time']
    conf_keys = ['id', 'device__name', 'device__device_type__name', 'device__ip_address']
    
    kwargs['experiment_keys'] = exp_keys[1:]
    kwargs['experiments'] = experiments.values(*exp_keys)
    
    kwargs['configuration_keys'] = conf_keys[1:]
    kwargs['configurations'] = configurations.values(*conf_keys)
    
    return render(request, 'dev_conf.html', kwargs)

def dev_conf_new(request, id_exp=0):

    if request.method == 'GET':
        form = ConfigurationForm(initial={'experiment':id_exp})
        
    if request.method == 'POST':
        form = ConfigurationForm(request.POST)
        
        if form.is_valid():
            experiment = Experiment.objects.get(pk=request.POST['experiment'])
            device = Device.objects.get(pk=request.POST['device'])
            
            exp_devices = Device.objects.filter(configuration__experiment=experiment)
              
            if device.id not in exp_devices.values('id',):
              
                DevConfModel = CONF_MODELS[device.device_type.name]
                conf = DevConfModel(experiment=experiment, device=device)
                conf.save()
                
                return redirect('url_experiment', id_exp=experiment.id)
        
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Configuration'
    kwargs['suptitle'] = 'New'
    kwargs['button'] = 'Create'
    
    return render(request, 'dev_conf_edit.html', kwargs)
    
def dev_conf_edit(request, id_conf):
    
    conf = Configuration.objects.get(pk=id_conf)
    
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
    
    return render(request, 'dev_conf_edit.html', kwargs)

def dev_conf_delete(request, id_conf):
     
    conf = Configuration.objects.get(pk=id_conf)
    
    if request.method=='POST':
        if request.user.is_staff:
            id_exp = conf.experiment.id
            conf.delete()
            return redirect('url_experiment', id_exp=id_exp)
        
        return HttpResponse("Not enough permission to delete this object")
    
    kwargs = {'object':conf, 'conf_active':'active',
          'url_cancel':'url_dev_conf', 'id_item':id_conf}
    
    return render(request, 'item_delete.html', kwargs)