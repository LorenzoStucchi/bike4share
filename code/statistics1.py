# -*- coding: utf-8 -*-
"""
Created on Mon May 20 17:18:06 2019

@author: sara maffioli
"""
#import packages
import pandas as pd
from sqlalchemy import create_engine
#from geoalchemy2 import Geometry
from psycopg2 import connect
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Select
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models.callbacks import CustomJS
from bokeh.palettes import Spectral5
from bokeh.transform import factor_cmap
import numpy as np


# Access to database
myFile = open('C:/Users/sara maffioli/Documents/GitHub/bike4share/code/dbConfig.txt')
connStr = myFile.readline()
data_conn = connStr.split(" ",2)
dbname = data_conn[0].split("=",1)[1]
username = data_conn[1].split("=",1)[1]
password = data_conn[2].split("=",1)[1]
conn = connect(connStr)
cur = conn.cursor()

#connection to the db
engine = create_engine('postgresql://'+username+':'+password+'@localhost:5432/'+dbname)
#read the datafram from postreSQL table
df_bike= pd.read_sql_table ('bike_stalls',engine)
df_stations = pd.read_sql_table('stations',engine)

#reindex the dataframe on a time index object using the date 
df_bike.index= pd.to_datetime (df_bike['time'])
df_bike['1'].plot
# convert the date column into days of the week and months
day =pd.to_datetime (df_bike['time']).dt.dayofweek
month =pd.to_datetime (df_bike['time']).dt.month
df_bike.insert(0, 'month', month)
df_bike['time'] = day
df_bike.rename(columns={'time':'day'}, inplace=True)
#compute the stations median bikes availability per day of the week and month
bike_days_med = df_bike.groupby('day', axis=0).median()
bike_months_med = df_bike.groupby('month', axis=0).median()
#axis row 0 is by default
bike_days_tot = df_bike.groupby('day', axis=0).sum()
bike_months_tot = df_bike.groupby('month', axis=0).sum()
day_name=bike_days_med.index.tolist()

#dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
#bike_days_med.rename(index=dayOfWeek,inplace=True)
#bike_days_med
#bike_days_med.rename(index={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'},inplace=True)

#Create Select Widget menu options with the list of all the stations
station_names = list(df_bike)
del station_names[0]
del station_names[0]
options=[]

for i in station_names:
    string = 'station %s' %i
    options.append(string) 

#Stations median bikes availability per day of the week plot
#Define variables
days = list(bike_days_med.index)
data = { 'x': days, 'y':  list(bike_days_med['1'])}

source = ColumnDataSource(data)



#Create the Bar plot day
p2 = figure(title="Stations median bikes availability per day of the week")
p2.vbar(x='x', top='y', source = source, width=0.9, line_color='white', legend='x')
      
p2.legend.orientation = "vertical"
p2.legend.location = "top_right"        

#Create Select Widget that allows us to create a drop down menu
select_widget = Select(options = options, value = options[0], 
                title = 'Select a station')


#callback needed to upload the graph
def callback(attr, old, new):
    column2plot = select_widget.value
    data.data = {'x' : days, 'y': list(bike_days_med[str(column2plot[-1])])}
    p2.vbar(x='x', top='y', source = source, width=0.9, line_color='white', 
            legend='x')
           
#Update Select Widget to each interaction
select_widget.on_change('value', callback)


#Stations median bikes availability per month plot
#Define variables
months= list(bike_months_med.index)
data_month = { 'x': months, 'y':  list(bike_months_med['1'])}
source_month = ColumnDataSource(data_month) 

#Create the Bar plot month
p3 = figure(title="Stations median bikes availability per month")
p3.vbar(x='x', top='y', source = source_month, width=0.9, line_color='white', legend='x')
      
p3.legend.orientation = "vertical"
p3.legend.location = "top_right"        

#callback needed to upload the graph
def callback(attr, old, new):
    column2plot = select_widget.value
    data.data = {'x' : days, 'y': list(bike_months_med[str(column2plot[-1])])}
    p3.vbar(x='x', top='y', source = source, width=0.9, line_color='white', 
            legend='x')

#Create the plot layout 
layout = row(select_widget, p2,p3 ) #p3
#Output the plot
output_file("hello.html")
show(layout)
# put the button and plot in a layout and add to the document
curdoc().add_root(layout)

