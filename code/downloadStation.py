import pandas as pd
from sqlalchemy import create_engine
import geojson

def data2geojson(df,url):
    features = []
    insert_features = lambda X: features.append(
            geojson.Feature(geometry=geojson.Point((X["Longitude"],
                                                    X["Latitude"])),
                            properties=dict(ID=X["ID"],
                                            STALLI=X["STALLI"],
                                            BIKE_SH=X["BIKE_SH"],
                                            INDIRIZZO=X["INDIRIZZO"],
                                            LOCALIZ=X["LOCALIZ"])))
    df.apply(insert_features, axis=1)
    with open(url, 'w', encoding='utf8') as fp:
        geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)

def data_to_geojson(url):
    myFile = open('dbConfig.txt')
    connStr = myFile.readline()
    data_conn = connStr.split(" ",2)
    dbname = data_conn[0].split("=",1)[1]
    username = data_conn[1].split("=",1)[1]
    password = data_conn[2].split("=",1)[1]
    db_url = 'postgresql://'+username+':'+password+'@localhost:5432/'+dbname
    engine = create_engine(db_url)
    data = pd.read_sql_table('stations',engine)
    data2geojson(data,url)
    
def add_var(url,name_file):
    with open(url,"r+") as f:
        features = f.read()
        f.seek(0)
        f.write("var "+name_file+" = ["+features+"];")

name_file = 'bike_stalls'   
url = 'static/'+name_file+'.geojson'

data_to_geojson(url)
add_var(url, name_file)

