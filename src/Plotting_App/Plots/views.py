from django.shortcuts import render
from django.views.generic import TemplateView
from bokeh.models import Tabs
from bokeh.embed import components
from django.conf import settings

# IMPORT HELPER FUNCTIONS
from .helper_functions import collect_source_test, create_tabs_test

# IMPORT MISC
import pandas as pd
from django.shortcuts import render

# Create your views here.

def home_view(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'Plots/home.html', context)

def about_view(request):
    context = {
        'title': 'About'
    }
    return render(request, 'Plots/about.html', context)

def plot_view(request):
    source, measure_names = collect_source_test(facility='19284')
    context = {
        'measure_names': measure_names
    }
    return render(request, 'Plots/plot.html', context)

def sidenav_view(request):
    

def shards_view(request):
    context = {}
    return render(request, 'Plots/shards_example.html', context)

def plot_view_def_test(request):
    # COLLECT DATA
    source, measure_names = collect_source_test(facility='19284')
    #[entry for entry in source]

    info = create_tabs_test(source=source, measure_names=measure_names)
    tabs = list(info['panel'])
    tabs = Tabs(tabs=tabs)
    embed_div, embed_script = components(tabs)

    context= {
        "embed_div": embed_div,
        "embed_script": embed_script 
    }

    return render(request, 'Plots/plot.html', context)