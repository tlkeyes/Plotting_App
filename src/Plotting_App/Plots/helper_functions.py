import numpy as np
from pandas import DataFrame, to_datetime
from bokeh.plotting import Figure
from bokeh.layouts import gridplot, layout, column, row
from bokeh.models import Panel, BoxAnnotation, Band, Span, ColumnDataSource, DataTable 
from bokeh.transform import jitter
from django.db.models import Sum

# IMPORT MODELS
from .models import RawMonthlyCurrent2 as RawData


#   BELOW ARE THE TEST FUNTCIONS FOR COLLECTING THE DATA
def collect_source_test(facility):
    source = RawData.objects.filter(jarid=facility, year__gte=2016)
    source = source.filter(process_outcome='Outcome', measure_name__in=['Clabsi'])
    source = source.values('measure_name', 'year', 'month').annotate(numerator=Sum('numerator'), denominator=Sum('denominator'))

    measure_names = source.values_list('measure_name', flat=True).distinct()

    #   CONVERT TO DATAFRAME
    source = DataFrame.from_records(source)
    
    #   ADD CUSTOM COLUMNS
    source['day'] = 1
    source['date'] = to_datetime(source[['year', 'month', 'day']])
    source['rate'] = round(source['numerator']/source['denominator']*1000,7)

    #   INDEX DATAFRAME
    source = source.set_index('measure_name').sort_values(by=['year','month'])

    return source, measure_names

#   BELOW ARE THE TEST FUNTCIONS FOR CREATING PLOT DATA

#   BELOW ARE THE TEST FUNCTIONS FOR CREATING THE TABS FOR BOKEH

def create_tabs_test(source, measure_names):
    tab_data = {
        'panel': []
    }

    for i in measure_names:
        # Import Data
        view_id = []
        view_id = source.loc[i].copy()  

        # U Chart Data
        u_hat = (view_id.numerator[view_id['year']==2016].sum()/view_id.denominator[view_id['year']==2016].sum())*1000
        view_id['3lower'] = u_hat - 3*np.sqrt(u_hat/(view_id.denominator/1000))
        view_id['3upper'] = u_hat + 3*np.sqrt(u_hat/(view_id.denominator/1000))
        view_id['2lower'] = u_hat - 2*np.sqrt(u_hat/(view_id.denominator/1000))
        view_id['2upper'] = u_hat + 2*np.sqrt(u_hat/(view_id.denominator/1000))

        # Create histogram data
        hist, edges = np.histogram(view_id['numerator'], density=True, bins=20)

        # Plot Templates
        f1 = Figure(title='Scatterplot for '+str(i)+' Data', 
                    plot_width=600, plot_height=350, toolbar_location=None)
        f1.scatter(source = view_id, x = 'numerator', y = 'denominator', 
                    marker='hex', size=8 ,fill_alpha=0.3)
        f2 = Figure(title='Histogram for '+str(i)+' Data', 
                    plot_width=600, plot_height=350, toolbar_location=None)
        f2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
            fill_color="navy", line_color="white", alpha=0.5)
        f3 = Figure(title='U-Chart for '+str(i)+' Data', x_axis_type='datetime', 
                    plot_width=1200, plot_height=350, toolbar_location=None)
        f3.line(source=view_id, x='date', y='rate',
                line_width=2)
        baseline_rate = Span(location=u_hat, dimension='width', line_color='grey', line_dash='dashed', line_width=2)
        f3.add_layout(baseline_rate)
        band_3 = Band(source=ColumnDataSource(view_id), 
                    base='date', lower='3upper', upper=10, level='underlay', 
                    line_color='black', line_dash='dashed', line_width=1.5,
                    fill_color='red', fill_alpha=0.3)
        band_2 = Band(source=ColumnDataSource(view_id), 
                    base='date', lower='2upper', upper='3upper', level='underlay', 
                    line_color='black', line_dash='dashed', line_width=1.5, 
                    fill_alpha=0.3)
        f3.add_layout(band_3)
        f3.add_layout(band_2)

        #l = gridplot([f1,f2,f3], ncols=3, plot_height=400, plot_width=450, toolbar_location=None)
        l = column(row(f1,f2),row(f3))
        tab_data['panel'].append(Panel(child=l, title=i))

    return tab_data
