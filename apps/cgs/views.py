from django.shortcuts import redirect, render, get_object_or_404

from apps.main.models import Experiment, Configuration
from .models import CGSConfiguration
from .forms import CGSConfigurationForm
# Create your views here.

def cgs_conf(request, id_conf):
    
    conf = get_object_or_404(CGSConfiguration, pk=id_conf)
    
    kwargs = {}
    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = ['experiment', 'device',
                               'freq0', 'freq1',
                               'freq2', 'freq3']
    
    kwargs['title'] = 'CGS Configuration'
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
    
    return render(request, 'cgs_conf.html', kwargs)

def cgs_conf_edit(request, id_conf):
    
    conf = get_object_or_404(CGSConfiguration, pk=id_conf)
    
    if request.method=='GET':
        form = CGSConfigurationForm(instance=conf)
        
    if request.method=='POST':
        form = CGSConfigurationForm(request.POST, instance=conf)
        
        if form.is_valid():
            form.save()
            return redirect('url_cgs_conf', id_conf=id_conf)
          
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Update'
    
    return render(request, 'cgs_conf_edit.html', kwargs)