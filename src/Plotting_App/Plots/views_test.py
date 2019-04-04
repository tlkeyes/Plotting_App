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
from .db_functions import collect_source, overall_rate, get_unit_types, unit_rate, df_collect_source, df_overall, df_unit_type, df_unit_rate

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
        source = collect_source(facility=19284, measure_name='Cauti')
        unit_types = get_unit_types(data=source)

        overall = overall_rate(data=source)
        
        # CREATE MEASURE DATA DICTIONARY
        unit_data = {}

        for item in unit_types:
            unit_data[item] = unit_rate(data=source, unit_type=item)
        
        plot_data = {
            'date': overall['date'],
            'overall': {
                'rate': overall['rate'],
                'warning': overall['2upper'],
                'upper': overall['3upper']
            },
            'unit_data': unit_data
        }

        return Response(plot_data)

class TestApiViewDf(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        RETURN A DICTIONARY OF DATA
        """
        source = df_collect_source(facility=19284, measure_name='Cauti')

        overall = df_overall(source_df=source)

        unit = df_unit_type(source_df=source)

        unit_data = {}

        for item in unit.index.unique(level='unit_type'):
            unit_data[item] = df_unit_rate(unit, item)

        plot_data = {
            'date': overall.index,
            'overall': {
                'rate': overall['rate'],
                'warning': overall['2upper'], 
                'upper': overall['3upper']
            },
            'unit_data': unit_data
        }

        return Response(plot_data)



