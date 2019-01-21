
import json

from django.contrib import messages
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required

from apps.main.models import Experiment, Device
from apps.main.views import sidebar

from .models import RCConfiguration, RCLine, RCLineType, RCLineCode
from .forms import RCConfigurationForm, RCLineForm, RCLineViewForm, RCLineEditForm, RCImportForm, RCLineCodesForm


def conf(request, conf_id):

    conf = get_object_or_404(RCConfiguration, pk=conf_id)

    lines = RCLine.objects.filter(rc_configuration=conf).order_by('channel')

    for line in lines:
        params = json.loads(line.params)
        line.form = RCLineViewForm(extra_fields=params, line=line)
        if 'params' in params:
            line.subforms = [RCLineViewForm(extra_fields=fields, line=line, subform=True) for fields in params['params']]

    kwargs = {}
    kwargs['dev_conf'] = conf
    kwargs['rc_lines'] = lines
    kwargs['dev_conf_keys'] = ['ipp_unit', 'ntx', 'clock_in', 'clock_divider', 'clock',
                               'time_before', 'time_after', 'sync', 'sampling_reference', 
                               'control_tx', 'control_sw']

    kwargs['title'] = 'Configuration'
    kwargs['suptitle'] = 'Detail'

    kwargs['button'] = 'Edit Configuration'
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf=conf))

    return render(request, 'rc_conf.html', kwargs)

@login_required
def conf_edit(request, conf_id):

    conf = get_object_or_404(RCConfiguration, pk=conf_id)

    lines = RCLine.objects.filter(rc_configuration=conf).order_by('channel')

    for line in lines:
        params = json.loads(line.params)
        line.form = RCLineEditForm(conf=conf, line=line, extra_fields=params)
        line.subform = False

        if 'params' in params:
            line.subforms = [RCLineEditForm(extra_fields=fields, line=line, subform=i) for i, fields in enumerate(params['params'])]
            line.subform = True

    if request.method=='GET':

        form = RCConfigurationForm(instance=conf)

    elif request.method=='POST':

        line_data = {}
        conf_data = {}
        extras = []

        #classified post fields
        for label,value in request.POST.items():
            if label=='csrfmiddlewaretoken':
                continue

            if label.count('|')==0:
                conf_data[label] = value
                continue

            elif label.split('|')[0]!='-1':
                extras.append(label)
                continue

            x, pk, name = label.split('|')

            if name=='codes':
                value = [s for s in value.split('\r\n') if s]

            if pk in line_data:
                line_data[pk][name] = value
            else:
                line_data[pk] = {name:value}

        #update conf
        form = RCConfigurationForm(conf_data, instance=conf)

        if form.is_valid():

            form.save()

            #update lines fields
            extras.sort()
            for label in extras:
                x, pk, name = label.split('|')
                if pk not in line_data:
                    line_data[pk] = {}
                if 'params' not in line_data[pk]:
                    line_data[pk]['params'] = []
                if len(line_data[pk]['params'])<int(x)+1:
                    line_data[pk]['params'].append({})
                line_data[pk]['params'][int(x)][name] = float(request.POST[label])

            for pk, params in line_data.items():
                line = RCLine.objects.get(pk=pk)
                if line.line_type.name in ('windows', 'prog_pulses'):
                    if 'params' not in params:
                        params['params'] = []
                line.params = json.dumps(params)
                line.save()

            #update pulses field
            conf.update_pulses()

            messages.success(request, 'RC Configuration successfully updated')

            return redirect(conf.get_absolute_url())

    kwargs = {}
    kwargs['dev_conf'] = conf
    kwargs['form'] = form
    kwargs['rc_lines'] = lines
    kwargs['edit'] = True

    kwargs['title'] = 'RC Configuration'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Update'

    return render(request, 'rc_conf_edit.html', kwargs)


def add_line(request, conf_id, line_type_id=None, code_id=None):

    conf = get_object_or_404(RCConfiguration, pk=conf_id)

    if request.method=='GET':
        if line_type_id:
            line_type = get_object_or_404(RCLineType, pk=line_type_id)

            if code_id:
                form = RCLineForm(initial={'rc_configuration':conf_id, 'line_type': line_type_id, 'code_id': code_id},
                                  extra_fields=json.loads(line_type.params))
            else:
                form = RCLineForm(initial={'rc_configuration':conf_id, 'line_type': line_type_id},
                                  extra_fields=json.loads(line_type.params))
        else:
            line_type = {'id':0}
            form = RCLineForm(initial={'rc_configuration':conf_id})

    if request.method=='POST':

        line_type = get_object_or_404(RCLineType, pk=line_type_id)
        form = RCLineForm(request.POST,
                          extra_fields=json.loads(line_type.params))

        if form.is_valid():
            form.save()
            form.instance.update_pulses()
            return redirect('url_edit_rc_conf', conf.id)

    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'RC Configuration'
    kwargs['suptitle'] = 'Add Line'
    kwargs['button'] = 'Add'
    kwargs['previous'] = conf.get_absolute_url_edit()
    kwargs['dev_conf'] = conf
    kwargs['line_type'] = line_type

    return render(request, 'rc_add_line.html', kwargs)

def edit_codes(request, conf_id, line_id, code_id=None):

    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    line = get_object_or_404(RCLine, pk=line_id)
    params = json.loads(line.params)

    if request.method=='GET':
        if code_id:
            code = get_object_or_404(RCLineCode, pk=code_id)
            form = RCLineCodesForm(instance=code)
        else:
            initial = {'code': params['code'],
                       'codes': params['codes'] if 'codes' in params else [],
                       'number_of_codes': len(params['codes']) if 'codes' in params else 0,
                       'bits_per_code': len(params['codes'][0]) if 'codes' in params else 0,
                       }
            form = RCLineCodesForm(initial=initial)

    if request.method=='POST':
        form = RCLineCodesForm(request.POST)
        if form.is_valid():
            params['code'] = request.POST['code']
            params['codes'] = [s for s in request.POST['codes'].split('\r\n') if s]
            line.params = json.dumps(params)
            line.save()
            messages.success(request, 'Line: "%s" has been updated.'  % line)
            return redirect('url_edit_rc_conf', conf.id)

    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = line
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Update'
    kwargs['dev_conf'] = conf
    kwargs['previous'] = conf.get_absolute_url_edit()
    kwargs['line'] = line

    return render(request, 'rc_edit_codes.html', kwargs)

def add_subline(request, conf_id, line_id):

    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    line = get_object_or_404(RCLine, pk=line_id)

    if request.method == 'POST':
        if line:
            params = json.loads(line.params)
            subparams = json.loads(line.line_type.params)
            if 'params' in subparams:
                dum = {}
                for key, value in subparams['params'].items():
                    dum[key] = value['value']
                params['params'].append(dum)
                line.params = json.dumps(params)
                line.save()
            return redirect('url_edit_rc_conf', conf.id)

    kwargs = {}

    kwargs['title'] = 'Add new'
    kwargs['suptitle'] = '%s to %s' % (line.line_type.name, line)

    return render(request, 'confirm.html', kwargs)

def remove_line(request, conf_id, line_id):

    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    line = get_object_or_404(RCLine, pk=line_id)

    if request.method == 'POST':
        if line:
            try:
                channel = line.channel
                line.delete()
                for ch in range(channel+1, RCLine.objects.filter(rc_configuration=conf).count()+1):
                    l = RCLine.objects.get(rc_configuration=conf, channel=ch)
                    l.channel = l.channel-1
                    l.save()
                messages.success(request, 'Line: "%s" has been deleted.'  % line)
            except:
                messages.error(request, 'Unable to delete line: "%s".' % line)

        return redirect('url_edit_rc_conf', conf.id)

    kwargs = {}

    kwargs['object'] = line
    kwargs['delete'] = True
    kwargs['title'] = 'Delete'
    kwargs['suptitle'] = 'Line'
    kwargs['previous'] = conf.get_absolute_url_edit()
    return render(request, 'confirm.html', kwargs)


def remove_subline(request, conf_id, line_id, subline_id):

    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    line = get_object_or_404(RCLine, pk=line_id)

    if request.method == 'POST':
        if line:
            params = json.loads(line.params)
            params['params'].remove(params['params'][int(subline_id)-1])
            line.params = json.dumps(params)
            line.save()

            return redirect('url_edit_rc_conf', conf.id)

    kwargs = {}

    kwargs['object'] = line
    kwargs['object_name'] = line.line_type.name
    kwargs['delete_view'] = True
    kwargs['title'] = 'Confirm delete'

    return render(request, 'confirm.html', kwargs)


def update_lines_position(request, conf_id):

    conf = get_object_or_404(RCConfiguration, pk=conf_id)

    if request.method=='POST':
        ch = 0
        for item in request.POST['items'].split('&'):
            line = RCLine.objects.get(pk=item.split('=')[-1])
            line.channel = ch
            line.save()
            ch += 1

        lines = RCLine.objects.filter(rc_configuration=conf).order_by('channel')

        for line in lines:
            params = json.loads(line.params)
            line.form = RCLineEditForm(conf=conf, line=line, extra_fields=params)

            if 'params' in params:
                line.subform = True
                line.subforms = [RCLineEditForm(extra_fields=fields, line=line, subform=i) for i, fields in enumerate(params['params'])]

        html = render(request, 'rc_lines.html', {'dev_conf':conf, 'rc_lines':lines, 'edit':True})
        data = {'html': html.content.decode('utf8')}

        return HttpResponse(json.dumps(data), content_type="application/json")
    return redirect('url_edit_rc_conf', conf.id)


def import_file(request, conf_id):

    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    if request.method=='POST':
        form = RCImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data = conf.import_from_file(request.FILES['file_name'])
                conf.dict_to_parms(data)
                conf.update_pulses()
                messages.success(request, 'Configuration "%s" loaded succesfully' % request.FILES['file_name'])
                return redirect(conf.get_absolute_url_edit())

            except Exception as e:
                messages.error(request, 'Error parsing file: "%s" - %s' % (request.FILES['file_name'], repr(e)))
    else:
        messages.warning(request, 'Your current configuration will be replaced')
        form = RCImportForm()

    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'RC Configuration'
    kwargs['suptitle'] = 'Import file'
    kwargs['button'] = 'Upload'
    kwargs['previous'] = conf.get_absolute_url()

    return render(request, 'rc_import.html', kwargs)


def plot_pulses(request, conf_id):

    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    km = True if 'km' in request.GET else False

    script, div = conf.plot_pulses(km=km)

    kwargs = {}
    kwargs['no_sidebar'] = True
    kwargs['title'] = 'RC Pulses'
    kwargs['suptitle'] = conf.name
    kwargs['div'] = mark_safe(div)
    kwargs['script'] = mark_safe(script)
    kwargs['units'] = conf.km2unit
    kwargs['kms'] = 1/conf.km2unit

    if km:
        kwargs['km_selected'] = True

    if 'json' in request.GET:
        return HttpResponse(json.dumps({'div':mark_safe(div), 'script':mark_safe(script)}), content_type="application/json")
    else:
        return render(request, 'rc_pulses.html', kwargs)

def plot_pulses2(request, conf_id):

    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    km = True if 'km' in request.GET else False

    script, div = conf.plot_pulses2(km=km)

    kwargs = {}
    kwargs['no_sidebar'] = True
    kwargs['title'] = 'RC Pulses'
    kwargs['suptitle'] = conf.name
    kwargs['div'] = mark_safe(div)
    kwargs['script'] = mark_safe(script)
    kwargs['units'] = conf.km2unit
    kwargs['kms'] = 1/conf.km2unit

    if km:
        kwargs['km_selected'] = True

    if 'json' in request.GET:
        return HttpResponse(json.dumps({'div':mark_safe(div), 'script':mark_safe(script)}), content_type="application/json")
    else:
        return render(request, 'rc_pulses.html', kwargs)

def conf_raw(request, conf_id):
    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    raw = conf.write_device(raw=True)
    return HttpResponse(raw, content_type='application/json')