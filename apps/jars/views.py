from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

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
    kwargs['resolution'] = filter_resolution

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

def view_filter(request, conf_id, filter_id):

    conf = get_object_or_404(JARSConfiguration, pk=conf_id)
    filter = get_object_or_404(JARSfilter, pk=filter_id)

    filter_parms       = eval(conf.filter_parms)
    if filter_parms.__class__.__name__=='str':
        filter_parms       = eval(filter_parms)
    #filter.name        = filter_parms['name']
    filter.clock       = filter_parms['clock']
    filter.mult        = filter_parms['mult']
    filter.fch         = filter_parms['fch']
    filter.fch_decimal = filter_parms['fch_decimal']
    filter.filter_fir  = filter_parms['filter_fir']
    filter.filter_2    = filter_parms['filter_2']
    filter.filter_5    = filter_parms['filter_5']

    kwargs = {}
    kwargs['conf']          = conf
    kwargs['filter']        = filter
    kwargs['dev_conf']      = filter
    kwargs['dev_conf_keys'] = ['clock', 'mult', #'name',
                               'fch', 'fch_decimal',
                               'filter_2', 'filter_5',
                               'filter_fir']

    kwargs['title']         = 'Filter View'
    kwargs['suptitle']      = 'Details'
    kwargs['button']        = 'SI'
    kwargs['edit_button']   = 'Edit Filter'
    kwargs['add_button']    = 'New Filter'

    return render(request, 'jars_filter.html', kwargs)

def edit_filter(request, conf_id, filter_id):

    conf = get_object_or_404(JARSConfiguration, pk=conf_id)
    filter_parms = eval(conf.filter_parms)

    if filter_id:
        filter = get_object_or_404(JARSfilter, pk=filter_id)

    if request.method=='GET':
        form = JARSfilterForm(initial=filter_parms)

    if request.method=='POST':
        parms = {}
        #parms['name']        = request.POST['name']
        parms['clock']       = request.POST['clock']
        parms['mult']        = request.POST['mult']
        parms['fch']         = request.POST['fch']
        parms['fch_decimal'] = request.POST['fch_decimal']
        parms['filter_fir'] = request.POST['filter_fir']
        parms['filter_2']   = request.POST['filter_2']
        parms['filter_5']   = request.POST['filter_5']

        conf.filter_parms = parms
        conf.save()

        #form = JARSfilterForm(request.POST)
        #form = JARSfilterForm(request.POST, instance=filter)
        #if form.is_valid():
            #form.save()
        #    messages.success(request, 'JARS Filter successfully updated')
        #    return redirect('url_jars_filter', conf.id, filter.id)
        return redirect('url_jars_filter', conf.id, filter.id)

    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = conf.name
    kwargs['suptitle'] = 'Edit Filter'
    kwargs['button'] = 'Save'
   # kwargs['previous'] = conf.get_absolute_url_edit()
    kwargs['dev_conf'] = conf

    return render(request, 'jars_filter_edit.html', kwargs)

def new_filter(request, conf_id):

    conf = get_object_or_404(JARSConfiguration, pk=conf_id)

    if request.method=='GET':
        form = JARSfilterForm()

    if request.method=='POST':
        form = JARSfilterForm(request.POST)
        if form.is_valid():
            form.save()
            new_filter  = get_object_or_404(JARSfilter, name=request.POST['name'])
            conf.filter = new_filter
            conf.add_parms_to_filter()
            messages.success(request, 'New JARS Filter successfully created')
            return redirect('url_edit_jars_conf', id_conf=conf.id)

    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'New Filter'
    kwargs['suptitle'] = ''
    kwargs['button'] = 'Create'
   # kwargs['previous'] = conf.get_absolute_url_edit()
    kwargs['dev_conf'] = conf

    return render(request, 'jars_new_filter.html', kwargs)


def change_filter(request, conf_id, filter_id=None):

    conf = get_object_or_404(JARSConfiguration, pk=conf_id)
    
    if filter_id:
        if filter_id.__class__.__name__ not in ['int', 'float']:
            filter_id = eval(filter_id)
            
    if filter_id == 0:
        return redirect('url_change_jars_filter', conf_id=conf.id)

    if request.method=='GET':
        if not filter_id:
            form = JARSfilterForm(initial={'jars_configuration':conf_id, 'filter_id': 0})
        else:
            form = JARSfilterForm(initial={'jars_configuration':conf_id, 'filter_id': filter_id})

    kwargs = {}
    kwargs['title'] = 'JARS Configuration'
    kwargs['suptitle'] = 'Change Filter'
    kwargs['form'] = form
    kwargs['conf_id'] = conf.id
    kwargs['filter_id'] = filter_id
    return render(request, 'change_jars_filter.html', kwargs)
