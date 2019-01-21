# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404

# from apps.main.models import Experiment, Configuration
from apps.main.views import sidebar

from .models import DDSConfiguration
from .forms import DDSConfigurationForm
# Create your views here.

def dds_conf(request, id_conf):

    conf = get_object_or_404(DDSConfiguration, pk=id_conf)

    kwargs = {}

    kwargs['status'] = conf.device.get_status_display()

#     if not kwargs['connected']:
#         messages.error(request, message=answer)

    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = [
                               'clock',
                               'multiplier',
                               'frequencyA_Mhz',
                                'frequencyA',
                                'frequencyB_Mhz',
                                'frequencyB',
                                'phaseA_degrees',
                                'phaseB_degrees',
                                'modulation',
                                'amplitude_enabled',
                                'amplitudeI',
                                'amplitudeQ']

    kwargs['title'] = 'DDS Configuration'
    kwargs['suptitle'] = 'Details'

    kwargs['button'] = 'Edit Configuration'

    ###### SIDEBAR ######
    kwargs.update(sidebar(conf=conf))

    return render(request, 'dds_conf.html', kwargs)

def dds_conf_edit(request, id_conf):

    conf = get_object_or_404(DDSConfiguration, pk=id_conf)

    if request.method=='GET':
        form = DDSConfigurationForm(instance=conf)

    if request.method=='POST':
        form = DDSConfigurationForm(request.POST, instance=conf)

        if form.is_valid():
            conf = form.save(commit=False)

            if conf.verify_frequencies():

                conf.save()
                return redirect('url_dds_conf', id_conf=conf.id)

            ##ERRORS

    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Save'

    return render(request, 'dds_conf_edit.html', kwargs)
