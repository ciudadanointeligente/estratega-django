from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from django.views import generic

from .models import Estrategia


# index view (http://site/)
def index(request):
    return render(request, 'estratega/index.html', {})


# the first view after login
class MisEstrategiasView(generic.ListView):
    model = Estrategia
    template_name='estrategias/mis_estrategias.html'


# the first view when user clicks on a strategy
class EstrategiaView(generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/estrategia.html'

