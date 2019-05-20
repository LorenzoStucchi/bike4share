import random
import pandas as pd
import geopandas as gpd
from psycopg2 import connect
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement

#SQL Command
cleanup = (
        'DROP TABLE IF EXISTS user_bike CASCADE',
        'DROP TABLE IF EXISTS key_list CASCADE'
        )

commands = (
        """
        CREATE TABLE key_list (
            id_key SERIAL PRIMARY KEY,
            secret_key VARCHAR(35) UNIQUE NOT NULL
        )
        """,

        """
        CREATE TABLE user_bike (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) UNIQUE NOT NULL,
            user_password VARCHAR(255) NOT NULL,
            user_type VARCHAR(255)
        )
        
        """)   
   
#KEY GENERATOR
def key_generator():
    arr = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!£$%&/()=?^"
    leng = 34
    psw = ""
    x = 0
    for x in range(int(leng)):
        psw += tipo[int(random.randrange(len(arr)))]
        x += 1
    return psw
        
# Main   
# Access to database
myFile = open('dbConfig.txt')
connStr = myFile.readline()
data_conn = connStr.split(" ",2)
dbname = data_conn[0].split("=",1)[1]
username = data_conn[1].split("=",1)[1]
password = data_conn[2].split("=",1)[1]
conn = connect(connStr)
cur = conn.cursor()
# Delete previous tables
for command in cleanup :
    cur.execute(command)
# Create new tables
for command in commands :
    cur.execute(command)
print('created tables')
# Fill the secret_key table
s_k = pd.DataFrame({"key"})
for i in range (20):
    secr_key = key_generator()
    cur.execute('INSERT INTO key_list (secret_key) VALUES (%s)', (secr_key,))
    s_k.loc[i] = [secr_key]    
print('Added secret key')
# Save secret key into a txt file
s_k.to_csv('secret_key.txt', header=None, index=None, sep='\n')
# Create engine for import dataframe
db_url = 'postgresql://'+username+':'+password+'@localhost:5432/'+dbname
engine = create_engine(db_url)
# Import dataframe of bike and stalls
df = pd.read_csv('./data/bike.csv')
df.to_sql('bike_stalls', engine, if_exists='replace', index=False)
print('Added dataframe of bike and stalls')
# Import geodataframe of the stations (shapefile)
#gdf = gpd.read_file('./data/stations.shp')
#gdf['geom'] = gdf['geometry'].apply(lambda x: WKTElement(x.wkt, srid=4326))
#gdf.drop('geometry', 1, inplace=True)
#gdf.to_sql('stations', engine, if_exists='replace', index=True, 
#            dtype={('geom'): Geometry('POINT', srid= 4326)})

# Import geodataframe of the stations (csv)
gdf = pd.read_csv('./data/stations.csv')
gdf.to_sql('stations', engine, if_exists='replace', index=False)
print('Added dataframe of stations')
# Close connection 
cur.close()
conn.commit()
conn.close()


