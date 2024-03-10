import smtplib
from email.message import EmailMessage


# Creditials
# login with google app password since less secure app of google discontinue fom may 30 2022
sender = 'sendmail259@gmail.com'
#password = '123456789hello'
password='vdqnykmqrbymzimk'

def sendmail(emailid,token):
    receiver = emailid
    try:
        # creating email format:
        message = EmailMessage()
        message['Subject'] = "Welcome to YTAnalytics -- Login!!"
        message['From'] = sender
        message['To'] = receiver
        body = f"Hello!!\nWelcome to YTAnalytics!!\nThank you for visiting our website.\nWe have also sent you a confirmation email, please confirm your email address in order to activate your account.\nThanking you,\nYTAnalytics"


        # no need subtype for plain text
        message.set_content(body, subtype='html')

        # creating smtp object
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # tts-transfer layer security improved version of ssl
        server.starttls()
        
        server.login(sender, password)
        # sending mail to target
        server.send_message(message)
        # quiting session
        server.quit()

        
        return True
    except:
        
        print("Error: unable to send email")
        return False
