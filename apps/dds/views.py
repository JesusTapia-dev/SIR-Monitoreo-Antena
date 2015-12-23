# Create your views here.

from django.shortcuts import redirect, render

from apps.main.models import Device
from .models import DDSConfiguration
from .forms import DDSConfigurationForm
# Create your views here.

def config_dds(request, id_conf):

    if id_conf:
                
        conf = DDSConfiguration.objects.get(pk=id_conf)
        form = DDSConfigurationForm(instance=conf)
        experiment = conf.experiment
        
        devices = Device.objects.filter(configuration__experiment=experiment)
        
        deviceList = devices.values('configuration__id', 'device_type__alias', 'device_type__name')
        
        for thisDevice in deviceList:
            if thisDevice['configuration__id'] == conf.id:
                thisDevice['active'] = 'active'
                break
        
        device = thisDevice
        
    else:
        form = DDSConfigurationForm()
        device = ''
        experiment = ''
        devices = {}
        
    kwargs = {
        'form': form,
        'device': device,
        'experiment': experiment,
        'devices': deviceList
    }

#     return render_to_response('conf_dds.html', kwargs, context_instance=RequestContext(request))
    return render(request, 'conf_dds.html', kwargs)
    
def config_dds_edit(request, id_conf):
    
    if request.method=='POST':
        
        conf = DDSConfiguration.objects.get(pk=id_conf)
        form = DDSConfigurationForm(instance=conf)
        
        if form.is_valid():
            form.save()
        else:
            raise ValueError, "Error"
            
    return redirect('url_conf_dds', id_conf=id_conf)