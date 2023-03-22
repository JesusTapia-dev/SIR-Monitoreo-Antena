from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template

from apps.main.models import Experiment
from .models import ATRADConfiguration, ATRADData

from .forms import ATRADConfigurationForm, UploadFileForm
from apps.main.views import sidebar

import requests
import json

import os
from django.http import JsonResponse
from .mqtt import client as mqtt_client
from radarsys.socketconfig import sio as sio
from datetime import timedelta
from datetime import datetime

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

def atrad_tx(request, id_conf, id_tx):
    kwargs = {}
    kwargs['id_tx'] = id_tx[-1]
    kwargs['title'] = 'Temperature Details'
    kwargs['button'] = 'Edit Configuration'
    try:
        time = ATRADData.objects.last().datetime
    except:
        time = datetime.now()
    
    id_stx = (int(id_tx[-1])-1)*4+1
    mydata = ATRADData.objects.filter(datetime__gte = (time-timedelta(hours=1)),nstx = id_stx).values('datetime',
    'temp1_1','temp2_1','temp3_1','temp4_1','temp5_1','temp6_1',
    'temp1_2','temp2_2','temp3_2','temp4_2','temp5_2','temp6_2',
    'temp1_3','temp2_3','temp3_3','temp4_3','temp5_3','temp6_3',
    'temp1_4','temp2_4','temp3_4','temp4_4','temp5_4','temp6_4',
    'combiner1','combiner2','combiner3','combiner4')
    kwargs['data'] = json.dumps(list(mydata),default=str)
    return render(request, 'atrad_tx.html', kwargs)

def QuerytoStr(data):
    time = data[0]
    strdata = str(time)
    return strdata

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

def publish_message(request):
    rc, mid = mqtt_client.publish('test/data2',1)
    return JsonResponse({'code1': 'HIKA', 'code2': 'LUCAS'})

def monitor(request):
    kwargs = {'no_sidebar': True}
    return render(request, 'monitor.html', kwargs)

def atrad_prueba(request):
    keys = ['id','temp1','temp2','temp3','temp4','temp5','temp6']
    time = ATRADData.objects.last().datetime
    mydata = ATRADData.objects.filter(datetime__gte = (time-timedelta(hours=1))).values('id','temp1_1','temp2_1','temp3_1','temp4_1','temp5_1','temp6_1',
    'temp1_2','temp2_2','temp3_2','temp4_2','temp5_2','temp6_2','temp1_3','temp2_3','temp3_3','temp4_3','temp5_3','temp6_3',
    'temp1_4','temp2_4','temp3_4','temp4_4','temp5_4','temp6_4')
    template = get_template('prueba.html')
    context = {
        'last' : time,
        'temps': mydata,
        'keys' : keys,
    }
    return HttpResponse(template.render(context, request))

@sio.on('connection-bind')
def atrad_connection_bind(sid, data):
    print("sid:",sid,"data",data)

@sio.on('disconnect')
def atrad_disconnect(sid):
    print("Disconnected")

@sio.event
def atrad_control_event(sid,message):
    mqtt_client.publish(os.environ.get('MQTT_TOPIC_ATRAD_CONTROL', 'atrad/test2'), json.dumps(message))