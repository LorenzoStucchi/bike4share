# -*- coding: utf-8 -*-
"""
Created on Wed May 29 19:38:41 2019

@author: Federica Vaghi
"""
    

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