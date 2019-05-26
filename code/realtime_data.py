import pandas as pd
from sqlalchemy import create_engine
import time
from datetime import date
import downloadStation as dS
import geojson

myFile = open('dbConfig.txt')
connStr = myFile.readline()
data_conn = connStr.split(" ",2)
dbname = data_conn[0].split("=",1)[1]
username = data_conn[1].split("=",1)[1]
password = data_conn[2].split("=",1)[1]
db_url = 'postgresql://'+username+':'+password+'@localhost:5432/'+dbname
engine = create_engine(db_url)

df_bike = pd.read_sql_table('bike_stalls',engine)

# now time and day
hour_now = time.strftime("%H")
day_now = date.today().strftime("%m-%d")
now = "2010-"+day_now+" "+hour_now+":00:00"

for index, row in df_bike.iterrows():
    if row.time == now:
        break
    
bike_free = row
bike_free.pop('time')
bike_free.index = bike_free.index.map(int)
bike_free = bike_free.to_frame()

bike_free.rename(columns={index:'available'}, inplace=True)

stations = pd.read_sql_table('stations',engine)
stations.index = stations.ID
stations = bike_free.merge(stations, how='outer', left_index=True, right_index=True)

# serve eliminare i valori nan, scegliere come trasformare questi valori se 
# renderli zero o non fare i calcoli in questo caso

stalls_free = stations["STALLI"] - stations["available"]
stalls_free =stalls_free.to_frame()
stations.insert(0, 'free', stalls_free) 

name_file = 'stalls_free'   
url = 'static/'+name_file+'.geojson'

# sotto funziona ma serve risorvere il punto prima

#features = []
#insert_features = lambda X: features.append(
#        geojson.Feature(geometry=geojson.Point((X["Longitude"],
#                                                X["Latitude"])),
#                        properties=dict(ID = X["ID"],
#                                        STALLI = X["STALLI"],
#                                        BIKE_SH = X["BIKE_SH"],
#                                        INDIRIZZO = X["INDIRIZZO"],
#                                        LOCALIZ = X["LOCALIZ"],
#                                        FREE = X["free"],
#                                        AVAILABLE = X["available"])))
#stations.apply(insert_features, axis=1)
#
#with open(url, 'w', encoding='utf8') as fp:
#    geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)
#
#dS.add_var(url, name_file)