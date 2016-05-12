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
    kwargs['dev_conf_keys'] = ['name',
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

# def dds_conf_import(request, id_conf):
#     
#     conf = get_object_or_404(DDSConfiguration, pk=id_conf)
#     
#     if request.method == 'GET':
#         file_form = UploadFileForm()
#         
#     if request.method == 'POST':
#         file_form = UploadFileForm(request.POST, request.FILES)
#         
#         if file_form.is_valid():
#             
#             parms = files.read_dds_file(request.FILES['file'])
#         
#             if parms:
#                 
#                 if not parms['clock']:
#                     messages.warning(request, "Clock Input could not be imported from '%s'. Please fill it out." %request.FILES['file'].name)
#                 else:
#                     messages.success(request, "Parameters imported from: '%s'." %request.FILES['file'].name)
#                 
#                 form = DDSConfigurationForm(initial=parms, instance=conf)
#                 
#                 kwargs = {}
#                 kwargs['id_dev'] = conf.id
#                 kwargs['form'] = form
#                 kwargs['title'] = 'Device Configuration'
#                 kwargs['suptitle'] = 'Parameters imported'
#                 kwargs['button'] = 'Save'
#                 kwargs['action'] = conf.get_absolute_url_edit()
#                 kwargs['previous'] = conf.get_absolute_url()
#                 
#                 ###### SIDEBAR ######
#                 kwargs.update(sidebar(conf))
#                 
#                 return render(request, 'dds_conf_edit.html', kwargs)
# 
#         messages.error(request, "Could not import parameters from file")
#     
#     kwargs = {}
#     kwargs['id_dev'] = conf.id
#     kwargs['title'] = 'Device Configuration'
#     kwargs['form'] = file_form
#     kwargs['suptitle'] = 'Importing file'
#     kwargs['button'] = 'Import'
#     
#     kwargs.update(sidebar(conf))
#     
#     return render(request, 'dds_conf_import.html', kwargs)
# 
# def dds_conf_export(request, id_conf):
#     
#     conf = get_object_or_404(DDSConfiguration, pk=id_conf)
#     
#     response = HttpResponse(content_type='text/plain')
#     response['Content-Disposition'] = 'attachment; filename="%s.dds"' %conf.name
#     response.write(conf.export_parms_to_dict())
#     
#     return response
# 
# def dds_conf_start(request, id_conf):
#     
#     conf = get_object_or_404(DDSConfiguration, pk=id_conf)
#     
#     if conf.start_device():
#         messages.success(request, conf.message)
#     else:
#         messages.error(request, conf.message)
#         
#     return redirect('url_dds_conf', id_conf=conf.id)
# 
# def dds_conf_stop(request, id_conf):
#     
#     conf = get_object_or_404(DDSConfiguration, pk=id_conf)
#     
#     if conf.stop_device():
#         messages.success(request, conf.message)
#     else:
#         messages.error(request, conf.message)
#     
#     return redirect('url_dds_conf', id_conf=conf.id)
# 
# def dds_conf_status(request, id_conf):
#     
#     conf = get_object_or_404(DDSConfiguration, pk=id_conf)
#     
#     if conf.status_device():
#         messages.success(request, conf.message)
#     else:
#         messages.error(request, conf.message)
#     
#     return redirect('url_dds_conf', id_conf=conf.id)
# 
# 
# def dds_conf_write(request, id_conf):
#     
#     conf = get_object_or_404(DDSConfiguration, pk=id_conf)
#     
#     answer = conf.write_device()
#     
#     if answer:
#         messages.success(request, conf.message)
#         
#         conf.pk = None
#         conf.id = None
#         conf.type = 1
#         conf.template = 0
#         conf.save()
#         
#     else:
#         messages.error(request, conf.message)
#     
#     return redirect('url_dds_conf', id_conf=id_conf)
# 
# def dds_conf_read(request, id_conf):
#     
#     conf = get_object_or_404(DDSConfiguration, pk=id_conf)
#     
#     if request.method=='GET':
#         
#         parms = conf.read_device()
#         
#         if not parms:
#             messages.error(request, conf.message)
#             return redirect('url_dds_conf', id_conf=conf.id)
#     
#         messages.warning(request, "Clock Input cannot be read from device. Please fill it out.")
#         
#         form = DDSConfigurationForm(initial=parms, instance=conf)
#     
#     if request.method=='POST':
#         form = DDSConfigurationForm(request.POST, instance=conf)
#         
#         if form.is_valid():
#             dds_model = form.save(commit=False)
#             
#             if dds_model.verify_frequencies():
#                 
#                 dds_model.save()
#                 return redirect('url_dds_conf', id_conf=conf.id)
#         
#         messages.error(request, "DDS parameters could not be saved")
#         
#     kwargs = {}
#     kwargs['id_dev'] = conf.id
#     kwargs['form'] = form
#     kwargs['title'] = 'Device Configuration'
#     kwargs['suptitle'] = 'Parameters read from device'
#     kwargs['button'] = 'Save'
#     
#     ###### SIDEBAR ######
#     kwargs.update(sidebar(conf))
#     
#     return render(request, 'dds_conf_edit.html', kwargs)