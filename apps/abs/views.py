from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from time import sleep
import os
import io

from apps.main.models import Device, Configuration, Experiment
from apps.main.views import sidebar

from .models import ABSConfiguration, ABSBeam
from .forms import ABSConfigurationForm, ABSBeamEditForm, ABSBeamAddForm, ABSImportForm

from .utils.overJroShow import overJroShow
from .utils.OverJRO import OverJRO
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

    conf = get_object_or_404(ABSConfiguration, pk=id_conf)
    beams = ABSBeam.objects.filter(abs_conf=conf)
    #------------Colors for Active Beam:-------------
    all_status = {}
    module_messages = json.loads(conf.module_messages)

    color_status   = {}
    for i, status in enumerate(conf.module_status):
        if status == '3':    #Running background-color: #00cc00;
            all_status['{}'.format(i+1)] = 2
            color_status['{}'.format(i+1)] = 'class=text-success'#'bgcolor=#00cc00'
        elif status == '1':  #Connected background-color: #ee902c;
            all_status['{}'.format(i+1)] = 1
            color_status['{}'.format(i+1)] = 'class=text-warning'#'bgcolor=#ee902c'
        else:                #Disconnected background-color: #ff0000;
            all_status['{}'.format(i+1)] = 0
            color_status['{}'.format(i+1)] = 'class=text-danger'#'bgcolor=#FF0000'
    #------------------------------------------------

    kwargs = {}
    kwargs['connected_modules'] = str(conf.connected_modules())+'/64'
    kwargs['dev_conf'] = conf
    
    if conf.operation_mode == 0:
        kwargs['dev_conf_keys'] = ['label', 'operation_mode']
    else:
        kwargs['dev_conf_keys'] = ['label', 'operation_mode', 'operation_value']

    kwargs['title'] = 'ABS Configuration'
    kwargs['suptitle'] = 'Details'
    kwargs['button'] = 'Edit Configuration'
    
    if conf.active_beam != 0:
        kwargs['active_beam'] = int(conf.active_beam)

    kwargs['beams'] = beams
    kwargs['modules_status'] = all_status
    kwargs['color_status']   = color_status
    kwargs['module_messages'] = module_messages
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf=conf))

    return render(request, 'abs_conf.html', kwargs)


def abs_conf_edit(request, id_conf):

    conf     = get_object_or_404(ABSConfiguration, pk=id_conf)

    beams = ABSBeam.objects.filter(abs_conf=conf)

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

@csrf_exempt
def abs_conf_alert(request):

    if request.method == 'POST':
        print request.POST
        return HttpResponse(json.dumps({'result':1}), content_type='application/json')
    else:
        return redirect('index')


def import_file(request, id_conf):

    conf = get_object_or_404(ABSConfiguration, pk=id_conf)
    if request.method=='POST':
        form = ABSImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                parms = conf.import_from_file(request.FILES['file_name'])

                if parms:
                    conf.update_from_file(parms)
                    messages.success(request, 'Configuration "%s" loaded succesfully' % request.FILES['file_name'])
                    return redirect(conf.get_absolute_url_edit())

            except Exception as e:
                messages.error(request, 'Error parsing file: "%s" - %s' % (request.FILES['file_name'], e))

    else:
        messages.warning(request, 'Your current configuration will be replaced')
        form = ABSImportForm()

    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'ABS Configuration'
    kwargs['suptitle'] = 'Import file'
    kwargs['button'] = 'Upload'
    kwargs['previous'] = conf.get_absolute_url()

    return render(request, 'abs_import.html', kwargs)


def send_beam(request, id_conf, id_beam):

    conf = get_object_or_404(ABSConfiguration, pk=id_conf)
    beam = get_object_or_404(ABSBeam, pk=id_beam)
    beams_list    = ABSBeam.objects.filter(abs_conf=conf)
    conf.active_beam = id_beam

    i = 0
    for b in beams_list:
        if b.id == int(id_beam):
            break
        else:
            i += 1
    beam_pos = i + 1 #Estandarizar
    print '%s Position: %s' % (beam.name, str(beam_pos))
    conf.send_beam(beam_pos)

    return redirect('url_abs_conf', conf.id)


def add_beam(request, id_conf):

    conf     = get_object_or_404(ABSConfiguration, pk=id_conf)
    confs    = Configuration.objects.all()

    if request.method=='GET':
        form = ABSBeamAddForm()

    if request.method=='POST':
        form = ABSBeamAddForm(request.POST)

        beam_data = get_values_from_form(request.POST)

        new_beam = ABSBeam(
                   name = beam_data['name'],
                   antenna = json.dumps(beam_data['antenna']),
                   abs_conf = conf,
                   tx = json.dumps(beam_data['tx']),
                   rx = json.dumps(beam_data['rx']),
                   ues = json.dumps(beam_data['ues']),
                   only_rx = json.dumps(beam_data['only_rx'])
                   )
        new_beam.save()
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

    return render(request, 'abs_edit_beam.html', kwargs)



def remove_beam(request, id_conf, id_beam):

    conf     = get_object_or_404(ABSConfiguration, pk=id_conf)
    beam     = get_object_or_404(ABSBeam, pk=id_beam)

    if request.method=='POST':
        if beam:
            try:
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



def plot_patterns(request, id_conf, id_beam=None):

    kwargs = {}
    conf = get_object_or_404(ABSConfiguration, pk=id_conf)
    beams = ABSBeam.objects.filter(abs_conf=conf)

    if id_beam:
        beam  = get_object_or_404(ABSBeam, pk=id_beam)
        kwargs['beam'] = beam

    ###### SIDEBAR ######

    kwargs['dev_conf']   = conf.device
    kwargs['id_dev']     = conf.device
    kwargs['id_conf']    = conf.id
    kwargs['abs_beams']  = beams
    kwargs['title']      = 'ABS Patterns'
    kwargs['suptitle']   = conf.name
    kwargs['no_sidebar'] = True

    return render(request, 'abs_patterns.html', kwargs)


def plot_pattern(request, id_conf, id_beam, antenna):

    if antenna=='down':
        sleep(3)

    conf = get_object_or_404(ABSConfiguration, pk=id_conf)
    beam = get_object_or_404(ABSBeam, pk=id_beam)
    just_rx = 1 if json.loads(beam.only_rx)[antenna] else 0
    phases = json.loads(beam.antenna)['antenna_{}'.format(antenna)]
    gain_tx = json.loads(beam.tx)[antenna]
    gain_rx = json.loads(beam.rx)[antenna]
    ues = json.loads(beam.ues)[antenna]
    newOverJro = overJroShow(beam.name)
    fig = newOverJro.plotPattern2(datetime.today(), phases, gain_tx, gain_rx, ues, just_rx)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response
    
