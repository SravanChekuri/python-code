from base64 import encode
from datetime import timedelta
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy import func
from flask import jsonify, request, session
from config import db
from Model.userData import *
# import bcrypt
from config import db, bcrypt
from werkzeug.security import generate_password_hash,check_password_hash
import re
import random
import smtplib
import ssl
from email.message import EmailMessage
import os



# def addadmin():
#     print("fghjk")
#     data = request.json
#     print("data",data)
#     try:
#         # password1 = ''
#         # for i in range(15):
#         #     pswchar = chr(random.randint(65, 122))
#         #     password1 = password1+pswchar
#         password1 = ''.join(chr(random.randint(97, 122)) for _ in range(15))
#         # password1 = uuid.uuid4()
#         print('password1',password1,ord('a'),ord('z'))
#         # hashed_password = bcrypt.hashpw(request.json['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#         # hashed_password = bcrypt.generate_password_hash(data['Password']).decode('utf-8')#[:10]
#         # print('hashed_password',hashed_password)
#         hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
#         user_id = data['User_Id']
#         dbdata = Admin.query.filter_by(USER_ID = user_id).first()
#         if dbdata:
#             return jsonify({"message": f'user id {user_id} already exist'}),400
#         email = data['Email_Id']
#         dbemail = Admin.query.filter_by(EMAIL_ID = email).first()
#         if dbemail:
#             return jsonify({"message": f'email {email} already exist'}),400
#         mobile_number = data['Mobile_Number']
#         dbnum = Admin.query.filter_by(MOBILE_NUMBER = mobile_number).first()
#         if dbnum:
#             return jsonify({"message": f'mobile number {mobile_number} already exist'}),400
#         returndata =[]
#         details = Admin(
#                          USER_ID = data['User_Id'],
#                          FIRST_NAME = data['First_Name'],
#                          MIDDLE_NAME = data['Middle_Name'],
#                          LAST_NAME = data['Last_Name'],
#                          EMAIL_ID = data['Email_Id'],
#                          PASSWORD = hashed_password,
#                          MOBILE_NUMBER = data['Mobile_Number'],
#                          ROLE = data['Role'],
#                          EFFECTIVE_START_DATE = data['Effective_Start_Date'],
#                          EFFECTIVE_END_DATE = data['Effective_End_Date'],
#                          CREATED_BY = 'HR',
#                          LAST_UPDATED_BY = 'HR')
       
 
#         try:
#             sessiondata ={}
#             sessiondata[email] = {
#                     'USER_ID': data['User_Id'],
#                     'PASSWORD': password1#data['Password']
#                     }
 
#             fromEmail = os.environ.get("SMTP_EMAIL")
#             password = os.environ.get("SMTP_PASSWORD")
 
#             msg = MIMEMultipart()
#             msg['From'] = fromEmail
#             msg['To'] = email
#             body = f'Your User id for LOGIN is: {user_id} and Password :{password1} '
#             msg['Subject'] = 'LOGIN CREDENTIALS'
#             msg.attach(MIMEText(body, 'plain'))
#             server =smtplib.SMTP(os.environ.get("SMTP_SERVER"), os.environ.get("SMTP_PORT"))
#             server.starttls()
           
#             server.login(fromEmail,password)
                       
#             server.sendmail(fromEmail, email, msg.as_string())
#             print(server)
#             server.quit()
#             # session.clear()
#             print(sessiondata)
#         except Exception as e:
#             return jsonify({'error':str(e)}),500
#         # return jsonify({'message': f'OTP sent to your mail--{otp}'})
#         temp = {
#                 "User_Id" : details.USER_ID,
#                 "First_Name" : details.FIRST_NAME,
#                 "Middle_Name" : details.MIDDLE_NAME,
#                 "Last_Name" : details.LAST_NAME,
#                 "Email_Id" : details.EMAIL_ID,
#                 "Mobile_Number" : details.MOBILE_NUMBER,
#                 "Role" : details.ROLE,
#                 "Effective_Start_Date" : datetime.strptime(str(details.EFFECTIVE_START_DATE),'%Y-%m-%d'),
#                 "Effective_End_Date" : datetime.strptime(str(details.EFFECTIVE_END_DATE),'%Y-%m-%d')
#             }
#             # details.EFFECTIVE_START_DATE = details.EFFECTIVE_START_DATE.strftime('%Y-%m-%d')
#             # details['EFFECTIVE_START_DATE']=details['EFFECTIVE_START_DATE'].
#         returndata.append(temp)
 
#         db.session.add(details)
#         db.session.commit()
 
#         # return jsonify({'details': details.serialize()}), 201
#         return jsonify({'message':'Registration successful and login credentials send to respected mail','data': returndata}), 201
#     except Exception as e:
#         return jsonify({'error':str(e)}),500
def addUser():
 
    data = request.json
    try:
        # token =
        # password1 = ''
        # for i in range(15):
        #     pswchar = chr(random.randint(65, 122))
        #     password1 = password1+pswchar
        password1 = ''.join(chr(random.randint(97, 122)) for _ in range(15))
        # password1 = uuid.uuid4()
        print('password1',password1,ord('a'),ord('z'))
        # hashed_password = bcrypt.hashpw(request.json['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # hashed_password = bcrypt.generate_password_hash(data['Password']).decode('utf-8')#[:10]
        # print('hashed_password',hashed_password)
        hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
        user_id = data['User_Id']
        dbdata = Admin.query.filter_by(USER_ID = user_id).first()
        if dbdata:
            return jsonify({"message": f'user id {user_id} already exist'}),400
        email = data['Email_Id']
        dbemail = Admin.query.filter_by(EMAIL_ID = email).first()
        if dbemail:
            return jsonify({"message": f'email {email} already exist'}),400
        mobile_number = data['Mobile_Number']
        dbnum = Admin.query.filter_by(MOBILE_NUMBER = mobile_number).first()
        if dbnum:
            return jsonify({"message": f'mobile number {mobile_number} already exist'}),400
        returndata =[]
        details = Admin(
                         USER_ID = data['User_Id'],
                         FIRST_NAME = data['First_Name'],
                         MIDDLE_NAME = data['Middle_Name'],
                         LAST_NAME = data['Last_Name'],
                         EMAIL_ID = data['Email_Id'],
                         PASSWORD = hashed_password,
                         MOBILE_NUMBER = data['Mobile_Number'],
                         ROLE = data['Role'],
                         EFFECTIVE_START_DATE = data['Effective_Start_Date'],
                         EFFECTIVE_END_DATE = data['Effective_End_Date'],
                         CREATED_BY = 'HR',
                         LAST_UPDATED_BY = 'HR')
       
 
        try:
            sessiondata ={}
            sessiondata[email] = {
                    'USER_ID': data['User_Id'],
                    'PASSWORD': password1#data['Password']
                    }
 
            fromEmail = os.environ.get("SMTP_EMAIL")
            password = os.environ.get("SMTP_PASSWORD")
 
            msg = MIMEMultipart()
            msg['From'] = fromEmail
            msg['To'] = email
            body = f'Your User id for LOGIN is: {user_id} and Password :{password1} '
            msg['Subject'] = 'LOGIN CREDENTIALS'
            msg.attach(MIMEText(body, 'plain'))
            server =smtplib.SMTP(os.environ.get("SMTP_SERVER"), os.environ.get("SMTP_PORT"))
            server.starttls()
           
            server.login(fromEmail,password)
                       
            server.sendmail(fromEmail, email, msg.as_string())
            print(server)
            server.quit()
            # session.clear()
            print(sessiondata)
        except Exception as e:
            return jsonify({'error':str(e)}),500
        # return jsonify({'message': f'OTP sent to your mail--{otp}'})
        temp = {
                "User_Id" : details.USER_ID,
                "First_Name" : details.FIRST_NAME,
                "Middle_Name" : details.MIDDLE_NAME,
                "Last_Name" : details.LAST_NAME,
                "Email_Id" : details.EMAIL_ID,
                "Mobile_Number" : details.MOBILE_NUMBER,
                "Role" : details.ROLE,
                "Effective_Start_Date" : datetime.strptime(str(details.EFFECTIVE_START_DATE),'%Y-%m-%d'),
                "Effective_End_Date" : datetime.strptime(str(details.EFFECTIVE_END_DATE),'%Y-%m-%d')
            }
            # details.EFFECTIVE_START_DATE = details.EFFECTIVE_START_DATE.strftime('%Y-%m-%d')
            # details['EFFECTIVE_START_DATE']=details['EFFECTIVE_START_DATE'].
        returndata.append(temp)
 
        db.session.add(details)
        db.session.commit()
 
        # return jsonify({'details': details.serialize()}), 201
        return jsonify({'message':'Registration successful and login credentials send to respected mail','data': returndata}), 201
    except Exception as e:
        return jsonify({'error':str(e)}),500

# login and token authentication[POST Method]
import jwt
def login():
    data = request.json
    try:
        user_Id=data['User_Id']
        user = Admin.query.filter_by(USER_ID=user_Id).first()
        SECRET_KEY = user_Id
        print(data['Password'])
        if user:
            if bcrypt.check_password_hash(user.PASSWORD, data['Password']):              
                expiration_time = datetime.utcnow() + timedelta(hours=1)
                
                payload = {'email': user.EMAIL_ID, 'User_Id': user.USER_ID, 'role':user.ROLE, 'exp': expiration_time}

                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                return jsonify({'message': 'Login successful', 'User_Id': user.USER_ID, 'Username':user.FIRST_NAME, "token": token})
            else:
                return jsonify({'error': 'Please enter valid Password'}), 401
        else:
            return jsonify({'error': 'User not found with entered user ID'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


# generate otp and send to email[POST Method]
sessiondata = {}
def email():
    try:
        data = request.json
        toEmail = data['Email_Id']
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if  not re.match(email_pattern, toEmail):
            return jsonify({'message': 'Invalid email pattern'}),400
        else:
            emaildb = Admin.query.filter_by(EMAIL_ID = toEmail).first()
            if not emaildb:
                return jsonify({'message':f' {toEmail} does not match any User'}), 400
            else:
 
 
                otp = str(random.randint(100000, 999999))
 
                expiration_time = datetime.now() + timedelta(minutes=1)
 
                sessiondata[toEmail] = {
                'otp': otp,
                'otp_expiry': expiration_time,  # Store current timestamp
                'email': toEmail
                }
 
                fromEmail = os.environ.get("SMTP_EMAIL")
                password = os.environ.get("SMTP_PASSWORD")
 
                msg = MIMEMultipart()
                msg['From'] = fromEmail
                msg['To'] = toEmail
                body = f'Your OTP for password reset is: {otp}'
                msg.attach(MIMEText(body, 'plain'))
                server =smtplib.SMTP(os.environ.get("SMTP_SERVER"), os.environ.get("SMTP_PORT"))
                server.starttls()
               
                server.login(fromEmail,password)
                           
                server.sendmail(fromEmail, toEmail, msg.as_string())
                print(server)
                server.quit()
                # session.clear()
                print(sessiondata)
                return jsonify({'message': 'OTP sent to your mail'})
       
    except Exception as e:
        return jsonify({'error':str(e)}),500



def verify():
    try:
        data = request.json
        print('data:',data,"sessiondata:", sessiondata)
        user_otp = data.get('OTP')  # Retrieve the OTP from the request data
        user_email = data.get('Email_Id')
        print("user_otp",user_otp)
        print("user_email",user_email)
    
        if sessiondata:
            print("session:",sessiondata)
            for user_data in sessiondata.values():
                stored_otp = user_data['otp']
                stored_email = user_data.get('email')
                print('stored_otp: ',stored_otp)
                otp_expiry = user_data.get('otp_expiry').replace(tzinfo=None)   #remove timezone information
                current_time = datetime.now()
                print("stored_email ,user_email",stored_email ,user_email)
                if stored_email == user_email:
                    if stored_otp == user_otp:
                        if otp_expiry and current_time < otp_expiry:
                            sessiondata.pop(user_data['email'])
                        # OTP matched and not expired
                            return jsonify({"message": "OTP verification Successful"}), 200
                        else:
                            return jsonify({'message': "OTP Expired"}), 500
    
                    else:
                        return jsonify({'message': "Invalid OTP"}), 400
                        # OTP expired
                else:              
                    return jsonify({'message': "Invalid email"}), 500
        else:
            # No OTP found in the session
            return jsonify({'message': "Invalid OTP"}), 404
    except Exception as e:
        return jsonify ({"error":str(e)}),500



def changePassword():
    try:
        get = request.json
        Email = get['Email_Id']
        print("Email",Email)
        data = Admin.query.filter_by(EMAIL_ID = Email).one()
        print("dfghjkllkjhgfdh")
        if data.EMAIL_ID != Email:
            return jsonify({'error': 'Invalid email'})
       
        print("data",data)  
        hashed_password = bcrypt.generate_password_hash(request.json['Password']).decode('utf-8')
        print("dfgyuioihg")
        data.PASSWORD = hashed_password
        print("dfghjukojb gtgfbhj")
        db.session.commit()
        return jsonify({'message': 'password changed successfully'}),200
 
    except Exception as e:
        return jsonify ({'error':str(e)}),500


    

# get all users[GET Method]
def getadmin():
    try:
        get=Admin.query.all()
        returndata=[]
        if not get:
            return jsonify({'message': f'user {id} not found'}),404
        for i in get:
            returndata.append(i.serialize())
        return jsonify({'data': returndata}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    

# get user by id[GET Method]
def getadmin_id(id):
    try:
        User =Admin.query.get(id)
        print('User',User)
        if not User:
            return jsonify({'message': f'User {id} not found'}),404
        print("person.serialize()",User.serialize())
        return jsonify({'data' : User.serialize()}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    
    
    
# update user details by id[PUT Method]
def updateadmin_details(id):
    try:
        a=Admin.query.get(id)
        data=request.json

        updateData = {
            'FIRST_NAME': data.get('First_Name'),
            'MIDDLE_NAME': data.get('Middle_Name'),
         'LAST_NAME': data.get('Last_Name'),
         'EMAIL_ID': data.get('Email_Id'),
         'MOBILE_NUMBER': data.get('Mobile_Number'),
         'ROLE': data.get('Role'),
         'CREATED_BY': data.get('Created_By'),
         'LAST_UPDATED_BY': data.get('Last_Updated_By')}
         
        if not a:
            return jsonify({'message':f'user {id} not found'}),404
        for i in updateData:
            cap = i.title()

            # if i != data['password'] and data['employee_Id']:
            new_value = data.get(cap),
            if getattr(a,i) != new_value:
                
                setattr(a,i,new_value)
        

        db.session.commit()
        return jsonify({'data':a.serialize()}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500  
    

# delete employee
def deleteadmin(id):
    try:
        data = Admin.query.get(id)
        
        if not data:
            return jsonify({'message': 'user not found'}),404
        print("data.serialize()",data.serialize())
        db.session.delete(data)
        db.session.commit()
        return jsonify({'data' : data.serialize()}),200
        
    except Exception as e:
        return jsonify({'error':str(e)}),500 

    