from datetime import date
import os
import random
from Model.userData import Admin
from app import Flask_app
from config import db, bcrypt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
 
 
 
def addsuperadmin():
    with Flask_app.app_context():
        try:
            email = 'sravanchekuri449@gmail.com'
            dbuser = Admin.query.filter(Admin.EMAIL_ID == email).all()
            # if dbuser:
            #     print('Admin details already exist')
            #     return 'Admin details already exist'
            # print('dbuser',dbuser)
            if not dbuser:
                password1 = ''.join(chr(random.randint(97, 122)) for _ in range(15))
                hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
               
                details = Admin(
                    USER_ID = 10001,
                    FIRST_NAME = 'AdminFN',
                    MIDDLE_NAME = 'AdminMN',
                    LAST_NAME = 'AdminLN',
                    EMAIL_ID = email,
                    PASSWORD = hashed_password,
                    MOBILE_NUMBER = '9873765983',
                    ROLE = 'Admin',
                    EFFECTIVE_START_DATE = date.today(),
                    EFFECTIVE_END_DATE = '4712-12-31',
                    CREATED_BY = 'HR',
                    LAST_UPDATED_BY = 'HR'
                )
               
                fromEmail = os.environ.get("SMTP_EMAIL")
                password = os.environ.get("SMTP_PASSWORD")
               
                msg = MIMEMultipart()
                msg['From'] = fromEmail
                msg['To'] = email
                body = f'Your User id for LOGIN is: 10001 and Password :{password1} '
                msg['Subject'] = 'LOGIN CREDENTIALS'
                msg.attach(MIMEText(body, 'plain'))
                server = smtplib.SMTP(os.environ.get("SMTP_SERVER"), os.environ.get("SMTP_PORT"))
                server.starttls()
               
                server.login(fromEmail, password)
                           
                server.sendmail(fromEmail, email, msg.as_string())
                server.quit()
               
                db.session.add(details)
                db.session.commit()
               
                print('Registration successful and login credentials sent to respective mail')
                return 'Registration successful and login credentials sent to respective mail'
           
        except Exception as e:
            print({'error':str(e)})