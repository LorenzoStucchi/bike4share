from flask import (
    Flask, render_template, request, redirect, flash, url_for, session, g
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from psycopg2 import (
        connect
)

import geopandas as gpd
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet, Select
from bokeh.plotting import figure, show, output_file
#from bokeh.tile_providers import get_provider, Vendors #bokeh version 1.1
from bokeh.tile_providers import CARTODBPOSITRON #bokeh version 1.0
from bokeh.io import curdoc
from bokeh.layouts import column, row

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
    

        
        
# Create a URL route in our application for "/"
@app.route('/')
@app.route('/index')
def index():
    conn = get_dbConn()
    cur = conn.cursor()
    cur.close()
    conn.commit()
    load_logged_in_user()

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

#MAP VISUALIZATION
@app.route('/bike_stations')
def bike_stations():
    conn = get_dbConn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM stations')
    stations = cur.fetchall()
    #stations_df = pd.DataFrame(stations)
    #df.columns = stations.keys()
    stations_df = pd.DataFrame(stations, columns=['ID','BIKE_SH','INDIRIZZO','STALLI','LOCALIZ','x','y'])
 

    #Use the dataframe as Bokeh ColumnDataSource
    psource = ColumnDataSource(stations_df)
   
    #Specify feature of the Hoover tool
    TOOLTIPS = [
        ("name", "@INDIRIZZO"),
        ("capacity", "@STALLI")
    ]
    
    #Create the Map plot
    # range bounds supplied in web mercator coordinates
    p1 = figure(x_range=(1020414, 1024954), y_range=(5692309, 5698497),
               x_axis_type="mercator", y_axis_type="mercator", tooltips=TOOLTIPS)
    
    #Add basemap tile
    #p1.add_tile(get_provider(Vendors.CARTODBPOSITRON)) #bokeh version 1.1 
    p1.add_tile(CARTODBPOSITRON) #bokeh version 1.0
    
    
    #Add Glyphs
    p1.circle('x', 'y', source=psource, color='red', radius=10)
    
    #Add Labels and add to the plot layout
    # use css as render mode for html 
    labels = LabelSet(x='x', y='y', text='ID', level="glyph",x_offset=5, y_offset=5, source=psource, render_mode='css')
    		  
    p1.add_layout(labels)
  
    #Create the plot layout
    
    layout = row(p1)
    output_file("templates/auth/bike_stations.html")
    show(layout)
    curdoc().add_root(layout)
    return render_template('auth/bike_stations.html')

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
