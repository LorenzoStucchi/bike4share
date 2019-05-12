import random
import pandas as pd
from psycopg2 import connect

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
    tipo = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!£$%&/()=?^"
    lunghezza = 34
    psw = ""
    x = 0
    for x in range(int(lunghezza)):
        psw += tipo[int(random.randrange(len(tipo)))]
        x += 1
    return psw
        
# Main    
myFile = open('dbConfig.txt')
connStr = myFile.readline()
conn = connect(connStr)
cur = conn.cursor()

for command in cleanup :
    cur.execute(command)
for command in commands :
    cur.execute(command)
print('created tables')
s =[[]]
s_k = pd.DataFrame({"key"})
for i in range (20):
    secr_key = key_generator()
    cur.execute('INSERT INTO key_list (secret_key) VALUES (%s)', (secr_key,))
    s_k.loc[i] = [secr_key]    
print('created secret key')

s_k.to_csv('secret_key.txt', header=None, index=None, sep='\n')

cur.close()
conn.commit()
conn.close()


