#function that allow to send an email, it'll take the address of the users automatically
def mail_sender(send_mail_to, rec_password):  
    import smtplib
    rec_password= ''.join(rec_password)
    object= "Subject:bike4share Password Recovery!\n\n"
    content="Hello there! Here you can find the code for the bike4share recovery password:" 
    message= object + content + rec_password
    email = smtplib.SMTP("smtp.gmail.com",587)
    email.ehlo()
    email.starttls()
    email.login("bike4sharepolimi@gmail.com","safelollobike4share")
    email.sendmail("bike4sharepolimi@gmail.com",send_mail_to, message)
    email.quit()