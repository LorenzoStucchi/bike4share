#function that allow to send an email, it'll take the address of the users automatically
def mail_sender(send_mail_to,rec_password):  
    import smtplib
    print('Added secret psw for recovery password', (rec_password,))
    rec_password= ''.join(rec_password)
    object= "Subject:bike4share Password Recovery!\n\n"
    content="Hello there! Here you can find the code for the bike4share recovery password: \n" 
    message= object + content + rec_password
    email = smtplib.SMTP("smtp.gmail.com",587)
    email.ehlo()
    email.starttls()
    email.login("bike4sharepolimi@gmail.com","safelollobike4share")
    email.sendmail("bike4sharepolimi@gmail.com",send_mail_to, message)
    email.quit()
    

#KEY GENERATOR
def key_generator(leng):
    import random
    arr = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!£$%&()=?^"
    psw = ""
    x = 0
    for x in range(int(leng)):
        psw += arr[int(random.randrange(len(arr)))]
        x += 1
    return psw