import numpy as np
from pandas import DataFrame, to_datetime
from bokeh.plotting import Figure
from bokeh.layouts import gridplot, layout, column, row
from bokeh.models import Panel, BoxAnnotation, Band, Span, ColumnDataSource, DataTable 
from bokeh.transform import jitter
from django.db.models import Sum

# IMPORT MODELS
from .models import RawMonthlyCurrent2 as RawData

# # CREATE FUNCTIONS TO GATHER DATA

def df_collect_source(facility, measure_name):

    # COLLECT INITAL SOURCE DATA
    source = RawData.objects.filter(jarid=facility, measure_name=measure_name, process_outcome='Outcome', year__gte=2016)
    source = source.values('measure_name', 'unit_type', 'year', 'month', 'numerator', 'denominator')

    source = DataFrame.from_records(source)
    source['day'] = 1
    source['date'] = to_datetime(source[['year', 'month', 'day']])

    source.drop(['day', 'month','year'], axis=1)

    return source

def df_weird_division(numerator, denominator):
    out = np.divide(numerator, denominator, out=np.zeros_like(denominator), where=denominator!=0)

    return out

def df_rate_bounds_calculation(data):
    source = data

    # ESTABLISH BASELINE RATE (UHAT)
    u_hat = round((source.numerator[source.index.year == 2016].sum()/source.denominator[source.index.year == 2016].sum())*1000,10)
    
    # CREATE CUSTOM COLUMNS
    inner_term = df_weird_division(u_hat, source['denominator']/1000)
    source['rate'] = np.round(df_weird_division(source['numerator'], source['denominator'])*1000,4)
    source['3upper'] = np.round(u_hat + 3*np.sqrt(inner_term),4)
    source['2upper'] = np.round(u_hat + 2*np.sqrt(inner_term),4)

    source.drop(['numerator', 'denominator'], axis=1)
    
    return source

def df_create_rate_bounds(source_df):
    
    bounds = source_df.groupby(['measure_name','date'])['numerator', 'denominator'].sum().reset_index()
    bounds = bounds.set_index(['date'])

    bounds = df_rate_bounds_calculation(bounds)

    return bounds

def df_unit_type(source_df):
    unit = source_df.groupby(['measure_name', 'unit_type', 'date'])['numerator', 'denominator'].sum().reset_index()

    unit = unit.set_index(['unit_type']).sort_index()

    return unit

def df_overall_rate(source_df):
    overall = source_df.groupby(['measure_name'])['numerator','denominator'].sum()
    overall['rate'] = np.round(df_weird_division(overall['numerator'], overall['denominator'])*1000,3)

    return overall

def df_unit_rate(source_df, unit_type):
    
    unit = source_df.loc[(unit_type)].copy()
    unit['rate'] = np.round(df_weird_division(unit['numerator'], unit['denominator'])*1000, 3)
    overall = df_overall_rate(unit)

    unit = unit.reset_index()
    unit = unit.drop(['measure_name', 'unit_type', 'date'], axis=1)

    unit = {
        'overall': overall,
        'rate': unit['rate']
    }

    return unit
