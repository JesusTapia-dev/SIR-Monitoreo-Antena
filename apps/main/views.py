from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages

from .forms import CampaignForm, ExperimentForm, DeviceForm, ConfigurationForm, LocationForm, UploadFileForm, DownloadFileForm, OperationForm
from .forms import OperationSearchForm
from apps.cgs.forms import CGSConfigurationForm
from apps.jars.forms import JARSConfigurationForm
from apps.usrp.forms import USRPConfigurationForm
from apps.abs.forms import ABSConfigurationForm
from apps.rc.forms import RCConfigurationForm
from apps.dds.forms import DDSConfigurationForm

from .models import Campaign, Experiment, Device, Configuration, Location#, RunningExperiment
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

def locations(request):
    
    locations = Location.objects.all().order_by('name')
    
    keys = ['id', 'name', 'description']
    
    kwargs = {}
    kwargs['location_keys'] = keys[1:]
    kwargs['locations'] = locations
    kwargs['title'] = 'Location'
    kwargs['suptitle'] = 'List'
    kwargs['button'] = 'New Location'
    
    return render(request, 'locations.html', kwargs)

def location(request, id_loc):
    
    location = get_object_or_404(Location, pk=id_loc)
    
    kwargs = {}
    kwargs['location'] = location
    kwargs['location_keys'] = ['name', 'description']
    
    kwargs['title'] = 'Location'
    kwargs['suptitle'] = 'Details'
    
    return render(request, 'location.html', kwargs)

#def location_play(request, id_camp, id_loc):
    
#    campaign = get_object_or_404(Campaign, pk=id_camp)
#    print campaign
#    location = get_object_or_404(Location, pk=id_loc)
#    experiments =  Experiment.objects.filter(location__pk=location.id).filter(campaign__pk=campaign.id)
#    locations = Location.objects.filter(pk=id_loc)
    
#    if request.method=='GET':
#        form = OperationForm(initial={'campaign': campaign.id})
    
#    kwargs = {}
    #---Campaign
#    kwargs['campaign'] = campaign
#    kwargs['campaign_keys'] = ['name', 'start_date', 'end_date', 'tags', 'description']
    #---Experiment
#    keys = ['id', 'name', 'start_time', 'end_time']
#    kwargs['experiment_keys'] = keys[1:]
#    kwargs['experiments'] = experiments
    #---Radar
#    kwargs['location'] = location
    #---Else
#    kwargs['title'] = 'Campaign'
#    kwargs['suptitle'] = campaign.name
#    kwargs['form'] = form
#    kwargs['button'] = 'Search'
    
#    return render(request, 'operation_play.html', kwargs)

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
    kwargs['title'] = 'Location'
    kwargs['suptitle'] = 'New'
    kwargs['button'] = 'Create'
        
    return render(request, 'location_edit.html', kwargs)

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
    
    return render(request, 'location_edit.html', kwargs)

def location_delete(request, id_loc):
    
    location = get_object_or_404(Location, pk=id_loc)
    
    if request.method=='POST':
        
        if request.user.is_staff:
            location.delete()
            return redirect('url_locations')
        
        return HttpResponse("Not enough permission to delete this object")
    
    kwargs = {'object':location, 'loc_active':'active',
              'url_cancel':'url_location', 'id_item':id_loc}
    
    return render(request, 'item_delete.html', kwargs)

def devices(request):
    
    devices = Device.objects.all().order_by('device_type__name')
    
#     keys = ['id', 'device_type__name', 'name', 'ip_address']
    keys = ['id', 'name', 'ip_address', 'port_address', 'device_type']
    
    kwargs = {}
    kwargs['device_keys'] = keys[1:]
    kwargs['devices'] = devices#.values(*keys)
    kwargs['title'] = 'Device'
    kwargs['suptitle'] = 'List'
    kwargs['button'] = 'New Device'
    
    return render(request, 'devices.html', kwargs)

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
        
    return render(request, 'device_edit.html', kwargs)

def device_edit(request, id_dev):
    
    device = get_object_or_404(Device, pk=id_dev)
    
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
    
    device = get_object_or_404(Device, pk=id_dev)
    
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
    kwargs['campaigns'] = campaigns#.values(*keys)
    kwargs['title'] = 'Campaign'
    kwargs['suptitle'] = 'List'
    kwargs['button'] = 'New Campaign'
    
    return render(request, 'campaigns.html', kwargs)

def campaign(request, id_camp):
    
    campaign = get_object_or_404(Campaign, pk=id_camp)
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
    
    campaign = get_object_or_404(Campaign, pk=id_camp)
    
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
     
    campaign = get_object_or_404(Campaign, pk=id_camp)
    
    if request.method=='POST':
        if request.user.is_staff:
            campaign.delete()
            return redirect('url_campaigns')
        
        return HttpResponse("Not enough permission to delete this object")
    
    kwargs = {'object':campaign, 'camp_active':'active',
              'url_cancel':'url_campaign', 'id_item':id_camp}
    
    return render(request, 'item_delete.html', kwargs)

def experiments(request):
    
    experiment_list = Experiment.objects.all().order_by('campaign')
    
    keys = ['id', 'name', 'start_time', 'end_time', 'campaign']
    
    kwargs = {}
    
    kwargs['experiment_keys'] = keys[1:]
    kwargs['experiments'] = experiment_list#.values(*keys)
    
    kwargs['title'] = 'Experiment'
    kwargs['suptitle'] = 'List'
    kwargs['button'] = 'New Experiment'
    
    return render(request, 'experiments.html', kwargs)

def experiment(request, id_exp):
    
    experiment = get_object_or_404(Experiment, pk=id_exp)
    
    experiments = Experiment.objects.filter(campaign=experiment.campaign)
    configurations = Configuration.objects.filter(experiment=experiment, type=0)
    
    kwargs = {}
    
    exp_keys = ['id', 'campaign', 'location', 'name', 'start_time', 'end_time']
    conf_keys = ['id', 'device__name', 'device__device_type', 'device__ip_address', 'device__port_address']
    
    conf_labels = ['id', 'device__name', 'device_type', 'ip_address', 'port_address']
    
    kwargs['experiment_keys'] = exp_keys[1:]
    kwargs['experiment'] = experiment
    
    kwargs['experiments'] = experiments.values(*exp_keys)
    
    kwargs['configuration_labels'] = conf_labels[1:]
    kwargs['configuration_keys'] = conf_keys[1:]
    kwargs['configurations'] = configurations #.values(*conf_keys)
    
    kwargs['title'] = 'Experiment'
    kwargs['suptitle'] = 'Details'
    
    kwargs['button'] = 'Add Configuration'
    
    return render(request, 'experiment.html', kwargs)

def experiment_new(request, id_camp=None):
    
    if request.method == 'GET':
        form = ExperimentForm(initial={'campaign':id_camp})
        
    if request.method == 'POST':
        form = ExperimentForm(request.POST, initial={'campaign':id_camp})
        
        if form.is_valid():
            experiment = form.save()
            ##AGREGAR!
            return redirect('url_experiment', id_exp=experiment.id)
        
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Experiment'
    kwargs['suptitle'] = 'New'
    kwargs['button'] = 'Create'
    
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
            id_camp = experiment.campaign.id
            experiment.delete()
            return redirect('url_campaign', id_camp=id_camp)
        
        return HttpResponse("Not enough permission to delete this object")
    
    kwargs = {'object':experiment, 'exp_active':'active',
              'url_cancel':'url_experiment', 'id_item':id_exp}
    
    return render(request, 'item_delete.html', kwargs)

def dev_confs(request):
    
    configurations = Configuration.objects.all().order_by('type', 'device__device_type', 'experiment')
    
#     keys = ['id', 'device__device_type__name', 'device__name', 'experiment__campaign__name', 'experiment__name']
    
    keys = ['id', 'device', 'experiment', 'type', 'programmed_date']

    kwargs = {}
    
    kwargs['configuration_keys'] = keys[1:]
    kwargs['configurations'] = configurations#.values(*keys)
    
    kwargs['title'] = 'Configuration'
    kwargs['suptitle'] = 'List'
    kwargs['button'] = 'New Configuration'
    
    return render(request, 'dev_confs.html', kwargs)

def dev_conf(request, id_conf):
    
    conf = get_object_or_404(Configuration, pk=id_conf)
    
    return redirect(conf.get_absolute_url())
    

def dev_conf_new(request, id_exp=0, id_dev=0):
    
    initial = {}
    
    if id_exp==0:
        initial['experiment'] = id_exp
    
    if id_dev<>0:
        initial['device'] = id_dev

    if request.method == 'GET':
        if id_dev==0:
            form = ConfigurationForm(initial=initial)
        else:
            device = Device.objects.get(pk=id_dev)
            DevConfForm = CONF_FORMS[device.device_type.name]
                                        
            form = DevConfForm(initial=initial)
        
    if request.method == 'POST':
        
        device = Device.objects.get(pk=request.POST['device'])
        DevConfForm = CONF_FORMS[device.device_type.name]
                                        
        form = DevConfForm(request.POST)
        
        if form.is_valid():
            dev_conf = form.save()
    
            return redirect('url_dev_confs')
        
    kwargs = {}
    kwargs['id_exp'] = id_exp
    kwargs['form'] = form
    kwargs['title'] = 'Configuration'
    kwargs['suptitle'] = 'New'
    kwargs['button'] = 'Create'
    
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
    kwargs.update(sidebar(conf))
    
    return render(request, '%s_conf_edit.html' %conf.device.device_type.name, kwargs)

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
        conf.pk = None
        conf.id = None
        conf.type = 1
        conf.template = 0
        conf.save()
        
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
    kwargs.update(sidebar(conf))
    
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
                print parms
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
                kwargs.update(sidebar(conf))
                
                return render(request, '%s_conf_edit.html' % conf.device.device_type.name, kwargs)

        messages.error(request, "Could not import parameters from file")
    
    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['title'] = 'Device Configuration'
    kwargs['form'] = file_form
    kwargs['suptitle'] = 'Importing file'
    kwargs['button'] = 'Import'
    
    kwargs.update(sidebar(conf))
    
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
            id_exp = conf.experiment.id
            conf.delete()
            return redirect('url_experiment', id_exp=id_exp)
        
        return HttpResponse("Not enough permission to delete this object")
    
    kwargs = {'object':conf, 'conf_active':'active',
          'url_cancel':'url_dev_conf', 'id_item':id_conf}
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf))
    
    return render(request, 'item_delete.html', kwargs)

def sidebar(conf):
    
    kwargs = {}
    
    if conf.experiment:
        experiments = Experiment.objects.filter(campaign=conf.experiment.campaign)
        configurations = Configuration.objects.filter(experiment=conf.experiment, type=0)
        exp_keys = ['id', 'campaign', 'name', 'start_time', 'end_time']
        kwargs['experiment_keys'] = exp_keys[1:]
        kwargs['experiments'] = experiments.values(*exp_keys)    
        conf_keys = ['id', 'device']            
        kwargs['configuration_keys'] = conf_keys[1:]
        kwargs['configurations'] = configurations #.values(*conf_keys)
    
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

def operation_search(request, id_camp=None, location_play = None):
    
    
    if not id_camp:
        campaigns = Campaign.objects.all().order_by('-start_date')
        form = OperationSearchForm()
        
        if not campaigns:
            return render(request, 'operation.html', {})
        
        id_camp = campaigns[0].id
        campaign = get_object_or_404(Campaign, pk = id_camp)
        
        kwargs = {}
        kwargs['title'] = 'All Campaigns'
        kwargs['form'] = form
        kwargs['details'] = True
        return render(request, 'operation.html', kwargs)
    
    else:
        campaign = get_object_or_404(Campaign, pk = id_camp)
        #locations = Location.objects.filter(experiment__campaign__pk = campaign.id).distinct()
        #experiments = Experiment.objects.filter(campaign__pk=campaign.id)
        experiments = Experiment.objects.filter(campaign__pk=campaign.id)
        locations= Location.objects.filter(experiment=experiments).distinct()
        #experiments = [Experiment.objects.filter(location__pk=location.id).filter(campaign__pk=campaign.id) for location in locations]
        form = OperationSearchForm(initial={'campaign': campaign.id})
        
        kwargs = {}
        #---Campaign
        kwargs['campaign'] = campaign
        kwargs['campaign_keys'] = ['name', 'start_date', 'end_date', 'tags', 'description']
        #---Experiment
        keys = ['id', 'name', 'start_time', 'end_time']
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
        
        
    if request.method=='POST':
        form = OperationSearchForm(request.POST, initial={'campaign':campaign.id})
        
        if form.is_valid():
            return redirect('operation.html', id_camp=campaign.id)
        
    
    return render(request, 'operation.html', kwargs)