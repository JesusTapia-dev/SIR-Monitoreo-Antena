from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from apps.main.models import Experiment, Configuration
from .models import CGSConfiguration

from .forms import CGSConfigurationForm
from apps.main.views import sidebar

import requests
# Create your views here.

def cgs_conf(request, id_conf):
    
    conf = get_object_or_404(CGSConfiguration, pk=id_conf)
    
    ip=conf.device.ip_address
    port=conf.device.port_address
    
    kwargs = {}
    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = ['experiment', 'device',
                               'freq0', 'freq1',
                               'freq2', 'freq3']
    
    kwargs['title'] = 'CGS Configuration'
    kwargs['suptitle'] = 'Details'
    
    kwargs['button'] = 'Edit Configuration'
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf))
    
    return render(request, 'cgs_conf.html', kwargs)

def cgs_conf_edit(request, id_conf):
    
    conf = get_object_or_404(CGSConfiguration, pk=id_conf)
    
    if request.method=='GET':
        form = CGSConfigurationForm(instance=conf)
        
    if request.method=='POST':
        form = CGSConfigurationForm(request.POST, instance=conf)
        
        if form.is_valid():
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
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf))
    
    return render(request, 'cgs_conf_edit.html', kwargs)

def cgs_conf_write(request, id_conf):
    
    conf = get_object_or_404(CGSConfiguration, pk=id_conf)
    ip=conf.device.ip_address
    port=conf.device.port_address
    
    #Frequencies from form
    f0 = conf.freq0
    f1 = conf.freq1
    f2 = conf.freq2
    f3 = conf.freq3
    headers = {'User-Agent': 'Mozilla/5.0'}
    post_data = {"f0":f0, "f1":f1, "f2":f2, "f3":f3}
    route = "http://" + str(ip) + ":" + str(port) + "/frequencies/"
    session = requests.session()
    
    r = session.post(route, data= post_data,headers= headers)
    print r.url
    print r.text
    
    
    
    
    return redirect('url_cgs_conf', id_conf=conf.id)

def cgs_conf_read(request, id_conf):
    
    conf = get_object_or_404(CGSConfiguration, pk=id_conf)
    ip=conf.device.ip_address
    port=conf.device.port_address
    
    if request.method=='POST':
        form = CGSConfigurationForm(request.POST, instance=conf)
        
        if form.is_valid():
            cgs_model = form.save(commit=False)
            
            if cgs_model.verify_frequencies():
                
                cgs_model.save()
                return redirect('url_cgs_conf', id_conf=conf.id)
        
        messages.error(request, "Parameters could not be saved. Invalid parameters")
        
        data = {}
    
    
    if request.method=='GET':
        #r: response = icon, status
        route = "http://" + str(ip) + ":" + str(port) + "/status/ad9548"
        r = requests.get(route)
        response = str(r.text)
        response = response.split(";")
        icon = response[0]
        status = response[-1] 
        #"icon" could be: "alert" or "okay"
        if  "okay" in icon:
            messages.success(request, status)
        else:
            messages.error(request, status)
        #Get Frequencies
        frequencies = requests.get('http://10.10.10.175:8080/frequencies/')
        frequencies = frequencies.json()
        frequencies = frequencies.get("Frecuencias")
        f0 = frequencies.get("f0")
        f1 = frequencies.get("f1")
        f2 = frequencies.get("f2")
        f3 = frequencies.get("f3")
        print f0,f1,f2,f3
            
        if not response:
            messages.error(request, "Could not read parameters from Device")
            return redirect('url_cgs_conf', id_conf=conf.id)

        data = {'experiment' : conf.experiment.id,
                'device' : conf.device.id,
                'freq0' : f0,
                'freq1' : f1,
                'freq2' : f2,
                'freq3' : f3,
                }
    
        form = CGSConfigurationForm(initial = data)
    
    kwargs = {}
    kwargs['id_dev'] = conf.id
    kwargs['form'] = form
    kwargs['title'] = 'Device Configuration'
    kwargs['suptitle'] = 'Parameters read from device'
    kwargs['button'] = 'Save'
    
    ###### SIDEBAR ######
    kwargs.update(sidebar(conf))
    
    return render(request, 'cgs_conf_edit.html', kwargs)