import json

from django.contrib import messages
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from apps.main.models import Configuration, Experiment, Device
from apps.main.views import sidebar

from .models import RCConfiguration, RCLine, RCLineType, RCLineCode
from .forms import RCConfigurationForm, RCLineForm, RCLineViewForm, RCLineEditForm, RCSubLineEditForm, RCImportForm
from .utils import RCFile, plot_pulses


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
    kwargs['dev_conf_keys'] = ['name', 'ipp', 'ntx', 'clock', 'clock_divider', 
                               'time_before', 'time_after', 'sync']
    
    kwargs['title'] = 'RC Configuration'
    kwargs['suptitle'] = 'Details'
    
    kwargs['button'] = 'Edit Configuration'
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf))
    
    return render(request, 'rc_conf.html', kwargs)


def conf_edit(request, conf_id):
    
    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    
    lines = RCLine.objects.filter(rc_configuration=conf).order_by('channel')
        
    for line in lines:
        line_type = get_object_or_404(RCLineType, pk=line.line_type.id)
        extra_fields = json.loads(line_type.params)
        params = json.loads(line.params)
        for item, values in extra_fields.items():
            if item=='params':
                continue              
            values['value'] = params[item]
        
        line.form = RCLineEditForm(initial={'rc_configuration':conf_id, 'line_type': line.line_type.id, 'line': line.id},
                                   extra_fields=extra_fields)
        
        if 'params' in params:
            line.subform = True
            line.subforms = [RCSubLineEditForm(extra_fields=fields, line=line.id, count=i) for i, fields in enumerate(params['params'])]
    
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
            elif label.count('|')==2:
                extras.append(label)
                continue 
            
            pk, name = label.split('|')
    
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
            for line in conf.get_lines():
                if line.line_type.name=='tr':
                    continue
                line.update_pulses()
            
            for tr in conf.get_lines('tr'):
                tr.update_pulses()
            
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
    kwargs['previous'] = conf.get_absolute_url()

    kwargs.update(sidebar(conf))
    
    return render(request, 'rc_conf_edit.html', kwargs)


def add_line(request, conf_id, line_type_id=None):
    
    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    
    if request.method=='GET':
        if line_type_id:
            line_type = get_object_or_404(RCLineType, pk=line_type_id)
            form = RCLineForm(initial={'rc_configuration':conf_id, 'line_type': line_type_id},
                              extra_fields=json.loads(line_type.params))
        else:
            form = RCLineForm(initial={'rc_configuration':conf_id})
        
    if request.method=='POST':
        line_type = get_object_or_404(RCLineType, pk=line_type_id)
        form = RCLineForm(request.POST, extra_fields=json.loads(line_type.params))
        
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
    
    kwargs.update(sidebar(conf))
    
    return render(request, 'rc_add_line.html', kwargs)

def add_subline(request, conf_id, line_id):
    
    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    line = get_object_or_404(RCLine, pk=line_id)
    
    if request.method == 'POST':
        if line:
            params = json.loads(line.params)
            if 'params' in params:
                subparams = json.loads(line.line_type.params)
                base = [p for p in subparams if p['name']=='params'][0]['form']
                new = {}
                for p in base:
                    new[p['name']] = p['value']
                params['params'].append(new)
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
    kwargs['delete_view'] = True
    kwargs['title'] = 'Confirm delete'
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
            line.form = RCLineViewForm(extra_fields=json.loads(line.params))
        
        html = render(request, 'rc_lines.html', {'rc_lines':lines, 'edit':True})
        data = {'html': html.content}
        
        return HttpResponse(json.dumps(data), content_type="application/json")
    return redirect('url_edit_rc_conf', conf.id)
    
def import_file(request, conf_id):
    
    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    if request.method=='POST':
        form = RCImportForm(request.POST, request.FILES)
        if form.is_valid():
            #try:
            if True:
                f = RCFile(request.FILES['file_name'])
                data = f.data
                conf.ipp = data['ipp']
                conf.ntx = data['ntx']
                conf.clock = data['clock']
                conf.clock_divider = data['clock_divider']
                conf.time_before = data['time_before']
                conf.time_after = data['time_after']
                conf.sync = data['sync']
                conf.save()                
                lines = []
                positions = {'tx':0, 'tr':0}                
                
                for i, line_data in enumerate(data['lines']):
                    line_type = RCLineType.objects.get(name=line_data.pop('type'))
                    if line_type.name=='codes':
                        code = RCLineCode.objects.get(name=line_data['code'])
                        line_data['code'] = code.pk
                    line = RCLine.objects.filter(rc_configuration=conf, channel=i)
                    if line:
                        line = line[0]
                        line.line_type = line_type
                        line.params = json.dumps(line_data)
                    else:
                        line = RCLine(rc_configuration=conf, line_type=line_type, 
                                      params=json.dumps(line_data),
                                      channel=i)                    
                    
                    if line_type.name=='tx':
                        line.position = positions['tx']
                        positions['tx'] += 1
                    
                    if line_type.name=='tr':
                        line.position = positions['tr']
                        positions['tr'] += 1
                        
                    line.save()
                    lines.append(line)
                    
                for line, line_data in zip(lines, data['lines']):
                    if 'TX_ref' in line_data:
                        params = json.loads(line.params)
                        params['TX_ref'] = [l.pk for l in lines if l.line_type.name=='tx' and l.get_name().replace(' ', '')==line_data['TX_ref']][0]
                        line.params = json.dumps(params)
                        line.save()                                
                     
                for line in conf.get_lines():
                    if line.line_type.name=='tr':
                        continue
                    line.update_pulses()
                
                for tr in conf.get_lines('tr'):
                    tr.update_pulses() 
                
                messages.success(request, 'Configuration "%s" loaded succesfully' % request.FILES['file_name'])
                return redirect(conf.get_absolute_url())
            
            #except Exception as e:    
            #    messages.error(request, 'Error parsing file: "%s" - %s' % (request.FILES['file_name'], e))
        
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


def view_pulses(request, conf_id):
    
    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    lines = RCLine.objects.filter(rc_configuration=conf)
    
    unit = (conf.clock/conf.clock_divider)*3./20
    
    N = int(conf.ipp*(conf.clock/conf.clock_divider)*20./3)*conf.ntx
        
    script, div = plot_pulses(unit, N, lines)
    
    kwargs = {'div':mark_safe(div), 'script':mark_safe(script)}
    
    if 'json' in request.GET:
    
        return HttpResponse(json.dumps(kwargs), content_type="application/json")
    
    else:
        
        
        
        return render(request, 'rc_pulses.html', kwargs)

