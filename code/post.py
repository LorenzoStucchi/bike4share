#function that allow to send an email, it'll take the address of the users automatically
def mail_sender(send_mail_to):  
    import smtplib
    object= "Subject:bike4share Password Recovery!\n\n"
    content="Here you can find your password:"
    message= object + content
    email = smtplib.SMTP("smtp.gmail.com",587)
    email.ehlo()
    email.starttls()
    email.login("bike4sharepolimi@gmail.com","safelollobike4share")
    email.sendmail("bike4sharepolimi@gmail.com",send_mail_to, message)
    email.quit()