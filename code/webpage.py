from flask import (
    Flask, render_template, request, redirect, flash, url_for, session, g
)
# from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from bokeh.embed import server_document
import subprocess

from psycopg2 import connect
import platform

import downloadStation
import realtime_data

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
    
downloadStation
realtime_data

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


def bash_command(cmd):
    subprocess.Popen(cmd, shell=True)
    
# check Operating System
if platform.system() == 'Windows':  
    bash_command('bokeh serve ./statistics.py --allow-websocket-origin=127.0.0.1:5000')
elif platform.system() == 'Darwin':  
    bash_command('bokeh serve ./statistics.py --allow-websocket-origin=localhost:5000')
else:
    bash_command('bokeh serve ./statistics.py --allow-websocket-origin=localhost:5000')

@app.route("/statistics")
def statistics():
    script=server_document("http://localhost:5006/statistics")
    print(script)
    return render_template('hello.html',bokS=script)
   
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
