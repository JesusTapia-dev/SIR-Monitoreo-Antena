from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from .forms import NewExperimentForm, NewDeviceForm, DeviceTypeForm

from .models import Experiment, Device, Configuration
from apps.cgs.models import CGSConfiguration
from apps.jars.models import JARSConfiguration
#from apps.usrp.models import USRPConfiguration
from apps.abs.models import ABSConfiguration
from apps.rc.models import RCConfiguration
from apps.dds.models import DDSConfiguration

# Create your views here.

MODELS = {
    'rc': RCConfiguration,
    'dds': DDSConfiguration,
    'jars': JARSConfiguration,
    'cgs': CGSConfiguration,
    'abs': ABSConfiguration,
}

def index(request):
    kwargs = {}
    
    return render_to_response("index.html", kwargs, context_instance=RequestContext(request))

def experiment(request, id_exp=0, id_dev_type=0):
    kwargs = {}
    if id_exp:
        experiment = Experiment.objects.get(pk=id_exp)
        devices = Device.objects.filter(configuration__experiment=experiment)
        kwargs['experiment'] = experiment
        kwargs['experiment_keys'] = ['name', 'alias', 'start_date', 'end_date']
        
        form = NewExperimentForm(instance=experiment)
        
        if id_dev_type:
            subform = DeviceTypeForm(initial={'device_type':id_dev_type})            
            kwargs['keys'] = ['model', 'ip_address', 'status']
            keys = ['id']+kwargs['keys']
            kwargs['items'] = Device.objects.filter(device_type=id_dev_type).values(*keys)
        else:
            subform = DeviceTypeForm()
        
        kwargs['form'] = form
        kwargs['subform'] = subform
        kwargs['device_keys'] = ['device_type__name', 'model', 'ip_address', 'status']
        kwargs['devices'] = devices.values('device_type__name', 'model', 'ip_address', 'status', 'device_type__alias', 'configuration__id')
        kwargs['suptitle'] = 'Detail'
    else:
        experiments = Experiment.objects.all().order_by('start_date')        
        kwargs['keys'] = ['name', 'start_date', 'end_date']
        keys = ['id']+kwargs['keys']
        kwargs['items'] = experiments.values(*keys)        
        kwargs['suptitle'] = 'List'
        kwargs['button'] = 'Add Experiment'
    
    kwargs['id_dev_type'] = id_dev_type
    kwargs['id_exp'] = id_exp
    return render_to_response("experiment.html", kwargs, context_instance=RequestContext(request))

def edit_experiment(request, id_exp):
    if request.method=='POST':
        experiment = Experiment.objects.get(pk=id_exp)
        form = NewExperimentForm(request.POST, instance=experiment)
        if form.is_valid():
            form.save()
    return redirect('experiment', id_exp=id_exp)

def experiment_add_device(request, id_exp):
    if request.method=='POST':
        experiment = Experiment.objects.get(pk=id_exp)
        device = Device.objects.get(pk=request.POST['device'])
        model = MODELS[device.device_type.alias]
        conf = model(experiment=experiment, device=device)
        conf.save()
    return redirect('experiment', id_exp=id_exp)

def add_experiment(request):
    kwargs = {}
    if request.method == 'POST':
        form = NewExperimentForm(request.POST)
        if form.is_valid():
            experiment = form.save()
            return redirect('experiment', id_exp=experiment.id)
    else:        
        form = NewExperimentForm()
    kwargs['form_new'] = form
    kwargs['title'] = 'Experiment'
    kwargs['suptitle'] = 'New'
    kwargs['id_exp'] = 0
    return render_to_response("experiment.html", kwargs, context_instance=RequestContext(request))

def device(request, id_dev=0):
    kwargs = {}
    if id_dev:
        device = Device.objects.get(pk=id_dev)
        kwargs['form'] = NewDeviceForm(instance=device)
        kwargs['action'] = 'edit/'
        kwargs['button'] = 'Update'
        kwargs['suptitle'] = 'Detail'
    else:
        devices = Device.objects.all()       
        kwargs['keys'] = ['device_type__name', 'model', 'serial_number', 'ip_address', 'status']
        keys = ['id']+kwargs['keys']
        kwargs['items'] = devices.values(*keys)
        kwargs['suptitle'] = 'List'
        kwargs['button'] = 'Add Device'
    return render_to_response("device.html", kwargs, context_instance=RequestContext(request))

def edit_device(request, id_dev):
    if request.method=='POST':
        device = Device.objects.get(pk=id_dev)
        form = NewDeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
    return redirect('devices')

def add_device(request):
    kwargs = {}
    if request.method == 'POST':
        form = NewDeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('devices')
    else:        
        form = NewDeviceForm()
    kwargs['form'] = form
    kwargs['button'] = 'Create'
    kwargs['suptitle'] = 'New'
    return render_to_response("device.html", kwargs, context_instance=RequestContext(request))

