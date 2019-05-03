#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 23:54:08 2019

@author: elisabettadinitto
"""
import random

from psycopg2 import (
        connect
)

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

sqlCommands = (
        'INSERT INTO user_bike (user_name, user_password) VALUES (%s, %s) RETURNING user_id',
        'INSERT INTO key_list (secret_key) VALUES (%s)'
        )        
#KEY GENERATOR
def key_generator():
    tipo = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lunghezza = 34
    psw = ""
    x = 0
    for x in range(int(lunghezza)):
        psw += tipo[int(random.randrange(len(tipo)))]
        x += 1
    return psw
        
        
conn = connect("dbname=bike4share user=postgres password=postgres")
cur = conn.cursor()

for command in cleanup :
    cur.execute(command)
for command in commands :
    cur.execute(command)
    print('execute command')
a = key_generator()
cur.execute(sqlCommands[0], (a, a))
#userId = cur.fetchone()[0]
#for i in range (20):
#   a = key_generator()
    #cur.execute(sqlCommands[1], ('pippo'))
#    pippo='pippo'
cur.execute('INSERT INTO key_list (secret_key) VALUES (%s)', a)
    
#    
#    
#
#print(cur.fetchall())
cur.execute('SELECT * FROM user_bike')
cur.close()
conn.commit()
conn.close()


