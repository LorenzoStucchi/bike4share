import pandas as pd
from sqlalchemy import create_engine
import geojson

name_file = 'stations'   
url = 'static/'+name_file+'.geojson'

myFile = open('dbConfig.txt')
connStr = myFile.readline()
data_conn = connStr.split(" ",2)
dbname = data_conn[0].split("=",1)[1]
username = data_conn[1].split("=",1)[1]
password = data_conn[2].split("=",1)[1]
db_url = 'postgresql://'+username+':'+password+'@localhost:5432/'+dbname
engine = create_engine(db_url)
data = pd.read_sql_table('stations',engine)
features = []
insert_features = lambda X: features.append(
        geojson.Feature(geometry=geojson.Point((X["Longitude"],
                                                X["Latitude"])),
                        properties=dict(ID=X["ID"],
                                        STALLI=X["STALLI"],
                                        BIKE_SH=X["BIKE_SH"],
                                        INDIRIZZO=X["INDIRIZZO"],
                                        LOCALIZ=X["LOCALIZ"])))
data.apply(insert_features, axis=1)
with open(url, 'w', encoding='utf8') as fp:
    geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)

f = open('static/var_stalls.geojson',"w")
with open(url,"r+") as f1:
    features = f1.read()
    f.seek(0)
    f.write("var "+name_file+" = ["+features+"];")

print("Saved locally stalls position")