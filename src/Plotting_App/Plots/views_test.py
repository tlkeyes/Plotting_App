from django.shortcuts import render
from django.views.generic import TemplateView, View
from bokeh.models import Tabs
from bokeh.embed import components
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from rest_framework.views import APIView
from rest_framework.response import Response

# IMPORT HELPER FUNCTIONS
from .db_functions import collect_source, overall_rate, get_measure_names, measure_rate

# IMPORT MISC
import pandas as pd
from django.shortcuts import render

class TestApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        RETURN A DICTIONARY OF DATA
        """
        source = collect_source(facility=19284)
        measure_names = get_measure_names(data=source)

        overall = overall_rate(data=source)
        measure_data = {}

        for name in measure_names:
            measure_data[name] = measure_rate(data=source, measure_name=name)
        
        plot_data = {
            'overall': overall,
            'measure_data': measure_data
        }

        return plot_data


