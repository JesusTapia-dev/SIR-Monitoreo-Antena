# Create your views here.
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from apps.main.models import Experiment, Configuration
from apps.main.views import sidebar

from .models import DDSConfiguration
from .forms import DDSConfigurationForm
# Create your views here.

from radarsys_api import jro_device, dds

def dds_conf(request, id_conf):

    conf = get_object_or_404(DDSConfiguration, pk=id_conf)
    
    if request.method=='GET':
        form = DDSConfigurationForm(instance=conf)
    
    answer = dds.echo(ip=str(conf.device.ip_address), port=conf.device.port_address)
    
    kwargs = {}
    kwargs['connected'] = (answer[0] == "1") 
    kwargs['form'] = form
    
    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = ['experiment', 'device',
                               'clock', 'multiplier',
                               'frequency',
#                                 'frequency_bin',
                                'phase',
#                                'phase_binary',
                               'amplitude_ch_A', 'amplitude_ch_B']
#                                'modulation',
#                                'frequency_mod',
#                                 'frequency_mod_bin',
#                                'phase_mod']
#                                'phase_binary_mod']
    
    kwargs['title'] = 'DDS Configuration'
    kwargs['suptitle'] = 'Details'
    
    kwargs['button'] = 'Edit Configuration'
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf))
    
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
    kwargs['dds_nbits'] = conf.get_nbits()
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf))
    
    return render(request, 'dds_conf_edit.html', kwargs)

def dds_conf_write(request, id_conf):
    
    conf = get_object_or_404(DDSConfiguration, pk=id_conf)
    
    answer = dds.write_config(ip=str(conf.device.ip_address),
                             port=conf.device.port_address,
                             clock=conf.clock,
                             multiplier=conf.multiplier,
                             freq_regA=conf.frequency_bin,
                             freq_regB=conf.frequency_mod_bin,
                             modulation=conf.modulation,
                             phaseA=conf.phase,
                             phaseB=conf.phase_mod,
                             amplitude0=conf.amplitude_ch_A,
                             amplitude1=conf.amplitude_ch_B)
    
    if answer[0] == "1":
        messages.success(request, answer[2:])
    else:
        messages.error(request, answer)
    
    return redirect('url_dds_conf', id_conf=conf.id)

def dds_conf_read(request, id_conf):
    
    conf = get_object_or_404(DDSConfiguration, pk=id_conf)
        
    if request.method=='POST':
        form = DDSConfigurationForm(request.POST, instance=conf)
        
        if form.is_valid():
            dds_model = form.save(commit=False)
            
            if dds_model.verify_frequencies():
                
                dds_model.save()
                return redirect('url_dds_conf', id_conf=conf.id)
    
    parms = None
    
    if request.method=='GET':
          
        #mult, freqA, freqB, modulation, phaseA, phaseB, amp0, amp1
        parms = dds.read_config(ip=conf.device.ip_address,
                          port=conf.device.port_address)
    
    if parms is None:
        return redirect('url_dds_conf', id_conf=conf.id)
        
    data = {'experiment' : conf.experiment.id,
            'device' : conf.device.id,
            'clock' : conf.clock,
            'multiplier' : parms[0],
            'frequency' : conf.binary2freq(parms[1], parms[0]*conf.clock),
            'frequency_bin' : parms[1],
            'phase' : parms[4],
            'amplitude_ch_A' : parms[6],
            'amplitude_ch_B' : parms[7],
            'modulation' : parms[3],
            'frequency_mod' : conf.binary2freq(parms[2], parms[0]*conf.clock),
            'frequency_mod_bin' : parms[2],
            'phase_mod' : parms[5],
            }
    
    form = DDSConfigurationForm(data)
    
    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Parameters read from device'
    kwargs['button'] = 'Save'
    kwargs['dds_nbits'] = conf.get_nbits()
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf))
    
    return render(request, 'dds_conf_edit.html', kwargs)