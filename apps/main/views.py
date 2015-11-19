from django.shortcuts import render,render_to_response
from django.template import RequestContext
from .forms import ExperimentForm, TemplatesForm

from .models import ExperimentTemplate, Device
# Create your views here.

def index(request, idtemplate=0):
    kwargs = {}
    if idtemplate not in (0, "0"):
        form = TemplatesForm(initial={'template':idtemplate})
        template = ExperimentTemplate.objects.get(id=idtemplate)
        devices = Device.objects.filter(configuration__experimentdetail__experiment=template.experiment_detail.experiment)
        kwargs['devices'] = devices        
    else:
        form = TemplatesForm()
    kwargs['form'] = form
    return render_to_response("index.html", kwargs, context_instance=RequestContext(request))

def new_experiment(request):
    kwargs = {}
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response("index.html", kwargs, context_instance=RequestContext(request))
    else:        
        form = ExperimentForm()
    kwargs['form'] = form
    return render_to_response("new_experiment.html", kwargs, context_instance=RequestContext(request))

def new_device(request):
    kwargs = {}

    return render_to_response("new_device.html", kwargs, context_instance=RequestContext(request))