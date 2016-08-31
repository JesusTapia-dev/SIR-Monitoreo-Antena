from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from apps.main.models import Device, Configuration
from apps.main.views import sidebar

from .models import ABSConfiguration, ABSBeam
from .forms import ABSConfigurationForm, ABSBeamEditForm, ABSBeamAddForm
# Create your views here.
import json, ast


def get_values_from_form(form_data):

    sublistup     = []
    sublistdown   = []
    subtxlistup   = []
    subtxlistdown = []
    subrxlistup   = []
    subrxlistdown = []

    up_values_list     = []
    down_values_list   = []
    up_txvalues_list   = []
    down_txvalues_list = []
    up_rxvalues_list   = []
    down_rxvalues_list = []

    values_list = {}
    cont = 1

    for i in range(1,65):
        x = float(form_data['abs_up'+str(i)])
        y = float(form_data['abs_down'+str(i)])
        sublistup.append(x)
        sublistdown.append(y)

        if str(i) in form_data.getlist('uptx_checks'):
            subtxlistup.append(1)
        else:
            subtxlistup.append(0)
        if str(i) in form_data.getlist('downtx_checks'):
            subtxlistdown.append(1)
        else:
            subtxlistdown.append(0)

        if str(i) in form_data.getlist('uprx_checks'):
            subrxlistup.append(1)
        else:
            subrxlistup.append(0)
        if str(i) in form_data.getlist('downrx_checks'):
            subrxlistdown.append(1)
        else:
            subrxlistdown.append(0)

        cont = cont+1

        if cont == 9:
            up_values_list.append(sublistup)
            down_values_list.append(sublistdown)
            sublistup   = []
            sublistdown = []

            up_txvalues_list.append(subtxlistup)
            down_txvalues_list.append(subtxlistdown)
            subtxlistup   = []
            subtxlistdown = []
            up_rxvalues_list.append(subrxlistup)
            down_rxvalues_list.append(subrxlistdown)
            subrxlistup   = []
            subrxlistdown = []
            cont = 1


    list_uesup   = []
    list_uesdown = []
    for i in range(1,5):
        if form_data['ues_up'+str(i)] == '':
            list_uesup.append(0.0)
        else:
            list_uesup.append(float(form_data['ues_up'+str(i)]))

        if form_data['ues_down'+str(i)] == '':
            list_uesdown.append(0.0)
        else:
            list_uesdown.append(float(form_data['ues_down'+str(i)]))

    onlyrx_list = form_data.getlist('onlyrx')
    only_rx = {}
    if '1' in onlyrx_list:
        only_rx['up'] = True
    else:
        only_rx['up'] = False
    if '2' in onlyrx_list:
        only_rx['down'] = True
    else:
        only_rx['down'] = False

    antenna = {'antenna_up': up_values_list, 'antenna_down': down_values_list}
    tx      = {'up': up_txvalues_list, 'down': down_txvalues_list}
    rx      = {'up': up_rxvalues_list, 'down': down_rxvalues_list}
    ues     = {'up': list_uesup, 'down': list_uesdown}
    name    = str(form_data['beam_name'])

    beam_data = {'name': name, 'antenna': antenna, 'tx': tx, 'rx': rx, 'ues': ues, 'only_rx': only_rx}

    return beam_data



def abs_conf(request, id_conf):

    conf     = get_object_or_404(ABSConfiguration, pk=id_conf)

    beams_dict = ast.literal_eval(conf.beams)
    beams = []
    for beam_id in range(1,len(beams_dict)+1):
        beam = ABSBeam.objects.get(pk=beams_dict['beam'+str(beam_id)])
        beams.append(beam)

    beams_id    = ast.literal_eval(conf.beams)

    ip=conf.device.ip_address
    port=conf.device.port_address

    kwargs = {}
    kwargs['status'] = conf.device.get_status_display()


    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = ['name',]

    kwargs['title'] = 'ABS Configuration'
    kwargs['suptitle'] = 'Details'
    kwargs['no_play'] = True

    kwargs['button'] = 'Edit Configuration'

    #kwargs['no_play'] = True
    kwargs['beams_id'] = beams_id
    kwargs['beams']    = beams
    kwargs['beam_selector'] = 0
    #kwargs['my_data'] =  simplejson.dumps(beams)

    kwargs['only_stop'] = True

    ###### SIDEBAR ######
    kwargs.update(sidebar(conf=conf))

    return render(request, 'abs_conf.html', kwargs)

def abs_conf_edit(request, id_conf):

    conf     = get_object_or_404(ABSConfiguration, pk=id_conf)
    beams_list = ast.literal_eval(conf.beams)
    i = 1
    beams = []
    for b in beams_list:
        beam = ABSBeam.objects.get(pk=beams_list['beam'+str(i)])
        beams.append(beam)
        i=i+1

    if request.method=='GET':
        form = ABSConfigurationForm(instance=conf)

    if request.method=='POST':
        form = ABSConfigurationForm(request.POST, instance=conf)

        if form.is_valid():
            conf = form.save(commit=False)
            conf.save()
            return redirect('url_abs_conf', id_conf=conf.id)

    ###### SIDEBAR ######
    kwargs = {}

    kwargs['dev_conf'] = conf
    #kwargs['id_dev'] = conf.id
    kwargs['id_conf'] = conf.id
    kwargs['form'] = form
    kwargs['abs_beams'] = beams
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Save'

    kwargs['edit'] = True

    return render(request, 'abs_conf_edit.html', kwargs)


def plot_patterns(request, id_conf):

    conf     = get_object_or_404(ABSConfiguration, pk=id_conf)
    beams_list = ast.literal_eval(conf.beams)
    i = 1
    beams = []
    for b in beams_list:
        beam = ABSBeam.objects.get(pk=beams_list['beam'+str(i)])
        beams.append(beam)
        i=i+1

    ###### SIDEBAR ######
    kwargs = {}

    kwargs['dev_conf'] = conf.device
    kwargs['id_dev'] = conf.device
    kwargs['id_conf'] = conf.id
    kwargs['abs_beams'] = beams
    kwargs['title'] = 'ABS Patterns'
    kwargs['suptitle'] = conf.name
    kwargs['no_sidebar'] = True

    return render(request, 'abs_patterns.html', kwargs)

def add_beam(request, id_conf):

    conf     = get_object_or_404(ABSConfiguration, pk=id_conf)
    confs    = Configuration.objects.all()

    if request.method=='GET':
        #form = ABSBeamEditForm()
        form = ABSBeamAddForm()

    if request.method=='POST':
        form = ABSBeamAddForm(request.POST)

        beam_data = get_values_from_form(request.POST)

        new_beam = ABSBeam(
                   name    =beam_data['name'],
                   antenna =json.dumps(beam_data['antenna']),
                   abs_conf=conf,
                   tx      =json.dumps(beam_data['tx']),
                   rx      =json.dumps(beam_data['rx']),
                   ues     =json.dumps(beam_data['ues']),
                   only_rx =json.dumps(beam_data['only_rx'])
                   )
        new_beam.save()
        #---Update 6bits configuration and add beam to abs configuration beams list.
        new_beam.modules_6bits()
        new_beam.add_beam2list()
        messages.success(request, 'Beam: "%s" has been added.'  % new_beam.name)

        return redirect('url_edit_abs_conf', conf.id)

    ###### SIDEBAR ######
    kwargs = {}

    #kwargs['dev_conf'] = conf.device
    #kwargs['id_dev'] = conf.device
    kwargs['id_conf'] = conf.id
    kwargs['form'] = form
    kwargs['title'] = 'ABS Beams'
    kwargs['suptitle'] = 'Add Beam'
    kwargs['button'] = 'Add'
    kwargs['no_sidebar'] = True

    #kwargs['previous'] = conf.get_absolute_url_edit()
    kwargs['edit'] = True

    return render(request, 'abs_add_beam.html', kwargs)


def edit_beam(request, id_conf, id_beam):

    conf = get_object_or_404(ABSConfiguration, pk=id_conf)
    beam = get_object_or_404(ABSBeam, pk=id_beam)

    if request.method=='GET':
        form = ABSBeamEditForm(initial={'beam': beam})

    if request.method=='POST':
        form = ABSBeamEditForm(request.POST)

        beam_data = get_values_from_form(request.POST)

        beam.dict_to_parms(beam_data)
        beam.save()

        messages.success(request, 'Beam: "%s" has been updated.'  % beam.name)

        return redirect('url_edit_abs_conf', conf.id)

    ###### SIDEBAR ######
    kwargs = {}

    kwargs['id_conf'] = conf.id
    kwargs['form'] = form
    kwargs['title'] = 'ABS Beams'
    kwargs['suptitle'] = 'Edit Beam'
    kwargs['button'] = 'Save'
    kwargs['no_sidebar'] = True

    #kwargs['previous'] = conf.get_absolute_url_edit()
    kwargs['edit'] = True

    return render(request, 'abs_add_beam.html', kwargs)



def remove_beam(request, id_conf, id_beam):

    conf     = get_object_or_404(ABSConfiguration, pk=id_conf)
    beam     = get_object_or_404(ABSBeam, pk=id_beam)

    if request.method=='POST':
        if beam:
            try:
                beam.remove_beamfromlist()
                beam.delete()
                messages.success(request, 'Beam: "%s" has been deleted.'  % beam)
            except:
                messages.error(request, 'Unable to delete beam: "%s".' % beam)

        return redirect('url_edit_abs_conf', conf.id)

    ###### SIDEBAR ######
    kwargs = {}

    kwargs['object'] = beam
    kwargs['delete'] = True
    kwargs['title'] = 'Delete'
    kwargs['suptitle'] = 'Beam'
    kwargs['previous'] = conf.get_absolute_url_edit()
    return render(request, 'confirm.html', kwargs)
