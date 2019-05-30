# -*- coding: utf-8 -*-
"""
Created on Wed May 29 19:38:41 2019

@author: Federica Vaghi
"""
def post():
    import smtplib
    receiver='fede94chicca@hotmail.it'
#   reciever= session.get('user_mail')  #l'idea è di prendere l'indirizzo e-mail dal database
#    if receiver is None:
#        g.mail = None
#    else:
#        conn = get_dbConn()
#        cur = conn.cursor()
#        cur.execute(
#            'SELECT * FROM user_bike WHERE user_password = %s', (user_password,)
#        )
#        g.mail = cur.fetchone()
#        cur.close()
#        conn.commit()
    object= "Subject:Password Recovering!\n\n"
    content="Here you can find the new password"
    message= object + content
    email = smtplib.SMTP("smtp.gmail.com",587)
    email.ehlo()
    email.starttls()
    email.login("bike4sharepolimi@gmail.com","safelollobike4share")
    email.sendmail("bike4sharepolimi@gmail.com",receiver,message)
    email.quit()