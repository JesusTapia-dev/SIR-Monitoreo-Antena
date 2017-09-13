from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from apps.main.models import Device
from apps.main.views import sidebar

from .models import JARSConfiguration, JARSfilter
from .forms import JARSConfigurationForm, JARSfilterForm, JARSImportForm

import json
# Create your views here.

def jars_conf(request, id_conf):

    conf = get_object_or_404(JARSConfiguration, pk=id_conf)

    filter_parms = eval(conf.filter_parms)
    if filter_parms.__class__.__name__=='str':
        filter_parms = eval(filter_parms)

    kwargs = {}
    kwargs['filter'] = filter_parms
    kwargs['filter_keys']  = ['clock', 'mult', 'fch', 'fch_decimal',
                                'filter_fir', 'filter_2', 'filter_5']
    
    filter_resolution=conf.filter_resolution()
    kwargs['resolution'] = '{} (MHz)'.format(filter_resolution)
    if filter_resolution < 1:
        kwargs['resolution'] = '{} (kHz)'.format(filter_resolution*1000)
    
    kwargs['status'] = conf.device.get_status_display()


    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = ['name',
                               'cards_number', 'channels_number', 'channels',
                               #'rd_directory', 'pd_directory',
                               'data_type',
                               'acq_profiles', 'profiles_block', 'raw_data_blocks', 'ftp_interval', 'fftpoints',
                               'cohe_integr_str', 'decode_data',
                               'incohe_integr', 'cohe_integr', 'spectral_number',
                               'spectral', 'create_directory', 'include_expname',
                               'save_ch_dc', 'save_data']

    kwargs['title'] = 'JARS Configuration'
    kwargs['suptitle'] = 'Details'

    kwargs['button'] = 'Edit Configuration'

    #kwargs['no_play'] = True

    #kwargs['only_stop'] = True

    ###### SIDEBAR ######
    kwargs.update(sidebar(conf=conf))

    return render(request, 'jars_conf.html', kwargs)

def jars_conf_edit(request, id_conf):

    conf = get_object_or_404(JARSConfiguration, pk=id_conf)

    filter_parms = eval(conf.filter_parms)
    if filter_parms.__class__.__name__=='str':
        filter_parms = eval(filter_parms)

    if request.method=='GET':
        form = JARSConfigurationForm(instance=conf)
        filter_form = JARSfilterForm(initial=filter_parms)

    if request.method=='POST':
        form = JARSConfigurationForm(request.POST, instance=conf)
        filter_form = JARSfilterForm(request.POST)

        if filter_form.is_valid():
            jars_filter = filter_form.cleaned_data
            try:
                jars_filter.pop('name')
            except:
                pass

        if form.is_valid():
            conf = form.save(commit=False)
            conf.filter_parms = json.dumps(jars_filter)
            conf.save()
            return redirect('url_jars_conf', id_conf=conf.id)

    kwargs = {}

    kwargs['id_dev'] = conf.id
    kwargs['form'] = form
    kwargs['filter_form'] = filter_form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Save'

    return render(request, 'jars_conf_edit.html', kwargs)

def import_file(request, conf_id):

    conf = get_object_or_404(JARSConfiguration, pk=conf_id)
    if request.method=='POST':
        form = JARSImportForm(request.POST, request.FILES)
        if form.is_valid():
            #try:
            if True:
                data = conf.import_from_file(request.FILES['file_name'])
                conf.dict_to_parms(data)
                messages.success(request, 'Configuration "%s" loaded succesfully' % request.FILES['file_name'])
                return redirect(conf.get_absolute_url_edit())

            #except Exception as e:
            #    messages.error(request, 'Error parsing file: "%s" - %s' % (request.FILES['file_name'], e))

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



def change_filter(request, conf_id, filter_id=None):

    conf = get_object_or_404(JARSConfiguration, pk=conf_id)
    
    if filter_id:
        if filter_id.__class__.__name__ not in ['int', 'float']:
            filter_id = eval(filter_id)
            
    if filter_id == 0:
        return redirect('url_change_jars_filter', conf_id=conf.id)

    if request.method=='GET':
        if not filter_id:
            form = JARSfilterForm(initial={'filter_id': 0})
        else:
            form = JARSfilterForm(initial={'filter_id': filter_id})

    if request.method=='POST':
        form = JARSfilterForm(request.POST)
        if form.is_valid():
            jars_filter = form.cleaned_data
            try:
                jars_filter.pop('name')
            except:
                pass
            conf.filter_parms = json.dumps(jars_filter)
            conf.save()
            return redirect('url_edit_jars_conf', id_conf=conf.id)
        else:
            messages.error(request, "Select a Filter Template")
            return redirect('url_change_jars_filter', conf_id=conf.id)

    kwargs = {}
    kwargs['title'] = 'JARS Configuration'
    kwargs['suptitle'] = 'Change Filter'
    kwargs['form'] = form
    kwargs['button'] = 'Change'
    kwargs['conf_id'] = conf.id
    kwargs['filter_id'] = filter_id
    return render(request, 'change_jars_filter.html', kwargs)


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