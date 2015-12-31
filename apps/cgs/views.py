from django.shortcuts import render, render_to_response
from django.template import RequestContext

from .forms import CGSConfigurationForm
from .models import CGSConfiguration
from apps.main.models import Device
# Create your views here.

def configurate_frequencies(request, id=0):
    
    if id:
        conf = CGSConfiguration.objects.get(pk=id)
        devices = Device.objects.filter(configuration__experiment=conf.experiment)
        devices = devices.values('configuration__id', 'device_type__name')
        for device in devices:
            if device['device_type__name']=='cgs':
                device['active'] = 'active'
                break
        
        device = device
        form = CGSConfigurationForm(instance=conf)
    else:
        form = CGSConfigurationForm()

    data = {
        'form': form,
        'device': device,
        'devices':devices,
        'title': ('YAP'),
    }
    
    data['dev_conf'] = conf
    data['dev_conf_keys'] = ['experiment', 'device']
    
    if request.method == 'POST':
        form = CGSConfigurationForm(request.POST) #, initial={'purchase_request':purchase_request}) 
        if form.is_valid():
            instance = form.save(commit=False)
            #if 'quote' in request.FILES:
            #    instance.quoe = request.FILES['quote']
            instance.save()
            form.save_m2m()
            msg = _(u'The frequencies have been activated successfully.')
            messages.success(request, msg, fail_silently=True)    
            #return redirect(purchase_request.get_absolute_url())
    else:
        form = CGSConfigurationForm()           
    
    return render(request, 'cgs_conf.html', data)


