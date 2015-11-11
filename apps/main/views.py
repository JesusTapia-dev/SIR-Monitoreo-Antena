from django.shortcuts import render,render_to_response
from django.template import RequestContext

# Create your views here.

def index(request):
    kwargs = {}
    return render_to_response("index.html", kwargs, context_instance=RequestContext(request))
