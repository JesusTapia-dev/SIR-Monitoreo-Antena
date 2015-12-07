from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.main.models import Device
from .models import JARSConfiguration
from .forms import JARSConfigurationForm
# Create your views here.

def jars_config(request, id):

    if id:
        conf = JARSConfiguration.objects.get(pk=id)
        devices = Device.objects.filter(configuration__experiment=conf.experiment)
        devices = devices.values('configuration__id', 'device_type__alias', 'device_type__name')
        for device in devices:
            if device['device_type__alias']=='jars':
                device['active'] = 'active'
        form = JARSConfigurationForm(instance=conf)
    else:
        form = JARSConfigurationForm()

    kwargs = {
        'form': form,
        'devices':devices,
    }

    return render_to_response('jars.html', kwargs, context_instance=RequestContext(request))
    



