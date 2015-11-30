from django.shortcuts import render, render_to_response
from django.template import RequestContext

from .forms import CGSConfigurationForm

# Create your views here.

def configurate_frequencies(request):
    kwargs = {}
    form = CGSConfigurationForm()

    data = {
        'form': form,
        'title': ('YAP'),
    }

    return render_to_response('index_cgs.html', data, context_instance=RequestContext(request))
    #return render_to_response("index.html", kwargs, context_instance=RequestContext(request))
    #return_to_response('index.html', {'title': 'Configura','form': form}, context_instance=RequestContext(request))



