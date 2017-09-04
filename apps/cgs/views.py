from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from apps.main.models import Experiment
from .models import CGSConfiguration

from .forms import CGSConfigurationForm, UploadFileForm
from apps.main.views import sidebar

import requests
import json
#from __builtin__ import None
# Create your views here.

def cgs_conf(request, id_conf):

    conf = get_object_or_404(CGSConfiguration, pk=id_conf)

    ip=conf.device.ip_address
    port=conf.device.port_address

    kwargs = {}

    kwargs['status'] = conf.device.get_status_display()

    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = ['name',
                               'freq0', 'freq1',
                               'freq2', 'freq3']

    kwargs['title'] = 'CGS Configuration'
    kwargs['suptitle'] = 'Details'

    kwargs['button'] = 'Edit Configuration'

    #kwargs['no_play'] = True

    ###### SIDEBAR ######
    kwargs.update(sidebar(conf=conf))

    return render(request, 'cgs_conf.html', kwargs)

def cgs_conf_edit(request, id_conf):

    conf = get_object_or_404(CGSConfiguration, pk=id_conf)

    if request.method=='GET':
        form = CGSConfigurationForm(instance=conf)

    if request.method=='POST':
        form = CGSConfigurationForm(request.POST, instance=conf)

        if form.is_valid():
            if conf.freq0 == None:  conf.freq0 = 0
            if conf.freq1 == None:  conf.freq1 = 0
            if conf.freq2 == None:  conf.freq2 = 0
            if conf.freq3 == None:  conf.freq3 = 0

            conf = form.save(commit=False)

            if conf.verify_frequencies():
                conf.save()
                return redirect('url_cgs_conf', id_conf=conf.id)

            ##ERRORS

    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Save'

    return render(request, 'cgs_conf_edit.html', kwargs)
