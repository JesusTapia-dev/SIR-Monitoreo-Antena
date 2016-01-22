import json

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from apps.main.models import Configuration, Experiment

from .models import RCConfiguration, RCLine
from .forms import RCConfigurationForm, RCLineForm, RCLineViewForm


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
    experiments = Experiment.objects.filter(campaign=conf.experiment.campaign)
    configurations = Configuration.objects.filter(experiment=conf.experiment)
    
    exp_keys = ['id', 'campaign', 'name', 'start_time', 'end_time']
    conf_keys = ['id', 'device__name', 'device__device_type__name', 'device__ip_address']
    
    kwargs['experiment_keys'] = exp_keys[1:]
    kwargs['experiments'] = experiments.values(*exp_keys)
    
    kwargs['configuration_keys'] = conf_keys[1:]
    kwargs['configurations'] = configurations.values(*conf_keys)
    
    return render(request, 'rc_conf.html', kwargs)

    
def conf_edit(request, id):
    
    conf = get_object_or_404(RCConfiguration, pk=id)
    
    if request.method=='GET':
        form = RCConfigurationForm(instance=conf)
        
    if request.method=='POST':
        form = RCConfigurationForm(request.POST, instance=conf)
        
        if form.is_valid():
            form.save()
            return redirect('url_rc_conf', id=id)
          
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Edit'    
    kwargs['button'] = 'Update'
    kwargs['previous'] = conf.get_absolute_url()
    return render(request, 'rc_conf_edit.html', kwargs)


def add_line(request, id):
    
    conf = get_object_or_404(RCConfiguration, pk=id)
    
    if request.method=='GET':
        form = RCLineForm(initial={'rc_configuration':conf.id})
        
    if request.method=='POST':
        form = RCLineForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('url_rc_conf', id=id)
          
    kwargs = {}
    kwargs['form'] = form
    kwargs['title'] = 'RC Configuration'
    kwargs['suptitle'] = 'Add Line'
    kwargs['button'] = 'Add'
    kwargs['previous'] = conf.get_absolute_url()
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


def line_up(request, conf_id, line_id):
    
    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    line = get_object_or_404(RCLine, pk=line_id)
    
    if line:
        ch = line.channel
        if ch-1>=0:
            line0 = RCLine.objects.get(rc_configuration=conf, channel=ch-1)
            line0.channel = ch
            line0.save()
            line.channel = ch-1 
            line.save()            
    
    return redirect(conf.get_absolute_url())


def line_down(request, conf_id, line_id):
    
    conf = get_object_or_404(RCConfiguration, pk=conf_id)
    line = get_object_or_404(RCLine, pk=line_id)
        
    if line:
        ch = line.channel
        if ch+1<RCLine.objects.filter(rc_configuration=conf).count():
            line1 = RCLine.objects.get(rc_configuration=conf, channel=ch+1)
            line1.channel = ch
            line1.save()
            line.channel = ch+1 
            line.save()
                    
    return redirect(conf.get_absolute_url())

