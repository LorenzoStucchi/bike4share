# -*- coding: utf-8 -*-
"""
Created on Wed May 29 19:38:41 2019

@author: Federica Vaghi
"""
    
    #FORGOT PASSWORD: it allows to recovery the forgotten password
@app.route('/ForgotPassword', methods=('GET', 'POST'))
def ForgotPassword():
    if request.method == 'POST':
       user_mail= request.form['user_mail']
       error = None
       
    if not user_mail:
           error = 'E-mail is required for the Password Recovery'
            
    else :
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
            'SELECT user_mail FROM user_bike WHERE user_mail = %s', (user_mail,))
            if    cur.fetchone() is not None:
                  sendmail=cur.fetchone()
                  cur.close()
                  conn.commit()
                  
            elif  cur.fetchone() is not None:
                  error = 'E-mail {} is not present, please check it or make the registration procedure again'.format(user_mail)
                  cur.close()
                  flash(error)
                  return render_template('auth/ForgotPassword.html')
    if error is None:
            post(sendmail)
#function that allow to send an email, it'll take the address of the users automatically
def post():  
    import smtplib
#    if request.method == 'POST':
#        user_mail = request.form['user_mail']
#        password = request.form['password']
#    conn = get_dbConn()
#    cur = conn.cursor()
#    cur.execute(
#                'SELECT password FROM user_bike WHERE user_mail = %s', (password,user_mail,))             
#    cur.close()
#    conn.commit()
    send_mail_to='sendmail'
    object= "Subject:bike4share Password Recovery!\n\n"
    content="Here you can find your password:"
    message= object + content
    email = smtplib.SMTP("smtp.gmail.com",587)
    email.ehlo()
    email.starttls()
    email.login("bike4sharepolimi@gmail.com","safelollobike4share")
    email.sendmail("bike4sharepolimi@gmail.com",send_mail_to, message)
    email.quit()
#POSTINO FUNZIONANTE    
#    def post():
#    import smtplib
#    send_mail_to='fede94chicca@hotmail.it'
#    object= "Subject:Password Recovering!\n\n"
#    content="Here you can find the new password:"
#    message= object + content
#    email = smtplib.SMTP("smtp.gmail.com",587)
#    email.ehlo()
#    email.starttls()
#    email.login("bike4sharepolimi@gmail.com","safelollobike4share")
#    email.sendmail("bike4sharepolimi@gmail.com",send_mail_to,message)
#    email.quit()