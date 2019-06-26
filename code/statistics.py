"""
BAR PLOTS
"""
#import packages
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from psycopg2 import connect
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Select, FuncTickFormatter, LabelSet,DatetimeTickFormatter
from bokeh.io import curdoc
from bokeh.layouts import row,gridplot
from bokeh.models.widgets import Panel, Tabs
from bokeh.tile_providers import get_provider, Vendors
import time
from datetime import date,timedelta
import datetime

# Access to database
myFile = open('dbConfig.txt')
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
# now time and day
hour_now = time.strftime("%H")
day_now = date.today().strftime("%m-%d")
now = "2010-"+day_now+" "+hour_now+":00:00"
for i in range(0,7):
    start_week=datetime.datetime.strptime(now, '%Y-%m-%d %H:00:00') - timedelta(days=i) 
    start_week=str(start_week)
    
if date.today().strftime("%m") in [ "04" ,"06" ,"09" ,"10"]:
    for i in range(0,30):
        start_month= datetime.datetime.strptime(now, '%Y-%m-%d %H:00:00') - timedelta(days=i) 
        start_month=str(start_month)
elif date.today("m") == "02":
    for i in range(0,28) :
        start_month=datetime.datetime.strptime(now, '%Y-%m-%d %H:00:00') - timedelta(days=i) 
        start_month=str(start_month)
else:    
    for i in range(0,31) :
        start_month=datetime.datetime.strptime(now, '%Y-%m-%d %H:00:00') - timedelta(days=i)
        start_month=str(start_month)

for index, row in df_bike.iterrows():
    if row.time == now:
        end=index
        break
for index, row in df_bike.iterrows():
    if row.time ==  start_week :
        start=index
        break   
previous_week=df_bike.loc[start:end]
previous_week.index= pd.to_datetime (previous_week['time'])
previous_week['1'].plot
previous_week=previous_week.drop('time', axis=1)

for index, row in df_bike.iterrows():
    if row.time == start_month :
        start_month_ind=index
        break  
previous_month=df_bike.loc[start_month_ind:end]
previous_month.index= pd.to_datetime (previous_month['time'])
previous_month['1'].plot
previous_month=previous_month.drop('time', axis=1)

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
#percentage
tot_bike_per_stalls = df_stations[["STALLI","ID"]]
tot_bike_per_stalls.index = tot_bike_per_stalls.ID
tot_bike_per_stalls = tot_bike_per_stalls.drop('ID',axis=1)
tot_bike_per_stalls = tot_bike_per_stalls.T

tot_days = pd.DataFrame(tot_bike_per_stalls*24*52)
for i in range(6):
    tot_days = tot_days.append(tot_bike_per_stalls*24*52,ignore_index=True)
    
tot_months = pd.DataFrame(tot_bike_per_stalls*24*31)
tot_months = tot_months.append(tot_bike_per_stalls*24*28,ignore_index=True)
tot_months = tot_months.append(tot_bike_per_stalls*24*31,ignore_index=True)
tot_months = tot_months.append(tot_bike_per_stalls*24*30,ignore_index=True)
tot_months = tot_months.append(tot_bike_per_stalls*24*31,ignore_index=True)
tot_months = tot_months.append(tot_bike_per_stalls*24*30,ignore_index=True)
tot_months = tot_months.append(tot_bike_per_stalls*24*31,ignore_index=True)
tot_months = tot_months.append(tot_bike_per_stalls*24*31,ignore_index=True)
tot_months = tot_months.append(tot_bike_per_stalls*24*30,ignore_index=True)
tot_months = tot_months.append(tot_bike_per_stalls*24*31,ignore_index=True)
tot_months = tot_months.append(tot_bike_per_stalls*24*30,ignore_index=True)
tot_months = tot_months.append(tot_bike_per_stalls*24*31,ignore_index=True)

tot_days.index = tot_days.index.map(int)
tot_months.index = tot_months.index.map(int)
bike_days_tot.columns = bike_days_tot.columns.map(int)
del bike_days_tot.index.name
del tot_days.columns.name

bike_months_tot.columns = bike_months_tot.columns.map(int)
bike_months_tot.index = bike_months_tot.index-1
del bike_months_tot.index.name

bike_days_tot_perc = 100*bike_days_tot/tot_days
bike_months_tot_perc = 100*bike_months_tot/tot_months

bike_days_tot_perc.index.name = "day"
bike_days_tot_perc.columns = bike_days_tot_perc.columns.map(str)

bike_months_tot_perc.index.name = "month"
bike_months_tot_perc.columns = bike_months_tot_perc.columns.map(str)

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
p2.border_fill_color = "#EEEEEE"
p2.min_border_left = 40
        
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
p3.vbar(x='x', top='y', source = data_m, width=1, line_color='white')
p3.line('x', 'y', source = data_m, color = 'blue',line_width=2)
label_dict_m = {0:0, 1:'Jan',2:'Feb',3:'Mar', 4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
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
p3.border_fill_color = "#EEEEEE"
p3.min_border_left = 40

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
days = list(bike_days_tot_perc.index)
data_4 = ColumnDataSource({'x' : days, 'y': list(bike_days_tot_perc['1'])})  
 
TOOLTIPS = [
    ("% av. bikes", "@y")
]
p4 = figure(title="Percentage of bikes availability per day", tooltips=TOOLTIPS)
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
p4.border_fill_color = "#EEEEEE"
p4.min_border_left = 40
        
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
    data_4.data = {'x' : days, 'y': list(bike_days_tot_perc[num])}
    p4.line('x', 'y', source = data_4, color = 'red',line_width=2)        
    p4.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict)
   
#Update Widget to each interaction
p4_widget.on_change('value', callback4)



#Stations median bikes availability per month plot
months= list(bike_months_tot_perc.index)
data_5 = ColumnDataSource({ 'x': months, 'y':  list(bike_months_tot_perc['1'])}) 

TOOLTIPS = [
    ("% av. bikes", "@y")
]
p5 = figure(title="Percentage of bikes availability per month", tooltips=TOOLTIPS)
p5.line('x', 'y', source = data_5, color = 'red',line_width=2)
label_dict_m = {0:'Jan',1:'Feb',2:'Mar', 3:'Apr',4:'May',5:'Jun',6:'Jul',7:'Aug',8:'Sep',9:'Oct',10:'Nov',11:'Dec'}
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
p5.border_fill_color = "#EEEEEE"
p5.min_border_left = 40

p5_widget = Select(options= options_1, value= options_1[0], width=150,
                title = 'Select a station',background='#FADBD8')

#callback needed to upload the graph
def callback5(attr, old, new):
    column5plot = p5_widget.value
    if int(column5plot[-2:]) > 9:
        num = column5plot[-2:]
    else:
        num = column5plot[-1:]
    data_5.data = {'x' : months, 'y': list(bike_months_tot_perc[num])}
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
p6 = figure(title="Bikes availability trend during weekend", tooltips=TOOLTIPS)
p6.vbar(x='x', top='y', source = data_6, width=0.9, line_color='white', color='orange')
p6.line('x', 'y', source = data_6, color = '#FF9B00',line_width=2)
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
p6.border_fill_color = "#EEEEEE"
p6.min_border_left = 40
p6.xaxis.ticker = [4, 5, 6]
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
    p6.vbar(x='x', top='y', source = data_6, width=0.9, line_color='white', color='orange')
    p6.line('x', 'y', source = data_6, color = '#FF9B00',line_width=2)
    label_dict_2 = {4:'Friday',5:'Saturday',6:'Sunday'}
    p6.xaxis.formatter = FuncTickFormatter(code="""
        var labels = %s;
        return labels[tick];
    """ % label_dict_2)

p6_widget.on_change('value', callback6)


'''MAP PLOT'''

#Importing data
stations = gpd.read_file("static/stations.geojson").to_crs(epsg=3857)
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
           title="Move over the map", height=400, width=400)
#p1.title.text_font_size = "25px"
p1.title.align = "center"
p1.title.text_color = "#3498DB"
p1.title.background_fill_color = "#D1F2EB"
p1.border_fill_color = "#EEEEEE"
p1.min_border_left = 40

#Add basemap tile
p1.add_tile(get_provider(Vendors.CARTODBPOSITRON)) #bokeh version 1.1
#p1.add_tile(CARTODBPOSITRON) #bokeh version 1.0
#Add Glyphs radius change according to the zoom
p1.circle('x', 'y', source=psource, color='blue', radius=40) #size=10

#Add Labels and add to the plot layout
labels = LabelSet(x='x', y='y', text='ID', text_color='blue',
              x_offset=5, y_offset=5, source=psource,render_mode='canvas')
p1.add_layout(labels)
#g1_panel = Panel(child=p1, title='Map')

'''REAL TIME PLOTS'''
#Stations bikes availability during previous week
date_7= list(previous_week.index)
data_7 = ColumnDataSource({ 'x': date_7, 'y':  list(previous_week['1'])}) 

TOOLTIPS = [
    ("No.bikes", "@y")
]

p7 = figure(title="Bikes availability real time data previous week", tooltips=TOOLTIPS)
p7.line('x', 'y', source = data_7, color = 'green',line_width=2)
p7.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )

p7.background_fill_color = "#ADFCA2"
p7.xaxis.axis_label = "Date"
p7.xaxis.axis_label_text_color = "#17AA02"
p7.xaxis.major_label_text_color = "#17AA02"
p7.yaxis.axis_label = "Number of bikes"
p7.yaxis.axis_label_text_color = "#17AA02"
p7.yaxis.major_label_text_color = "#17AA02"
p7.yaxis.major_label_orientation = "vertical"

p7.title.align = "center"
p7.title.text_color = "#17AA02"
p7.title.background_fill_color = "#A8FF33"    
p7.border_fill_color = "#EEEEEE"
p7.min_border_left = 40

p7_widget = Select(options= options_1, value= options_1[0], width=150,
                title = 'Select a station',background= '#ADFCA2')

#callback needed to upload the graph
def callback7(attr, old, new):
    column7plot = p7_widget.value
    if int(column7plot[-2:]) > 9:
        num = column7plot[-2:]
    else:
        num = column7plot[-1:]
    data_7.data = {'x' : date_7, 'y': list(previous_week[num])}
    p6.line('x', 'y', source = data_7, color = 'green',line_width=2)

p7_widget.on_change('value', callback7)

#Stations bikes availability during previous month
date_8= list(previous_month.index)
data_8 = ColumnDataSource({ 'x': date_8, 'y':  list(previous_month['1'])}) 

TOOLTIPS = [
    ("No.bikes", "@y")
]
p8 = figure(title="Bikes availability real time data previous month", tooltips=TOOLTIPS)
p8.line('x', 'y', source = data_8, color = 'green',line_width=2)
p8.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )


p8.background_fill_color = "#ADFCA2"
p8.xaxis.axis_label = "Date"
p8.xaxis.axis_label_text_color = "#17AA02"
p8.xaxis.major_label_text_color = "#17AA02"
p8.yaxis.axis_label = "Number of bikes"
p8.yaxis.axis_label_text_color = "#17AA02"
p8.yaxis.major_label_text_color = "#17AA02"
p8.yaxis.major_label_orientation = "vertical"

p8.title.align = "center"
p8.title.text_color = "#17AA02"
p8.title.background_fill_color = "#A8FF33"    
p8.border_fill_color = "#EEEEEE"
p8.min_border_left = 40

p8_widget = Select(options= options_1, value= options_1[0], width=150,
                title = 'Select a station',background= '#ADFCA2')

#callback needed to upload the graph
def callback8(attr, old, new):
    column8plot = p8_widget.value
    if int(column8plot[-2:]) > 9:
        num = column8plot[-2:]
    else:
        num = column8plot[-1:]
    data_8.data = {'x' : date_8, 'y': list(previous_month[num])}
    p8.line('x', 'y', source = data_8, color = 'green',line_width=2)


p8_widget.on_change('value', callback8)
#Create the plot layout 
g2= gridplot([p2_widget,p2], ncols=2, plot_height=400,toolbar_location="right")
g_2= gridplot([g2,p1], ncols=2,toolbar_location="right")
g3= gridplot([p3_widget, p3], ncols=2, plot_height=400,toolbar_location="right")
g_3= gridplot([g3,p1], ncols=2,toolbar_location="right")
g2_panel = Panel(child=g_2, title='Day median availability')
g3_panel = Panel(child=g_3, title='Month median availability')
g4= gridplot([p4_widget, p4], ncols=2, plot_height=400,toolbar_location="right")
g_4= gridplot([g4,p1], ncols=2,toolbar_location="right")
g5= gridplot([p5_widget, p5], ncols=2,  plot_height=400,toolbar_location="right")
g_5= gridplot([g5,p1], ncols=2,toolbar_location="right")
g4_panel = Panel(child=g_4, title='Percentage per day')
g5_panel = Panel(child=g_5, title='Percentage per month')
g6= gridplot([p6_widget, p6], ncols=2, plot_height=400,toolbar_location="right")
g_6= gridplot([g6,p1], ncols=2,toolbar_location="right")
g6_panel = Panel(child=g_6, title='Weekend availability')
g7= gridplot([p7_widget, p7], ncols=2, plot_height=400,toolbar_location="right")
g_7= gridplot([g7,p1], ncols=2,toolbar_location="right")
g7_panel = Panel(child=g_7, title='Real time data previous week')
g8= gridplot([p8_widget, p8], ncols=2, plot_height=400,toolbar_location="right")
g_8= gridplot([g8,p1], ncols=2,toolbar_location="right")
g8_panel = Panel(child=g_8, title='Real time data previous month')


tab = Tabs(tabs=[g2_panel,g3_panel,g4_panel,g5_panel,g6_panel,g7_panel,g8_panel])		  
layout=(tab)
#Output the plot
output_file("templates/stat_bikes.html")
show(layout)
# put the button and plot in a layout and add to the document
curdoc().add_root(layout)

