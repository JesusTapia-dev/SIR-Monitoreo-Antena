import json

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from apps.main.models import Configuration, Experiment
from apps.main.views import sidebar

from .models import RCConfiguration, RCLine, RCLineType
from .forms import RCConfigurationForm, RCLineForm, RCLineViewForm, RCLineEditForm


def conf(request, id):

    conf = get_object_or_404(RCConfiguration, pk=id)
    
    lines = RCLine.objects.filter(rc_configuration=conf).order_by('channel')
    
    for line in lines:
        line.form = RCLineViewForm(extra_fields=json.loads(line.params))
    
    kwargs = {}
    kwargs['dev_conf'] = conf
    kwargs['rc_lines'] = lines
    kwargs['dev_conf_keys'] = ['clock', 'ipp', 'ntx','clock_divider']
    
    kwargs['title'] = 'RC Configuration'
    kwargs['suptitle'] = 'Details'
    
    kwargs['button'] = 'Edit Configuration'
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf))
    
    return render(request, 'rc_conf.html', kwargs)

    
def conf_edit(request, id):
    
    conf = get_object_or_404(RCConfiguration, pk=id)
    
    if request.method=='GET':
        form = RCConfigurationForm(instance=conf)
        
    if request.method=='POST':
        form = RCConfigurationForm(request.POST, instance=conf)
        
        if form.is_valid():
            form.save()
            return redirect('url_dev_conf', id=id)
          
    kwargs = {}
    kwargs['dev_conf'] = conf
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
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
            return redirect(conf.get_absolute_url())
          
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'RC Configuration'
    kwargs['suptitle'] = 'Add Line'
    kwargs['button'] = 'Add'
    kwargs['previous'] = conf.get_absolute_url()
    kwargs['dev_conf'] = conf
    
    kwargs.update(sidebar(conf))
    
    return render(request, 'rc_add_line.html', kwargs)


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

        return redirect(conf.get_absolute_url())
            
    kwargs = {}
    
    kwargs['object'] = line
    kwargs['delete_view'] = True
    kwargs['title'] = 'Confirm delete'
    kwargs['previous'] = conf.get_absolute_url()
    return render(request, 'confirm.html', kwargs)


def edit_lines(request, conf_id):
    
    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    
    if request.method=='GET':         
        lines = RCLine.objects.filter(rc_configuration=conf).order_by('channel')
        for line in lines:
            line_type = get_object_or_404(RCLineType, pk=line.line_type.id)
            extra_fields = json.loads(line_type.params)
            for item in extra_fields:
                params = json.loads(line.params)
                item['value'] = params[item['name']]
            line.form = RCLineEditForm(initial={'rc_configuration':conf_id, 'line_type': line.line_type.id, 'line': line.id},
                                   extra_fields=extra_fields)
    
    elif request.method=='POST':
        data = {}
        for label,value in request.POST.items():
            if '|' not in label:
                continue
            id, name = label.split('|')
            if id in data:
                data[id][name]=value
            else:
                data[id] = {name:value}
                
        for id, params in data.items():
            line = RCLine.objects.get(pk=id)
            line.params = json.dumps(params)
            line.save()    
        
        return redirect(conf.get_absolute_url())    
    
    kwargs = {}
    kwargs['dev_conf'] = conf
    kwargs['rc_lines'] = lines
    kwargs['edit'] = True
    
    kwargs['title'] = 'RC Configuration'
    kwargs['suptitle'] = 'Edit Lines'    
    kwargs['button'] = 'Update'
    kwargs['previous'] = conf.get_absolute_url()

    
    kwargs.update(sidebar(conf))
    
    return render(request, 'rc_edit_lines.html', kwargs)
    

def update_lines(request, conf_id):
    
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
        
        html = render(request, 'rc_lines.html', {'rc_lines':lines})
        data = {'html': html.content}
        
        return HttpResponse(json.dumps(data), content_type="application/json")
    return redirect(conf.get_absolute_url())
    


