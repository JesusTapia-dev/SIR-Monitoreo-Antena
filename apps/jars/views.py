from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404

from apps.main.models import Device
from apps.main.views import sidebar

from .models import JARSConfiguration
from .forms import JARSConfigurationForm
# Create your views here.

def jars_conf(request, id_conf):
    
    conf = get_object_or_404(JARSConfiguration, pk=id_conf)
    
    ip=conf.device.ip_address
    port=conf.device.port_address
    
    kwargs = {}
    
    kwargs['status'] = conf.device.get_status_display()
    
    
    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = ['experiment', 'device',
                               'cards_number', 'channels_number',
                               'rd_directory', 'create_directory',
                               'include_expname', 'raw_data_blocks',
                               'acq_profiles', 'profiles_block', 'filter']
    
    kwargs['title'] = 'JARS Configuration'
    kwargs['suptitle'] = 'Details'
    
    kwargs['button'] = 'Edit Configuration'
    
    kwargs['no_play'] = True
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf=conf))
    
    return render(request, 'jars_conf.html', kwargs)

def jars_conf_edit(request, id_conf):
    
    conf = get_object_or_404(JARSConfiguration, pk=id_conf)
    
    if request.method=='GET':
        form = JARSConfigurationForm(instance=conf)
        
    if request.method=='POST':
        form = JARSConfigurationForm(request.POST, instance=conf)
        
        if form.is_valid():
            conf = form.save(commit=False)
            conf.save()
            return redirect('url_jars_conf', id_conf=conf.id)
            
            ##ERRORS
        
    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Save'
    
    return render(request, 'jars_conf_edit.html', kwargs)