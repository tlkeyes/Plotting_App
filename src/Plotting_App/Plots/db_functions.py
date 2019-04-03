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

def collect_source(facility):

    # COLLECT INITAL SOURCE DATA
    source = RawData.objects.filter(jarid=facility, process_outcome='Outcome', year__gte=2016)
    source = source.values('measure_name', 'unit_type', 'year', 'month', 'numerator', 'denominator')

    return source

def get_measure_names(data):
    measure_names = data.values_list('measure_name', flat=True).distinct()

    return measure_names

def create_rate_bounds(data):
    source = data

    # ESTABLISH BASELINE RATE (UHAT)
    u_hat = round((source.numerator[source['year']==2016].sum()/source.denominator[source['year']==2016].sum())*1000,10)
    
    # CREATE CUSTOM COLUMNS
    source['rate'] = round(source['numerator']/source['denominator']*1000,3)
    source['3upper'] = round(u_hat + 3*np.sqrt(u_hat/(source.denominator/1000)),3)
    source['2upper'] = round(u_hat + 2*np.sqrt(u_hat/(source.denominator/1000)),3)
    
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

    # INDEX DATA FRAME ON DATE
    overall = overall.set_index('date')

    return overall

def measure_rate(data, measure_name):

    # PASS SOURCE DATA INTO FUNCTION AND AGGREGATE
    measure = data.filter(measure_name=measure_name)
    measure = measure.values('date', 'year', 'month').annotate(numerator=Sum('numerator'), denominator=Sum('denominator'))

    # CONVERT TO DATA FRAME
    measure = DataFrame.from_records(measure)

    # CREATE DATE FIELD
    measure['day'] = 1
    measure['date'] = to_datetime(measure[['year', 'month', 'day']])

    # CREATE CUSTOM FIELDS
    measure = create_rate_bounds(data=measure)

    return measure