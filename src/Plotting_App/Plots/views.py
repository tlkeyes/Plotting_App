from django.shortcuts import render
from django.views.generic import TemplateView, View
from bokeh.models import Tabs
from bokeh.embed import components
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

# IMPORT HELPER FUNCTIONS
from .helper_functions import collect_source_test, create_tabs_test

# IMPORT MISC
import pandas as pd
from django.shortcuts import render

# Create your views here.

def plot_view(request):
    source, measure_names = collect_source_test(facility='19284')
    context = {
        'measure_names': measure_names
    }
    return render(request, 'Plots/plot.html', context)

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

# Views for shard template

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Plots/base.html', {"customers": 10})

class ShardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Plots/shards_example.html', {})

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        Return a dictionary of data.
        """
        source, measure_names = collect_source_test(facility='19284')
        context = {
            'measure_names': measure_names,
            'date': source['date'],
            'rate': source['rate']
        }
        return Response(context)