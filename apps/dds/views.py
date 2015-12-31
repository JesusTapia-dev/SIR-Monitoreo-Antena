# Create your views here.

from django.shortcuts import redirect, render

from apps.main.models import Experiment, Configuration
from .models import DDSConfiguration
from .forms import DDSConfigurationForm
# Create your views here.

def dds_conf(request, id_conf):

    conf = DDSConfiguration.objects.get(pk=id_conf)
    
    kwargs = {}
    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = ['experiment', 'device',
                               'clock', 'multiplier',
                               'freq_reg', 'phase_reg',
                               'amplitude_chA', 'amplitude_chB',
                               'modulation',
                               'freq_reg_mod', 'phase_reg_mod']
    
    kwargs['title'] = 'DDS Configuration'
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
    
    return render(request, 'dds_conf.html', kwargs)
    
def edit_dds_conf(request, id_conf):
    
    conf = DDSConfiguration.objects.get(pk=id_conf)
    
    if request.method=='GET':
        form = DDSConfigurationForm(instance=conf)
        
    if request.method=='POST':
        form = DDSConfigurationForm(request.POST, instance=conf)
        
        if form.is_valid():
            form.save()
            return redirect('url_dds_conf', id_conf=id_conf)
          
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Update'
    
    return render(request, 'dds_conf_edit.html', kwargs)