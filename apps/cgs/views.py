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

    #if request.method=='GET':
        #r: response = icon, status
    #    try:
    #        route = "http://" + str(ip) + ":" + str(port) + "/status/ad9548"
    #        r = requests.get(route)
    #        response = str(r.text)
    #        response = response.split(";")
    #        icon = response[0]
    #        status = response[-1]
            #print r.text
            #"icon" could be: "alert" or "okay"
            # Si hay alerta pero esta conectado
    #        if "alert" in icon:
    #            if "Starting Up" in status: #No Esta conectado
    #                kwargs['connected'] = False
    #            else:
    #                kwargs['connected'] = True
    #        elif "okay" in icon:
    #            kwargs['connected'] = True
    #        else:
    #            kwargs['connected'] = False

    #    except:
    #        kwargs['connected'] = False
    #        status = "The Device is not connected."

    #if not kwargs['connected']:
    #    messages.error(request, message=status)

    kwargs['dev_conf'] = conf
    kwargs['dev_conf_keys'] = ['name',
                               'freq0', 'freq1',
                               'freq2', 'freq3']

    kwargs['title'] = 'CGS Configuration'
    kwargs['suptitle'] = 'Details'

    kwargs['button'] = 'Edit Configuration'

    kwargs['no_play'] = True

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
#
# def cgs_conf_write(request, id_conf):
#
#     conf = get_object_or_404(CGSConfiguration, pk=id_conf)
#     ip=conf.device.ip_address
#     port=conf.device.port_address
#
#     #Frequencies from form
#     f0 = conf.freq0
#     f1 = conf.freq1
#     f2 = conf.freq2
#     f3 = conf.freq3
#
#     try:
#         post_data = {"f0":f0, "f1":f1, "f2":f2, "f3":f3}
#         route = "http://" + str(ip) + ":" + str(port) + "/frequencies/"
#         r = requests.post(route, post_data)
#         text = r.text
#         text = text.split(',')
#
#         try:
#             if len(text)>1:
#                 title = text[0]
#                 status = text[1]
#                 status_ok = r.status_code
#                 if title == "okay":
#                     messages.success(request, status)
#                 else:
#                     messages.error(request, status)
#
#             else:
#                 title = text[0]
#                 messages.error(request, title)
#
#         except:
#             messages.error(request, "An hardware error was found.")
#
#     except:
#         messages.error(request, "Could not write parameters.")
#
#
#
#
#     return redirect('url_cgs_conf', id_conf=conf.id)
#
# def cgs_conf_read(request, id_conf):
#
#     conf = get_object_or_404(CGSConfiguration, pk=id_conf)
#
#     ip=conf.device.ip_address
#     port=conf.device.port_address
#
#     if request.method=='POST':
#         form = CGSConfigurationForm(request.POST, instance=conf)
#
#         if form.is_valid():
#             cgs_model = form.save(commit=False)
#
#             if cgs_model.verify_frequencies():
#
#                 cgs_model.save()
#                 return redirect('url_cgs_conf', id_conf=conf.id)
#
#         messages.error(request, "Parameters could not be saved. Invalid parameters")
#
#         data = {}
#
#
#     if request.method=='GET':
#         #r: response = icon, status
#         route = "http://" + str(ip) + ":" + str(port) + "/status/ad9548"
#         try:
#             r = requests.get(route)
#             response = str(r.text)
#             response = response.split(";")
#             icon = response[0]
#             status = response[-1]
#             print r.text
#             #"icon" could be: "alert" or "okay"
#             if  "okay" in icon:
#                 messages.success(request, status)
#             else:
#                 messages.error(request, status)
#             #Get Frequencies
#             route = "http://" + str(ip) + ":" + str(port) + "/frequencies/"
#             #frequencies = requests.get('http://10.10.10.175:8080/frequencies/')
#             frequencies = requests.get(route)
#             frequencies = frequencies.json()
#             frequencies = frequencies.get("Frecuencias")
#             f0 = frequencies.get("f0")
#             f1 = frequencies.get("f1")
#             f2 = frequencies.get("f2")
#             f3 = frequencies.get("f3")
#             print f0,f1,f2,f3
#
#
#             if not response:
#                 messages.error(request, "Could not read parameters from Device")
#                 return redirect('url_cgs_conf', id_conf=conf.id)
#
#             data = {'experiment' : conf.experiment.id,
#                     'device' : conf.device.id,
#                     'freq0' : f0,
#                     'freq1' : f1,
#                     'freq2' : f2,
#                     'freq3' : f3,
#                     }
#         except:
#             messages.error(request, "Could not read parameters from Device")
#             data = {'experiment' : conf.experiment.id,
#                     'device' : conf.device.id,
#                     'freq0' : None,
#                     'freq1' : None,
#                     'freq2' : None,
#                     'freq3' : None,
#                     }
#             return redirect('url_cgs_conf', id_conf=conf.id)
#
#         form = CGSConfigurationForm(initial = data)
#
#     kwargs = {}
#     kwargs['id_dev'] = conf.id
#     kwargs['form'] = form
#     kwargs['title'] = 'Device Configuration'
#     kwargs['suptitle'] = 'Parameters read from device'
#     kwargs['button'] = 'Save'
#
#     ###### SIDEBAR ######
#     kwargs.update(sidebar(conf))
#
#     return render(request, 'cgs_conf_edit.html', kwargs)
#
# def cgs_conf_import(request, id_conf):
#
#     conf = get_object_or_404(CGSConfiguration, pk=id_conf)
#
#     if request.method == 'POST':
#         file_form = UploadFileForm(request.POST, request.FILES)
#
#         if file_form.is_valid():
#
#             try:
#                 if conf.update_from_file(request.FILES['file']):
#
#                     try:
#                         conf.full_clean()
#                     except ValidationError as e:
#                         messages.error(request, e)
#                     else:
#                         conf.save()
#
#                         messages.success(request, "Parameters imported from file: '%s'." %request.FILES['file'].name)
#                         #messages.warning(request,"")
#                         return redirect('url_cgs_conf', id_conf=conf.id)
#             except:
#                 messages.error(request, "No JSON object could be decoded.")
#
#         messages.error(request, "Could not import parameters from file")
#
#     else:
#         file_form = UploadFileForm(initial={'title': '.json'})
#
#
#     kwargs = {}
#     kwargs['id_dev'] = conf.id
#     kwargs['title'] = 'Device Configuration'
#     kwargs['form'] = file_form
#     kwargs['suptitle'] = 'Importing file'
#     kwargs['button'] = 'Import'
#
#     kwargs.update(sidebar(conf))
#
#     return render(request, 'cgs_conf_import.html', kwargs)
#
# def handle_uploaded_file(f):
#
#     data = {'freq0' : 62500000,
#             'freq1' : 62500000,
#             'freq2' : 62500000,
#             'freq3' : 62500000,
#             }
#
#     return data
#
# def cgs_conf_export(request, id_conf):
#
#     conf = get_object_or_404(CGSConfiguration, pk=id_conf)
#     ip=conf.device.ip_address
#     port=conf.device.port_address
#
#     #if request.method=='GET':
#     #    data = {"Frequencies": [
#     #                ["freq0", conf.freq0],
#     #                ["freq1", conf.freq1],
#     #                ["freq2", conf.freq2],
#     #                ["freq3", conf.freq3]
#     #           ]}
#     #    json_data = json.dumps(data)
#     #    conf.parameters = json_data
#     #    response = HttpResponse(conf.parameters, content_type="application/json")
#     #    response['Content-Disposition'] = 'attachment; filename="data.json"'
#
#     #    return response
#
#     kwargs = {}
#     kwargs['dev_conf'] = conf
#     kwargs['dev_conf_keys'] = ['experiment', 'device',
#                                'freq0', 'freq1',
#                                'freq2', 'freq3']
#
#     kwargs['title'] = 'CGS Configuration'
#     kwargs['suptitle'] = 'Details'
#
#     kwargs['button'] = 'Edit Configuration'
#
#     ###### SIDEBAR ######
#     kwargs.update(sidebar(conf))
#     return render(request, 'cgs_conf.html', kwargs)
