import numpy as np
from pandas import DataFrame, to_datetime
from bokeh.plotting import Figure
from bokeh.layouts import gridplot, layout, column, row
from bokeh.models import Panel, BoxAnnotation, Band, Span, ColumnDataSource, DataTable 
from bokeh.transform import jitter
from django.db.models import Sum

# IMPORT MODELS
from .models import RawMonthlyCurrent2 as RawData

# CREATE FUNCTIONS TO GATHER DATA

def collect_source(facility, measure_name):

    # COLLECT INITAL SOURCE DATA
    source = RawData.objects.filter(jarid=facility, measure_name=measure_name, process_outcome='Outcome', year__gte=2016)
    source = source.values('measure_name', 'unit_type', 'year', 'month', 'numerator', 'denominator')

    return source

def get_measure_names(data):
    measure_names = data.values_list('measure_name', flat=True).distinct()

    return measure_names

def get_unit_types(data):
    unit_types = data.values_list('unit_type', flat=True).distinct()

    return unit_types

def weird_division(numerator, denominator):
    result = np.divide(numerator, denominator, out=np.zeros_like(denominator), where=denominator!=0)

    return result

def create_rate_bounds(data):
    source = data

    # ESTABLISH BASELINE RATE (UHAT)
    u_hat = round((source.numerator[source['year']==2016].sum()/source.denominator[source['year']==2016].sum())*1000,10)
    
    # CREATE CUSTOM COLUMNS
    inner_term = weird_division(u_hat, source['denominator']/1000)
    source['rate'] = np.round(weird_division(source['numerator'], source['denominator'])*1000,4)
    source['3upper'] = np.round(u_hat + 3*np.sqrt(inner_term),4)
    source['2upper'] = np.round(u_hat + 2*np.sqrt(inner_term),4)
    
    return source

def overall_rate(data):

    # PASS SOURCE DATA INTO FUNCTION AND AGGREGATE
    overall = data.values('year', 'month').annotate(numerator=Sum('numerator'), denominator=Sum('denominator'))

    # CONVERT TO DATAFRAME
    overall = DataFrame.from_records(overall)

    # CREATE DATE FIELD
    overall['day'] = 1
    overall['date'] = to_datetime(overall[['year', 'month', 'day']])

    # CREATE CUSTOM RATE FIELDS
    overall = create_rate_bounds(data=overall)

    # ORDER DATA FRAME ON DATE
    overall = overall.sort_values(by=['date'])

    return overall

def unit_rate(data, unit_type):

    # PASS SOURCE DATA INTO FUNCTION AND AGGREGATE
    unit = data.filter(unit_type=unit_type)
    unit = unit.values('year', 'month', 'unit_type').annotate(numerator=Sum('numerator'), denominator=Sum('denominator'))

    # CONVERT TO DATA FRAME
    unit = DataFrame.from_records(unit)

    # CREATE CUSTOM FIELDS
    unit = create_rate_bounds(data=unit)

    unit = unit.sort_values(by=['year', 'month'])

    unit = {
        'rate': unit['rate']
    }

    return unit