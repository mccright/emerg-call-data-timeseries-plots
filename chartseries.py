"""
This code started with "Light timeseries charts"  
By Fabio Arciniegas. Original downloaded from: 
https://github.com/fabioarciniegas/light_timeseries_charts/tree/master  

Plot diagrams using arbitrary time series data of the form:

"incident_date","response_unit","dispatch_time","time_in_service"
"01/01/10","M5","07:05:17","00:04:56"
"01/01/10","WAVE1","06:51:33","00:20:10"
"01/01/10","WAVE12","06:51:33","01:26:48"
"01/01/10","GRE310","07:56:42","00:06:56"
"01/01/10","WAVE1","07:56:42","00:11:42"
"01/01/10","WAVE11","08:05:59","00:59:47"
"01/01/10","MWM31","09:51:58","02:08:33"
"01/01/10","PLEA1","09:51:58","00:40:12"
"01/01/10","PLEA2","09:51:58","00:40:17"
"01/01/10","SE1","15:48:32","00:20:35"
"01/01/10","SE11","15:48:32","00:20:06"
"01/01/10","SE12","15:58:26","00:33:07"
"01/01/10","B1","20:22:57","00:00:05"
"01/02/10","8707","02:02:55","02:48:52"
"01/02/10","CERE1","01:41:51","02:58:42"
"01/02/10","RAYM1","01:46:16","01:52:36"
"01/02/10","WAVE1","01:46:16","01:07:18"
"01/02/10","SW1","16:33:09","00:26:58"

This was assembled to consolidate some of the Lincoln County, Nebraska emergency service response data into simple time series charts.  

The data is contained in a csv file, generating a single png output.

Normally response_unit is the name of a given team, dispatch_time is when they received a call for service and time_in_service is the amount of time a given response_unit spent on that given service.

"""
import argparse
import sys
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series
from pandas.plotting import register_matplotlib_converters
import itertools
from math import ceil
 
def setup_plot_style():
    register_matplotlib_converters()
    plt.rcParams.update(plt.rcParamsDefault)
    plt.style.use('ggplot')
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 8
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 9
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 8

def trend_line_and_x(l):
    # fit polynomial of degree 1 :)
    x = [i for i in range(len(l))]
    f = np.polyfit(x, l, 1)
    return np.poly1d(f), x
    
if __name__ == "__main__":
     parser = argparse.ArgumentParser(description="Plot a series of chart from timeseries data")
     parser.add_argument("--cols",type=int,default=2,
                         help="number image columns (2 by default)")
     parser.add_argument("--response_unit",type=str, default="response_unit",
                         help="title of response_unit column (e.g. tool)")
     parser.add_argument("--subcategory",type=str, default="response_unit",
                         help="title of response_unit column (e.g. tool)")
     parser.add_argument("--incident_date",type=str, default="incident_date",
                         help="title of incident_date column (e.g. datetime). String must be convertible by pandas.to_datetime")
     parser.add_argument("--time_in_service",type=str, default="time_in_service",
                         help="title of time_in_service column (e.g. numeric_reading).")

     parser.add_argument("infile",type=argparse.FileType("r"),nargs="?",default=sys.stdin,
                         help="read input from provided csv file (stdin by default)")
     parser.add_argument("outfile",
                         help="save result as csv in provided file (stdout by default)")
     setup_plot_style()
     args = parser.parse_args()
     df = pd.read_csv(args.infile)
     # TODO: allow for no-headers input
     response_unit = args.response_unit
     sub = args.subcategory
     time_in_service = args.time_in_service
     incident_date = args.incident_date     
     df.set_index([response_unit,sub],inplace=True)
     df.sort_values(incident_date,inplace=True)

     fig = plt.figure(1)
     s_i = 1
     rows = ceil(len(np.unique(df.index.get_level_values(response_unit)))/args.cols)
     for t in np.unique(df.index.get_level_values(response_unit)):
         plt.subplot(rows,args.cols,s_i)
         plt.title(t, fontsize=12)
         plt.xticks(rotation=10)
         for m in np.unique(df.loc[t,:].index.get_level_values(sub)):
            data = df.loc[t,m]
            data[incident_date] = pd.to_datetime(data[incident_date])
            plt.plot(data[incident_date].tolist(),data[time_in_service].tolist())
         plt.legend(np.unique(df.loc[t,:].index.get_level_values(sub)))
         s_i +=1
     plt.subplots_adjust(top=.90, bottom=0.08, left=0.10, right=0.95, hspace=.43,wspace=0.35)
     plt.gcf().set_size_inches(16,9)
     plt.savefig(args.outfile,dpi=300)
