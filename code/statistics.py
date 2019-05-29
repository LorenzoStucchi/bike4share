# -*- coding: utf-8 -*-
"""
BAR PLOTS
"""
#import packages
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from psycopg2 import connect
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Select, FuncTickFormatter, LabelSet
from bokeh.io import curdoc
from bokeh.layouts import row,gridplot,column
from bokeh.models.widgets import Panel, Tabs
from bokeh.tile_providers import get_provider, Vendors #bokeh version 1.1
#from bokeh.tile_providers import CARTODBPOSITRON #bokeh version 1.0


# Access to database
myFile = open('dbConfig.txt')
connStr = myFile.readline()
data_conn = connStr.split(" ",2)
dbname = data_conn[0].split("=",1)[1]
username = data_conn[1].split("=",1)[1]
password = data_conn[2].split("=",1)[1]

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
bike_days_med=bike_days_med.drop('month', axis=1)
bike_months_med = df_bike.groupby('month', axis=0).median()
bike_months_med=bike_months_med.drop('day', axis=1)
#axis row 0 is by default
bike_days_tot = df_bike.groupby('day', axis=0).sum()
bike_days_tot=bike_days_tot.drop('month', axis=1)
bike_months_tot = df_bike.groupby('month', axis=0).sum()
bike_months_tot=bike_months_tot.drop('day', axis=1)
bikes_weekend=bike_days_med.drop(bike_days_med.index[[0,1,2,3]])

#Create Select Widget menu options with the list of all the stations
station_names = list(df_bike)
del station_names[0]
del station_names[0]
options_1=[]

for i in station_names:
    string = 'station %s' %i
    options_1.append(string) 

#Stations median bikes availability per day of the week plot
days = list(bike_days_med.index)
data = ColumnDataSource({'x' : days, 'y': list(bike_days_med['1'])})  
 
TOOLTIPS = [
    ("No.bikes", "@y")
]
p2 = figure(title="Stations median bikes availability per day of the week", tooltips=TOOLTIPS)
p2.vbar(x='x', top='y', source = data, width=0.9,  line_color='white')
p2.line('x', 'y', source = data, color = 'blue',line_width=2)
label_dict = {0:'Mon',1:'Tue',2:'Wen', 3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
p2.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict)

p2.background_fill_color = "#E8F8F5"
p2.xaxis.axis_label = "Day"
p2.xaxis.axis_label_text_color = "#0430F8"
p2.xaxis.major_label_text_color = "#0430F8"
p2.yaxis.axis_label = "Number of bikes"
p2.yaxis.axis_label_text_color = "#0430F8"
p2.yaxis.major_label_text_color = "#0430F8"
p2.yaxis.major_label_orientation = "vertical"

p2.title.align = "center"
p2.title.text_color = "#3498DB"
p2.title.background_fill_color = "#D1F2EB"

        
#Create Select Widget that allows us to create a drop down menu
p2_widget = Select(options = options_1, value = options_1[0], width=150,
                title = 'Select a station', background='#D1F2EB')


#callback needed to upload the graph
def callback(attr, old, new):
    column2plot = p2_widget.value
    if int(column2plot[-2:]) > 9:
        num = column2plot[-2:]
    else:
        num = column2plot[-1:]
    data.data = {'x' : days, 'y': list(bike_days_med[num])}
    p2.vbar(x='x', top='y', source = data, width=0.9, line_color='white')
    p2.line('x', 'y', source = data, color = 'blue',line_width=2)
    p2.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict)
   
#Update Widget to each interaction
p2_widget.on_change('value', callback)



#Stations median bikes availability per month plot
months= list(bike_months_med.index)
data_m = ColumnDataSource({ 'x': months, 'y':  list(bike_months_med['1'])}) 

TOOLTIPS = [
    ("No.bikes", "@y")
]
p3 = figure(title="Stations median bikes availability per month", tooltips=TOOLTIPS)
p3.vbar(x='x', top='y', source = data_m, width=0.9, line_color='white')
p3.line('x', 'y', source = data_m, color = 'blue',line_width=2)
label_dict_m = {0:'Jan',1:'Jan',2:'Feb',3:'Mar', 4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
p3.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict_m)

p3.background_fill_color = "#E8F8F5"
p3.xaxis.axis_label = "Month"
p3.xaxis.axis_label_text_color = "#0430F8"
p3.xaxis.major_label_text_color = "#0430F8"
p3.yaxis.axis_label = "Number of bikes"
p3.yaxis.axis_label_text_color = "#0430F8"
p3.yaxis.major_label_text_color = "#0430F8"
p3.yaxis.major_label_orientation = "vertical"

p3.title.align = "center"
p3.title.text_color = "#3498DB"
p3.title.background_fill_color = "#D1F2EB"      

p3_widget = Select(options= options_1, value= options_1[0], width=150,
                title = 'Select a station',background='#D1F2EB')

#callback needed to upload the graph
def callback2(attr, old, new):
    column3plot = p3_widget.value
    if int(column3plot[-2:]) > 9:
        num = column3plot[-2:]
    else:
        num = column3plot[-1:]
    data_m.data = {'x' : months, 'y': list(bike_months_med[num])}
    p3.vbar(x='x', top='y', source = data_m, width=0.9, line_color='white')
    p3.line('x', 'y', source = data_m, color = 'blue',line_width=2)
    p3.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict_m)

p3_widget.on_change('value', callback2)


#Total bikes availability per day of the week plot
days = list(bike_days_tot.index)
data_4 = ColumnDataSource({'x' : days, 'y': list(bike_days_tot['1'])})  
 
TOOLTIPS = [
    ("No.bikes", "@y")
]
p4 = figure(title="Total bikes availability per day of the week", tooltips=TOOLTIPS)
p4.vbar(x='x', top='y', source = data_4, width=0.9,  line_color='white',color='#DA1414')
p4.line('x', 'y', source = data_4, color = 'red',line_width=2)
label_dict = {0:'Mon',1:'Tue',2:'Wen', 3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
p4.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict)

p4.background_fill_color = "#F5B7B1"
p4.xaxis.axis_label = "Day"
p4.xaxis.axis_label_text_color = "#FF0000"
p4.xaxis.major_label_text_color = "#FF0000"
p4.yaxis.axis_label = "Number of bikes"
p4.yaxis.axis_label_text_color = "#FF0000"
p4.yaxis.major_label_text_color = "#FF0000"
p4.yaxis.major_label_orientation = "vertical"

p4.title.align = "center"
p4.title.text_color = "#E70F0F"
p4.title.background_fill_color = "#FADBD8"

        
#Create Select Widget that allows us to create a drop down menu
p4_widget = Select(options = options_1, value = options_1[0], width=150,
                title = 'Select a station', background='#FADBD8')


#callback needed to upload the graph
def callback4(attr, old, new):
    column4plot = p4_widget.value
    if int(column4plot[-2:]) > 9:
        num = column4plot[-2:]
    else:
        num = column4plot[-1:]
    data_4.data = {'x' : days, 'y': list(bike_days_tot[num])}
    p4.vbar(x='x', top='y', source = data_4, width=0.9, line_color='white',color='#DA1414')
    p4.line('x', 'y', source = data_4, color = 'red',line_width=2)        
    p4.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict)
   
#Update Widget to each interaction
p4_widget.on_change('value', callback4)



#Stations median bikes availability per month plot
months= list(bike_months_tot.index)
data_5 = ColumnDataSource({ 'x': months, 'y':  list(bike_months_tot['1'])}) 

TOOLTIPS = [
    ("No.bikes", "@y")
]
p5 = figure(title="Total bikes availability per month", tooltips=TOOLTIPS)
p5.vbar(x='x', top='y', source = data_5, width=0.9, line_color='white',color='#DA1414')
p5.line('x', 'y', source = data_5, color = 'red',line_width=2)
label_dict_m = {0:'Jan',1:'Jan',2:'Feb',3:'Mar', 4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
p5.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict_m)

p5.background_fill_color = "#F5B7B1"
p5.xaxis.axis_label = "Month"
p5.xaxis.axis_label_text_color = "#FF0000"
p5.xaxis.major_label_text_color = "#FF0000"
p5.yaxis.axis_label = "Number of bikes"
p5.yaxis.axis_label_text_color = "#FF0000"
p5.yaxis.major_label_text_color = "#FF0000"
p5.yaxis.major_label_orientation = "vertical"

p5.title.align = "center"
p5.title.text_color = "#E70F0F"
p5.title.background_fill_color = "#FADBD8"    

p5_widget = Select(options= options_1, value= options_1[0], width=150,
                title = 'Select a station',background='#FADBD8')

#callback needed to upload the graph
def callback5(attr, old, new):
    column5plot = p5_widget.value
    if int(column5plot[-2:]) > 9:
        num = column5plot[-2:]
    else:
        num = column5plot[-1:]
    data_5.data = {'x' : months, 'y': list(bike_months_tot[num])}
    p5.vbar(x='x', top='y', source = data_5, width=0.9, line_color='white',color='#DA1414')
    p5.line('x', 'y', source = data_5, color = 'red',line_width=2)        
    p5.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict_m)

p5_widget.on_change('value', callback5)

#Stations bikes availability during weeknds
day2= list(bikes_weekend.index)
data_6 = ColumnDataSource({ 'x': day2, 'y':  list(bikes_weekend['1'])}) 

TOOLTIPS = [
    ("No.bikes", "@y")
]
p6 = figure(title="Bikes availability trend weekend", tooltips=TOOLTIPS)
p6.line('x', 'y', source = data_6, color = 'orange',line_width=2)
label_dict_2 = {4:'Friday',5:'Saturday',6:'Sunday'}
p6.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict_2)

p6.background_fill_color = "#FDEBD0"
p6.xaxis.axis_label = "Day"
p6.xaxis.axis_label_text_color = "#FD6400"
p6.xaxis.major_label_text_color = "#FD6400"
p6.yaxis.axis_label = "Number of bikes"
p6.yaxis.axis_label_text_color = "#FD6400"
p6.yaxis.major_label_text_color = "#FD6400"
p6.yaxis.major_label_orientation = "vertical"

p6.title.align = "center"
p6.title.text_color = "#FD6400"
p6.title.background_fill_color = "#FEB280"    

p6_widget = Select(options= options_1, value= options_1[0], width=150,
                title = 'Select a station',background= '#FDEBD0')

#callback needed to upload the graph
def callback6(attr, old, new):
    column6plot = p6_widget.value
    if int(column6plot[-2:]) > 9:
        num = column6plot[-2:]
    else:
        num = column6plot[-1:]
    data_6.data = {'x' : day2, 'y': list(bikes_weekend[num])}
    p6.line('x', 'y', source = data_6, color = 'orange',line_width=2)
    label_dict_2 = {4:'Friday',5:'Saturday',6:'Sunday'}
    p6.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict_2)

p6_widget.on_change('value', callback6)

#Create the plot layout 
g2= gridplot([p2_widget, p2], ncols=2,  plot_height=400,toolbar_location="right")
g3= gridplot([p3_widget, p3], ncols=2, plot_height=400,toolbar_location="right")
g2_panel = Panel(child=g2, title='Day median availability')
g3_panel = Panel(child=g3, title='Month median availability')
g4= gridplot([p4_widget, p4], ncols=2, plot_height=400,toolbar_location="right")
g5= gridplot([p5_widget, p5], ncols=2,  plot_height=400,toolbar_location="right")
g4_panel = Panel(child=g4, title='Day tot availability')
g5_panel = Panel(child=g5, title='Month tot availability')
g6= gridplot([p6_widget, p6], ncols=2, plot_height=400,toolbar_location="right")
g6_panel = Panel(child=g6, title='Availability weekend')
# Assign the panels to Tabs

#tab = Tabs(tabs=[g2_panel,g3_panel,g4_panel,g5_panel,g6_panel])
         
'''MAP PLOT'''

#Importing data
stations = gpd.read_file("data/stations.shp").to_crs(epsg=3857)
#create a function to extract coordinates from the geodataframe 
def getPointCoords(rows, geom, coord_type):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    if coord_type == 'x':
        return rows[geom].x
    elif coord_type == 'y':
        return rows[geom].y
    
stations['x'] = stations.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
stations['y'] = stations.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)

#Save the coordinates as attributes ina new dataframe
stations_df = stations.drop('geometry', axis=1).copy()

#Use the dataframe as Bokeh ColumnDataSource
psource = ColumnDataSource(stations_df)

#Specify feature of the Hoover tool add a widget and costumize it

TOOLTIPS2=[
    ("name", "@BIKE_SH"),
    ("capacity", "@STALLI")
]
#Create the Map plot
p1 = figure(x_range=(1020414, 1024954), y_range=(5692309, 5698497),
           x_axis_type="mercator", y_axis_type="mercator", tooltips=TOOLTIPS2,
           title="Move over the map", height=400)
p1.title.text_font_size = "25px"
p1.title.align = "center"
p1.title.text_color = "#3498DB"
p1.title.background_fill_color = "#D1F2EB"
#Add basemap tile
p1.add_tile(get_provider(Vendors.CARTODBPOSITRON)) #bokeh version 1.1
#p1.add_tile(CARTODBPOSITRON) #bokeh version 1.0
#Add Glyphs radius change according to the zoom
p1.circle('x', 'y', source=psource, color='blue', radius=40) #size=10

#Add Labels and add to the plot layout
labels = LabelSet(x='x', y='y', text='ID', text_color='blue',
              x_offset=5, y_offset=5, source=psource,render_mode='canvas')
p1.add_layout(labels)
#g1= gridplot([tab,p1], ncols=2, toolbar_location="right")
g1_panel = Panel(child=p1, title='Map')
tab = Tabs(tabs=[g2_panel,g3_panel,g4_panel,g5_panel,g6_panel,g1_panel])		  
layout=(tab)
#Output the plot
output_file("templates/stat_bikes.html")
show(layout)
# put the button and plot in a layout and add to the document
curdoc().add_root(layout)

