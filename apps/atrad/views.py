from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from apps.main.models import Experiment
from .models import ATRADConfiguration

from .forms import ATRADConfigurationForm, UploadFileForm
from apps.main.views import sidebar

import requests
import json

import os
from django.http import JsonResponse
from .mqtt import client as mqtt_client
from radarsys.socketconfig import sio as sio


def atrad_conf(request, id_conf):

    conf = get_object_or_404(ATRADConfiguration, pk=id_conf)

    ip=conf.device.ip_address
    port=conf.device.port_address

    kwargs = {}

    kwargs['status'] = conf.device.get_status_display()

    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = ['label',
                               'topic']

    kwargs['title'] = 'ATRAD Configuration'
    kwargs['suptitle'] = 'Details'

    kwargs['button'] = 'Edit Configuration'

    #kwargs['no_play'] = True

    ###### SIDEBAR ######
    kwargs.update(sidebar(conf=conf))

    return render(request, 'atrad_conf.html', kwargs)

def atrad_conf_edit(request, id_conf):

    conf = get_object_or_404(ATRADConfiguration, pk=id_conf)

    if request.method=='GET':
        form = ATRADConfigurationForm(instance=conf)

    if request.method=='POST':
        form = ATRADConfigurationForm(request.POST, instance=conf)

        if form.is_valid():
            if conf.topic == None:  conf.topic = 0

            conf = form.save(commit=False)

            if conf.verify_frequencies():
                conf.save()
                return redirect('url_atrad_conf', id_conf=conf.id)

    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Edit'
    kwargs['button'] = 'Save'

    return render(request, 'atrad_conf_edit.html', kwargs)

import os
from django.http import HttpResponse#

def publish_message(request):
    rc, mid = mqtt_client.publish('test/data2',1)
    return JsonResponse({'code1': 'HIKA', 'code2': 'LUCAS'})

def monitor(request):
    kwargs = {'no_sidebar': True}
    return render(request, 'monitor.html', kwargs)

def prueba(request):
    kwargs = {'no_sidebar': True}
    return render(request, 'prueba.html', kwargs)

@sio.on('connection-bind')
def connection_bind(sid, data):
    print("sid:",sid,"data",data)

@sio.on('disconnect')
def test_disconnect(sid):
    print("Disconnected")

@sio.event
def control_event(sid,message):
    mqtt_client.publish('test/data2',message['data'])

def hello(data):
    try:
        rc, mid = mqtt_client.publish('test/data2', 'Hello')
        sio.emit('test', data={'topic':mid, 'status': 'Not Running'})
    except:
        print('ERROR', flush=True)
    return HttpResponse("Hello")