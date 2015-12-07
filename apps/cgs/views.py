from django.shortcuts import render, render_to_response
from django.template import RequestContext

from .forms import CGSConfigurationForm
from .models import CGSConfiguration
from apps.main.models import Device
# Create your views here.

def configurate_frequencies(request, id=0):
    kwargs = {}
    if id:
        conf = CGSConfiguration.objects.get(pk=id)
        devices = Device.objects.filter(configuration__experiment=conf.experiment)
        devices = devices.values('configuration__id', 'device_type__alias', 'device_type__name')
        for device in devices:
            if device['device_type__alias']=='cgs':
                device['active'] = 'active'
        form = CGSConfigurationForm(instance=conf)
    else:
        form = CGSConfigurationForm()

    data = {
        'form': form,
        'devices':devices,
        'title': ('YAP'),
    }

    return render_to_response('index_cgs.html', data, context_instance=RequestContext(request))
    #return render_to_response("index.html", kwargs, context_instance=RequestContext(request))
    #return_to_response('index.html', {'title': 'Configura','form': form}, context_instance=RequestContext(request))



