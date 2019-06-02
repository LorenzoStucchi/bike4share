from flask import (
    Flask, render_template, request, redirect, flash, url_for, session, g
)
# from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from bokeh.embed import server_document
import subprocess

from psycopg2 import connect
import platform
import os

import downloadStation
#import realtime_data
from post import mail_sender


# Create the application instance
app = Flask(__name__, template_folder="templates")
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.urandom(24) 

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
#realtime_data

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
    load_logged_in_user()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']   
        user_mail= request.form['user_mail']
        user_type = 'u'
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not user_mail:
            error = 'E-mail is required.'
            
        else :
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
            'SELECT user_id FROM user_bike WHERE user_name = %s', (username,))
            if cur.fetchone() is not None:
                error = 'User {} is already registered, please change your username'.format(username)
                cur.close()

        if error is None:
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO user_bike (user_name, user_password, user_mail, user_type) VALUES (%s, %s, %s, %s)',
                (username, generate_password_hash(password), user_mail, user_type)
            )
            cur.close()
            conn.commit()
            return redirect(url_for('login'))

        flash(error)

    return render_template('auth/register.html')

#TECH REGISTRATION
@app.route('/tec_reg', methods=('GET', 'POST'))
def tec_reg():
    load_logged_in_user()
    if request.method =='POST':
        secret_code = request.form['secret_code']
        username = request.form['username']
        password = request.form['password']
        user_mail= request.form['user_mail']
        
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
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not user_mail:
            error = 'E-mail is required.'
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
            user_type = 't'
            cur.execute(
                'INSERT INTO user_bike (user_name, user_password, user_mail, user_type) VALUES (%s, %s, %s, %s)',
                (username, generate_password_hash(password), user_mail, user_type)
            )
            cur.execute(
                'DELETE FROM key_list WHERE secret_key = %s',(secret_code,)
            )
            cur.close()
            conn.commit()
            error = "Tecnician regitration done!"
            return redirect(url_for('login'))

        flash(error)
        
    return render_template('auth/tec_reg.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    load_logged_in_user()
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
            error ='The username {} does not exist.'.format(username)
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

#FORGOT PASSWORD: it allows to recovery the forgotten password
@app.route('/forgotpassword', methods=('GET', 'POST'))
def forgotpassword():
   if request.method == 'POST':
       mail_lostp = request.form['user_mail']
       error = None
       if not mail_lostp:
           error = 'E-mail is required for the Password Recovery'
       else :
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
            'SELECT user_mail FROM user_bike WHERE user_mail = %s', (mail_lostp,))
            user = cur.fetchone()
            if user is None:
                error = 'E-mail {} is not present, please check it or make the registration procedure again'.format(mail_lostp)
            cur.close()
        
       if error is None:

             conn = get_dbConn()
             cur = conn.cursor()
             rec_password=mail_sender(mail_lostp)
             error = 'Email is sent to {} check in your inbox or SPAM folder'.format(mail_lostp)                            
             print('Added secret psw for recovery password', (rec_password,))
             cur.close()
        
       flash(error)
   return render_template('auth/forgotpassword.html')

#@app.route('/set_new_password', methods=('GET', 'POST'))
#def set_new_password():
#    load_logged_in_user()
#    if request.method =='POST':
#        given_code = request.form['psw_recovery']
#        username = request.form['username']
#        new_password = request.form['new_password']
#        conn = get_dbConn()
#        cur = conn.cursor()
#        error = None
#        cur.execute(
#            'SELECT * FROM password_recovery WHERE psw_recovery = %s', (given_code,)
#        )
#        p_r = cur.fetchone()
#        cur.close()
#        conn.commit()
#        
#        if p_r is None:
#            error = ' Incorrect secret key, Please follow the Forgot Password procedure to obtain it.'
#            flash(error)
#        elif not username:
#            error = 'Username is required.'
#        elif not new_password:
#            error = 'New password is required.'
#            
#        else :
#            conn = get_dbConn()
#            cur = conn.cursor()
#            cur.execute(
#            'SELECT user_id FROM user_bike WHERE user_name = %s', (username,))
#            
#        
#        if error is None:
#            conn = get_dbConn()
#            cur = conn.cursor()                        
#            cur.execute(                    
#                'INSERT INTO user_bike (user_name, user_password)  VALUES (%s,%s)' , (username, new_password,))
#            cur.execute(
#                'DELETE FROM password_recovery WHERE psw_recovery = %s',(given_code,)
#            cur.close()
#            conn.commit()
#            error = "new password is been set!"
#            return redirect(url_for('login'))
#
#        flash(error)
#        
#    return render_template('auth/forgotpassword.html')
        

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

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
    load_logged_in_user()
    script=server_document("http://localhost:5006/statistics")
    print(script)   
    return render_template('statistics.html',bokS=script)
   
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
