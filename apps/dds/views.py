# Create your views here.
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from django.core.exceptions import ValidationError

# from apps.main.models import Experiment, Configuration
from apps.main.views import sidebar

from .models import DDSConfiguration
from .forms import DDSConfigurationForm, UploadFileForm
# Create your views here.

from radarsys_api import dds

def dds_conf(request, id_conf):

    conf = get_object_or_404(DDSConfiguration, pk=id_conf)
    
    answer = dds.echo(ip=str(conf.device.ip_address), port=conf.device.port_address)
    
    kwargs = {}
    
    kwargs['connected'] = (answer[0] == "1")
    
    if not kwargs['connected']:
        messages.error(request, message=answer)
    
    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = ['experiment', 'device',
                               'clock', 'multiplier',
                               'frequency',
                                'frequency_bin',
                                'phase',
#                                'phase_binary',
                               'amplitude_ch_A', 'amplitude_ch_B',
                                'modulation',
                                'frequency_mod',
                                'frequency_mod_bin',
                                'phase_mod']
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
                             phaseA=conf.phase2binary(conf.phase),
                             phaseB=conf.phase2binary(conf.phase_mod),
                             amplitude0=conf.amplitude_ch_A,
                             amplitude1=conf.amplitude_ch_B)
    
    if answer[0] == "1":
        messages.success(request, answer[2:])
        
        conf.pk = None
        conf.id = None
        conf.type = 1
        conf.save()
        
    else:
        messages.error(request, "Could not write the parameters to this device")
    
    return redirect('url_dds_conf', id_conf=id_conf)

def dds_conf_read(request, id_conf):
    
    conf = get_object_or_404(DDSConfiguration, pk=id_conf)
    
    if request.method=='POST':
        form = DDSConfigurationForm(request.POST, instance=conf)
        
        if form.is_valid():
            dds_model = form.save(commit=False)
            
            if dds_model.verify_frequencies():
                
                dds_model.save()
                return redirect('url_dds_conf', id_conf=conf.id)
        
        messages.error(request, "Parameters could not be saved")
        
        data = {}
    
    if request.method=='GET':
        #mult, freqA, freqB, modulation, phaseA, phaseB, amp0, amp1
        parms = dds.read_config(ip=conf.device.ip_address,
                          port=conf.device.port_address)
        
        if not parms:
            messages.error(request, "Could not read dds parameters from this device")
            return redirect('url_dds_conf', id_conf=conf.id)
            
        data = {'multiplier' : parms[0],
                'frequency' : conf.binary2freq(parms[1], parms[0]*conf.clock),
                'frequency_bin' : parms[1],
                'phase' : conf.binary2phase(parms[4]),
                'amplitude_ch_A' : parms[6],
                'amplitude_ch_B' : parms[7],
                'modulation' : parms[3],
                'frequency_mod' : conf.binary2freq(parms[2], parms[0]*conf.clock),
                'frequency_mod_bin' : parms[2],
                'phase_mod' : conf.binary2phase(parms[5]),
                }
    
        form = DDSConfigurationForm(initial=data, instance=conf)
    
    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Parameters read from device'
    kwargs['button'] = 'Save'
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf))
    
    return render(request, 'dds_conf_edit.html', kwargs)

def dds_conf_import(request, id_conf):
    
    conf = get_object_or_404(DDSConfiguration, pk=id_conf)
    
    if request.method == 'POST':
        file_form = UploadFileForm(request.POST, request.FILES)
        
        if file_form.is_valid():
            
            if conf.update_from_file(request.FILES['file']):
            
                try:
                    conf.full_clean()
                except ValidationError as e:
                    messages.error(request, e)
                else:
                    conf.save()
                    
                    messages.success(request, "Parameters imported from file: '%s'." %request.FILES['file'].name)
                    messages.warning(request, "Clock Input could not be read from file, using %3.2fMhz by default. Please update it to its real value" %conf.clock)
                    return redirect('url_dds_conf', id_conf=conf.id)
        
        messages.error(request, "Could not import parameters from file")
        
    else:
        file_form = UploadFileForm()
    
    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['title'] = 'Device Configuration'
    kwargs['form'] = file_form
    kwargs['suptitle'] = 'Importing file'
    kwargs['button'] = 'Import'
    
    kwargs.update(sidebar(conf))
    
    return render(request, 'dds_conf_import.html', kwargs)

def handle_uploaded_file(f):
    
    data = {'multiplier' : 5,
            'frequency' : 49.92,
            'frequency_bin' : 45678,
            'phase' : 0,
            'amplitude_ch_A' : 1024,
            'amplitude_ch_B' : 2014,
            'modulation' : 1,
            'frequency_mod' : 0,
            'frequency_mod_bin' : 0,
            'phase_mod' : 180,
            }
    
    
    return data