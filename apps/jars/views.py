from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from apps.main.models import Device
from apps.main.views import sidebar

from .models import JARSConfiguration, JARSFilter
from .forms import JARSConfigurationForm, JARSFilterForm, JARSImportForm

import json
# Create your views here.

def jars_conf(request, id_conf):

    conf = get_object_or_404(JARSConfiguration, pk=id_conf)

    filter_parms = json.loads(conf.filter_parms)

    kwargs = {}
    kwargs['filter'] = filter_parms
    kwargs['filter_obj'] = JARSFilter.objects.get(pk=1)
    kwargs['filter_keys']  = ['clock', 'multiplier', 'frequency', 'f_decimal',
                              'cic_2', 'scale_cic_2', 'cic_5', 'scale_cic_5', 'fir', 
                              'scale_fir', 'number_taps', 'taps']

    filter_resolution = conf.filter_resolution()
    kwargs['resolution'] = '{} (MHz)'.format(filter_resolution)
    if filter_resolution < 1:
        kwargs['resolution'] = '{} (kHz)'.format(filter_resolution*1000)

    kwargs['status'] = conf.device.get_status_display()
    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = ['cards_number', 'channels_number', 'channels',
                               'ftp_interval', 'data_type','acq_profiles',
                               'profiles_block', 'raw_data_blocks', 'ftp_interval',
                               'cohe_integr_str', 'cohe_integr', 'decode_data', 'post_coh_int',
                               'incohe_integr', 'fftpoints', 'spectral_number',
                               'spectral', 'create_directory', 'include_expname',
                               'save_ch_dc', 'save_data']

    if conf.exp_type == 0:
        for field in ['incohe_integr','fftpoints','spectral_number', 'spectral', 'save_ch_dc']:
            kwargs['dev_conf_keys'].remove(field)

    if conf.decode_data == 0:
        kwargs['dev_conf_keys'].remove('decode_data')
        kwargs['dev_conf_keys'].remove('post_coh_int')

    kwargs['title'] = 'JARS Configuration'
    kwargs['suptitle'] = 'Details'

    ###### SIDEBAR ######
    kwargs.update(sidebar(conf=conf))

    return render(request, 'jars_conf.html', kwargs)

def jars_conf_edit(request, id_conf):

    conf = get_object_or_404(JARSConfiguration, pk=id_conf)

    filter_parms = json.loads(conf.filter_parms)
    
    if request.method=='GET':
        form = JARSConfigurationForm(instance=conf)
        filter_form = JARSFilterForm(initial=filter_parms)

    if request.method=='POST':
        form = JARSConfigurationForm(request.POST, instance=conf)
        filter_form = JARSFilterForm(request.POST)

        if filter_form.is_valid():
           jars_filter = filter_form.cleaned_data
           jars_filter['id'] = request.POST['filter_template']
        else:
           messages.error(request, filter_form.errors)

        if form.is_valid():
            conf = form.save(commit=False)
            conf.filter_parms = json.dumps(jars_filter)
            conf.save()
            return redirect('url_jars_conf', id_conf=conf.id)

    kwargs = {}

    kwargs['id_dev'] = conf.id
    kwargs['form'] = form
    kwargs['filter_form'] = filter_form
    kwargs['filter_name'] = JARSFilter.objects.get(pk=filter_parms['id']).name
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Save'

    return render(request, 'jars_conf_edit.html', kwargs)

def import_file(request, conf_id):

    conf = get_object_or_404(JARSConfiguration, pk=conf_id)
    if request.method=='POST':
        form = JARSImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data = conf.import_from_file(request.FILES['file_name'])
                conf.dict_to_parms(data)
                messages.success(request, 'Configuration "%s" loaded succesfully' % request.FILES['file_name'])
                return redirect(conf.get_absolute_url_edit())

            except Exception as e:
                messages.error(request, 'Error parsing file: "%s" - %s' % (request.FILES['file_name'], repr(e)))
    else:
        messages.warning(request, 'Your current configuration will be replaced')
        form = JARSImportForm()

    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'JARS Configuration'
    kwargs['suptitle'] = 'Import file'
    kwargs['button'] = 'Upload'
    kwargs['previous'] = conf.get_absolute_url()

    return render(request, 'jars_import.html', kwargs)

def read_conf(request, conf_id):

    conf   = get_object_or_404(JARSConfiguration, pk=conf_id)
    #filter = get_object_or_404(JARSfilter, pk=filter_id)

    if request.method=='GET':

        parms = conf.read_device()
        conf.status_device()

        if not parms:
            messages.error(request, conf.message)
            return redirect(conf.get_absolute_url())

        form = JARSConfigurationForm(initial=parms, instance=conf)

    if request.method=='POST':
        form = JARSConfigurationForm(request.POST, instance=conf)

        if form.is_valid():
            form.save()
            return redirect(conf.get_absolute_url())

        messages.error(request, "Parameters could not be saved")

    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['filter_id'] = conf.filter.id
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Parameters read from device'
    kwargs['button'] = 'Save'

    ###### SIDEBAR ######
    kwargs.update(sidebar(conf=conf))

    return render(request, 'jars_conf_edit.html', kwargs)

def change_filter(request, conf_id, filter_id):

    conf = get_object_or_404(JARSConfiguration, pk=conf_id)
    filter = get_object_or_404(JARSFilter, pk=filter_id)
    conf.filter_parms = json.dumps(filter.jsonify())
    conf.save()

    return redirect('url_edit_jars_conf', id_conf=conf.id)    

def get_log(request, conf_id):

    conf = get_object_or_404(JARSConfiguration, pk=conf_id)
    response = conf.get_log()

    if not response:
        message = conf.message
        messages.error(request, message)
        return redirect('url_jars_conf', id_conf=conf.id)

    try:
        message = response.json()['message']
        messages.error(request, message)
        return redirect('url_jars_conf', id_conf=conf.id)
    except Exception as e:
        message = 'Restarting Report.txt has been downloaded successfully.'

    content = response
    filename     =  'Log_%s_%s.txt' %(conf.experiment.name, conf.experiment.id)
    response = HttpResponse(content,content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s"' %filename

    return response
