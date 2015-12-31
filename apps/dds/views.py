# Create your views here.

from django.shortcuts import redirect, render

from .models import DDSConfiguration
from .forms import DDSConfigurationForm
# Create your views here.

def dds_conf(request, id_conf):

    dev_conf = DDSConfiguration.objects.get(pk=id_conf)
    
    kwargs = {}
    kwargs['dev_conf'] = dev_conf
    kwargs['dev_conf_keys'] = ['experiment', 'device',
                               'clock', 'multiplier',
                               'freq_reg', 'phase_reg',
                               'amplitude_chA', 'amplitude_chB',
                               'modulation',
                               'freq_reg_mod', 'phase_reg_mod']
    
    kwargs['title'] = 'DDS Configuration'
    kwargs['suptitle'] = 'Details'
    
    kwargs['button'] = 'Edit Configuration'
    
    return render(request, 'dds_conf.html', kwargs)
    
def edit_dds_conf(request, id_conf):
    
    dev_conf = DDSConfiguration.objects.get(pk=id_conf)
    
    if request.method=='GET':
        form = DDSConfigurationForm(instance=dev_conf)
        
    if request.method=='POST':
        form = DDSConfigurationForm(request.POST, instance=dev_conf)
        
        if form.is_valid():
            form.save()
            return redirect('url_dds_conf', id_conf=id_conf)
          
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Update'
    
    return render(request, 'dds_conf_edit.html', kwargs)