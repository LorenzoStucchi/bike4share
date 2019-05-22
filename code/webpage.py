from flask import (
    Flask, render_template, request, redirect, flash, url_for, session, g
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from psycopg2 import connect

import pandas as pd
from sqlalchemy import create_engine
import geojson

# Create the application instance
app = Flask(__name__, template_folder="templates")
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# function
def get_dbConn():
    if 'dbConn' not in g:
        myFile = open('dbConfig.txt')
        connStr = myFile.readline()
        g.dbConn = connect(connStr)
    
    return g.dbConn

def close_dbConn():
    if 'dbConn' in g:
        g.dbComm.close()
        g.pop('dbConn')
        
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        conn = get_dbConn()
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM user_bike WHERE user_id = %s', (user_id,)
        )
        g.user = cur.fetchone()
        cur.close()
        conn.commit()
    if g.user is None:
        return False
    else: 
        return True
    
# block used to download the data of stations from the server
#def data2geojson(df):
#    features = []
#    insert_features = lambda X: features.append(
#            geojson.Feature(geometry=geojson.Point((X["Longitude"],
#                                                    X["Latitude"])),
#                            properties=dict(ID=X["ID"],
#                                            STALLI=X["STALLI"],
#                                            BIKE_SH=X["BIKE_SH"],
#                                            INDIRIZZO=X["INDIRIZZO"],
#                                            LOCALIZ=X["LOCALIZ"])))
#    df.apply(insert_features, axis=1)
#    with open('static/bike_stalls.geojson', 'w', encoding='utf8') as fp:
#        geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)
#
#def data_to_geojson():
#    myFile = open('dbConfig.txt')
#    connStr = myFile.readline()
#    data_conn = connStr.split(" ",2)
#    dbname = data_conn[0].split("=",1)[1]
#    username = data_conn[1].split("=",1)[1]
#    password = data_conn[2].split("=",1)[1]
#    db_url = 'postgresql://'+username+':'+password+'@localhost:5432/'+dbname
#    engine = create_engine(db_url)
#    data = pd.read_sql_table('stations',engine)
#    data2geojson(data)
    
    
        
# Create a URL route in our application for "/"
@app.route('/')
@app.route('/index')
def index():
    conn = get_dbConn()
    cur = conn.cursor()
    cur.close()
    conn.commit()
    load_logged_in_user()
    #data_to_geojson()

    return render_template('index.html')
        
#USER REGISTRATION
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = 'u'
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else :
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
            'SELECT user_id FROM user_bike WHERE user_name = %s', (username,))
            if cur.fetchone() is not None:
                error = 'User {} is already registered.'.format(username)
                cur.close()

        if error is None:
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO user_bike (user_name, user_password, user_type) VALUES (%s, %s, %s)',
                (username, generate_password_hash(password), user_type)
            )
            cur.close()
            conn.commit()
            return redirect(url_for('login'))

        flash(error)

    return render_template('auth/register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_dbConn()
        cur = conn.cursor()
        error = None
        cur.execute(
            'SELECT * FROM user_bike WHERE user_name = %s', (username,)
        )
        user = cur.fetchone()
        cur.close()
        conn.commit()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#TECH REGISTRATION
@app.route('/tec_reg', methods=('GET', 'POST'))
def tec_reg():
    
    if request.method =='POST':
        secret_code = request.form['secret_code']
        username = request.form['username']
        password = request.form['password']
        
        conn = get_dbConn()
        cur = conn.cursor()
        error = None
        cur.execute(
            'SELECT * FROM key_list WHERE secret_key = %s', (secret_code,)
        )
        s_k = cur.fetchone()
        cur.close()
        conn.commit()
        
        if s_k is None:
            error = ' Incorrect secret key, Please contact the administrator to obtain it.'
            flash(error)
        else:
            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            else :
                conn = get_dbConn()
                cur = conn.cursor()
                cur.execute(
                'SELECT user_id FROM user_bike WHERE user_name = %s', (username,))
                if cur.fetchone() is not None:
                    error = 'User {} is already registered.'.format(username)
                    cur.close()
                    
            flash(error)
            
            if error is None:
                conn = get_dbConn()
                cur = conn.cursor()
                user_type = 't'
                cur.execute(
                    'INSERT INTO user_bike (user_name, user_password, user_type) VALUES (%s, %s, %s)',
                    (username, generate_password_hash(password), user_type)
                )
                cur.execute(
                    'DELETE FROM key_list WHERE secret_key = %s',(secret_code,)
                )
                
                cur.close()
                conn.commit()
                return redirect(url_for('login'))
            
    return render_template('auth/tec_reg.html')
   
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
