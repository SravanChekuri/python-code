from base64 import encode
from datetime import date, timedelta
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import pandas as os

from sqlalchemy import func
from flask import jsonify, request, send_file, session
from config import db
from Model.employeeData import *
from Model.empProfile import *
from Model.userData import Admin

# import bcrypt
from config import db, bcrypt
from werkzeug.security import generate_password_hash,check_password_hash
import re
import random
import smtplib
import ssl
from email.message import EmailMessage
import os

from sqlalchemy.exc import IntegrityError
from types import NoneType




    
# add employee details[POST Method]
def addEmployee():
    try:
        print("fgbhnjm,")
        data = request.json
        print("data",data)
 
        # email pattern validation
        e_id = data.get('Email_Id')
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, e_id):
            email = e_id
        else:
            return jsonify ({'error' : 'Invalid email'}),400
        print("sdfgbh")
        # mobile pattern validation
        mobile_no = data['Mobile_No']
        mobile_pattern = r'^(\+\d{1,3}[- ]?)?\d{10}$'
        if re.match(mobile_pattern,mobile_no):
            mobilenum = mobile_no
        else:
            return jsonify ({"error": 'Please enter valid mobile number'}),400
        print("lkjhg")
        # checking mobile number in database
        mob_data = EMPLOYEE_DETAILS.query.filter_by(MOBILE_NO = mobile_no).first()
        if not mob_data:
            mobilenum = mobile_no
        else:
            return jsonify ({"error" : f'mobile number {mobile_no} already exist'}),400
        print("dfgbhnjm")
        # DOB validation
        DOB = data['Date_Of_Birth']  # Assuming date format is YYYY-MM-DD
        dob= datetime.strptime(DOB, '%Y-%m-%d')
        dob_year = dob.date().year
        today = datetime.today()
        this_year = today.date().year
        min_age = this_year - dob_year
        if min_age >= 18:
            d_o_b = DOB
        else:
            return jsonify({'error':f"You must be at least 18 years old."}),400
 
        # emlpoyee number validation  
        emp_no = data.get('Employee_Number')
        existing_empnum = EMPLOYEE_DETAILS.query.filter_by(EMPLOYEE_NUMBER = emp_no).first()
        if existing_empnum:
            return jsonify({'message':f'Employee Number {emp_no} already exist '}), 400
       
        # email validation
        existing_emp = EMPLOYEE_DETAILS.query.filter_by(EMAIL_ID = e_id).first()
        print("existing_emp",existing_emp)
        if existing_emp:
            return jsonify({'message':f'email {e_id} already exist '}), 400
   
        # required fields validation
        required_fields = ['Employee_Number','First_Name','Last_Name','Effective_Start_Date','Effective_End_Date','Worker_Type','Date_Of_Birth','Mobile_No','Job_Location','Email_Id']
        returnData = []
        if not data:
            return jsonify ({'error': 'data is required'}),400
        for i in required_fields:
            print("a",i)
            if i not in data:
                returnData.append(f'{i} is required')
 
                print("returnData",returnData)
               
        if returnData:
            return jsonify({'message':returnData}),400
       
       
        print("data.get('Effective_Start_Date')",type(data.get('Effective_Start_Date')))
        userEmail='sravanchekuri449@gmail.com'
        print(userEmail)
        user = Admin.query.filter_by(EMAIL_ID=userEmail).first()
        # user = Admin.query.get(1)
        print("user.USER_ID",user.USER_ID)
        details = EMPLOYEE_DETAILS(
           
                    EMPLOYEE_NUMBER = data['Employee_Number'],
                    FIRST_NAME = data['First_Name'],
                    MIDDLE_NAME = data['Middle_Name'],
                    LAST_NAME = data['Last_Name'],
                    DATE_OF_BIRTH = d_o_b,
                    WORKER_TYPE = data['Worker_Type'],
                    MOBILE_NO = mobilenum,
                    EFFECTIVE_START_DATE = data.get('Effective_Start_Date'),
                    EFFECTIVE_END_DATE = data.get('Effective_End_Date') if data.get('Effective_End_Date') else date(4712, 12, 31),
                    JOB_LOCATION = data['Job_Location'],
                    USER_ID = user.USER_ID,
                    EMAIL_ID =email,
                    CREATED_BY = 'HRName',
                    LAST_UPDATED_BY = "HRName")
 
        db.session.add(details)
        db.session.commit()
        print("details.serialize()",details.serialize())
        return jsonify({"message": f'{data['Employee_Number']} candidate added successfully','details': details.serialize()}), 201
           
    except Exception as e:
        return jsonify({'error':str(e)}),500



# add bulk employee details[POST Method]
# def addbulk():
#     try:
#         excel = request.files['EXCEL']
#         df = pd.read_excel(excel,sheet_name=0)
#         print("df[Name]",df)
#         # userEmail='sowmya@gmail.com'
#         # print(userEmail)
#         # user = Admin.query.filter_by(EMAIL_ID=userEmail).first()
#         # user = Admin.query.get(1)
 
       
       
#         returndata =[]
#         for index,row in df.iterrows():
#             e_id = row.get('Email_Id')
#             e_no = row.get('Employee_Number')
 
#             temp = row['Date_Of_Joining']
#             print("row",temp)
           
#             userEmail='sravanchekuri449@gmail.com'
#             print(userEmail)
#             user = Admin.query.filter_by(EMAIL_ID=userEmail).first()
#             # user = Admin.query.get(1)
#             print("user.USER_ID",user.USER_ID)
#             existing_emp = EMPLOYEE_DETAILS.query.filter_by(EMAIL_ID = e_id).all()
#             emp_no = EMPLOYEE_DETAILS.query.filter_by(EMPLOYEE_NUMBER = e_no).all()
#             print("existing_emp",existing_emp,emp_no)
#             if existing_emp:
#                 return jsonify({'message':f'email {e_id} already exist '}), 400
#             if emp_no:
#                 return jsonify({'message': f'employee number {e_no} already exist'}), 400
           
#             if type(row.get('Middle_Name')) != float:
#                 middleName = row.get('Middle_Name')
 
#             else:
#                 middleName = None
 
           
#             email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#             if re.match(email_pattern, row['Email_Id']):
#                 email = row['Email_Id']
#             else:
#                 return jsonify ({'error' : 'Invalid email'})
           
#             mobile = row['Mobile_No']
#             mobile_no = mobile.replace("-", "")
#             print("mobile_no",mobile_no)
#             mobile_pattern = r'^(\+\d{1,3}[- ]?)?\d{10}$'
#             if re.match(mobile_pattern,mobile_no):
#                 mobilenum = mobile_no
#             else:
#                 return jsonify ({"error": 'Please enter valid mobile number'}),400
           
#             mob_data = EMPLOYEE_DETAILS.query.filter_by(MOBILE_NO = mobile_no).first()
#             if not mob_data:
#                 mobilenum = mobile_no
#             else:
#                 return jsonify ({"error" : f'mobile number {mobile_no} already exist'}),400
#             print("dfghjkl")
           
#             # DOB validation
#             DOB = row['Date_Of_Birth']  # Assuming date format is YYYY-MM-DD
#             print("DOB",DOB)
#             # dob= datetime.strptime(DOB, '%Y-%m-%d')
#             # print("dob",dob)
#             dob_year = DOB.date().year
#             print("dob_year",dob_year)
#             today = datetime.today()
#             this_year = today.date().year
#             print("this_year",this_year)
#             min_age = this_year - dob_year
#             print("min_age",min_age)
#             if min_age >= 18:
#                 d_o_b = DOB
#             else:
#                 return jsonify({'error':f"You must be at least 18 years old."}),400
           
#             print("row['Effective_Start_Date']",row['Effective_Start_Date'])
#             # print("row['Date_Of_Joining']",row['Date_Of_Joining'])
#             # DOJ = row['Date_Of_Joining']
#             # ESD = row.get('Effective_Start_Date')
#             # if not DOJ == ESD:
#             #     return jsonify ({"message":f"Effective start date {ESD} must be Date of joining"}),400
#             # else:
#             details = EMPLOYEE_DETAILS(EMPLOYEE_NUMBER = row['Employee_Number'],
#                                     FIRST_NAME =row['First_Name'],
#                                     MIDDLE_NAME = middleName,
#                                     LAST_NAME =row['Last_Name'],
#                                     JOB_LOCATION =row['Job_Location'],
#                                     EFFECTIVE_START_DATE =row['Effective_Start_Date'],
#                                     MOBILE_NO = mobilenum,
#                                     DATE_OF_BIRTH = d_o_b,
#                                     USER_ID = user.USER_ID,
#                                     EFFECTIVE_END_DATE = '4712-12-31',
#                                     WORKER_TYPE = row['Worker_Type'],
#                                     #    USER_ID =user.USER_ID,
#                                     EMAIL_ID =email,
#                                     CREATED_BY = 'HR',
#                                     LAST_UPDATED_BY = 'HR')
#             print("sdvjvosvkm")
#             print("details['EFFECTIVE_START_DATE']",details.EFFECTIVE_START_DATE.strftime('%Y-%m-%d'))
#             temp = {
#                 "Employee_Id" : details.EMPLOYEE_ID,
#                 "Employee_Number" : details.EMPLOYEE_NUMBER,
#                 "First_Name" : details.FIRST_NAME,
#                 "Middle_Name" : details.MIDDLE_NAME,
#                 "Last_Name" : details.LAST_NAME,
#                 "Effective_Start_Date" : details.EFFECTIVE_START_DATE.strftime('%Y-%m-%d'),
#                 "Date_Of_Birth" : details.DATE_OF_BIRTH.strftime('%Y-%m-%d'),
#                 "Worker_Type" : details.WORKER_TYPE,
#                 "Mobile_No" : details.MOBILE_NO,
#                 "Effective_End_Date" : details.EFFECTIVE_END_DATE,
#                 "User_Id" : details.USER_ID,
#                 "Job_Location" : details.JOB_LOCATION,
#                 "Email" : details.EMAIL_ID
#             }
#             print("sdfghjk")
#             # details.EFFECTIVE_START_DATE = details.EFFECTIVE_START_DATE.strftime('%Y-%m-%d')
#             # details['EFFECTIVE_START_DATE']=details['EFFECTIVE_START_DATE'].
#             returndata.append(temp)
#             # break
 
#             db.session.add(details)
#             print("asdfghj")
#         db.session.commit()
#         print("returndata",returndata)
#         return jsonify({"message":"Bulk Upload Successfully",'details': returndata}), 201
           
           
#     # except IntegrityError as e:
#     #     return jsonify({'error': 'Unique key violation. This operation would result in duplicate data.'}), 400
#     except Exception as e:
#         return jsonify({'error':str(e)}),500

def addbulk():
    try:
        print("dfghjk")
        excel = request.files['EXCEL']
        print("excel",excel)
        if not excel:
            return jsonify({"error":"please select the excel file"}),400
        df = pd.read_excel(excel,sheet_name=0)
        print("df[Name]",df)
        userEmail='sravanchekuri449@gmail.com'
        print(userEmail)
        user = Admin.query.filter_by(EMAIL_ID=userEmail).first()
        print("user.USER_ID",user.USER_ID)
        returndata = []
        returndta =[]
        for index,row in df.iterrows():
            Employee_number = row.get('Employee_Number')
            e_emp = 'E' + Employee_number[1:]
            c_emp = 'C' + Employee_number[1:]
            dbdata = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == e_emp) |
                                                    (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == c_emp)).first()
            if dbdata:
                # email pattern validation
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if re.match(email_pattern, row['Email_Id']):
                        email = row.get('Email_Id')
                else:
                    return jsonify({"error":"Invalid email pattern"}),400
 
                print("row.get('Middle_Name')----->",row.get('Middle_Name'))
               
                if type(row.get('Middle_Name')) != float:
                    middleName = row.get('Middle_Name')
 
                else:
                    middleName = None
                print("type(row.get('Middle_Name'))",type(row.get('Middle_Name')),row.get('Middle_Name'))
           
                # DOB validation
                DOB = row['Date_Of_Birth']  # Assuming date format is YYYY-MM-DD
                # dob= datetime.strptime(DOB, '%Y-%m-%d')
                dob_year = DOB.date().year
                today = datetime.today()
                this_year = today.date().year
                min_age = this_year - dob_year
                if not min_age >= 18:
                    return jsonify({'error':f"You must be at least 18 years old."}),400
           
                # mobile pattern validation
                mobile = row['Mobile_No']
                mobile_no = mobile.replace("-", "")
                print("mobile_no",mobile_no)
                mobile_pattern = r'^(\+\d{1,3}[- ]?)?\d{10}$'
                if re.match(mobile_pattern,mobile_no):
                    mobilenum = mobile_no
                else:
                    return jsonify ({"error": 'Please enter valid mobile number'}),400
                mob_data = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.MOBILE_NO == mobile_no)).all()
                empf = row.get('Employee_Number')
                if mobile_no != dbdata.MOBILE_NO:
                    for i in mob_data:
                            empb = i.EMPLOYEE_NUMBER
                            if empf[1:] != empb[1:]:
                                return jsonify ({"error" : f'mobile number {mobile_no} already exist'}),400
                # emp_no = row.get('Emp_Number')
                get_emp = EMPLOYEE_DETAILS.query.filter(EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == row.get('Employee_Number')).first()
                print("get_emp......",get_emp)
                Employee_number = row.get('Employee_Number')
                Can_emp = 'C' + Employee_number[1:]
                if not get_emp:
                    get_Can = EMPLOYEE_DETAILS.query.filter(EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == Can_emp).first()
                    if get_Can:
                        print("updating candidate to employee")
                        # empf = row.get('Employee_Number')
                        # dta = EMPLOYEE_DETAILS.query.filter(
                        #                                     (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == row.get('Employee_Number')) &
                        #                                     (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= row.get('Effective_Start_Date')) &
                        #                                     (row.get('Effective_Start_Date') <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)
                        #                                 ).first()
   
                        print("get_Can----",get_Can)
                       
 
                   
                        email_data = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMAIL_ID == email)).all()
                        empfr = row.get("Employee_Number")
                        for i in email_data:
                                empb = i.EMPLOYEE_NUMBER
                                if empfr[1:] != empb[1:]:
                                    return jsonify ({"error" : f'email {email} already exist'}),400
                        dbESD = datetime.strptime(str(get_Can.EFFECTIVE_START_DATE), "%Y-%m-%d")
                        Datedb = str(row['Effective_Start_Date'])
                        print("Datedb",Datedb)
                        Dated = datetime.strptime(Datedb, "%Y-%m-%d %H:%M:%S")
                        print("Dated",Dated)
                        PrevEED = Dated - timedelta(days=1)
                        if dbESD >= Dated:
                            return jsonify({"message":"Effective Start Date shouldn't be earlier or same as candidate's Effective Start Date "})
                        elif dbESD < Dated:
                            get_Can.EFFECTIVE_END_DATE = PrevEED
                   
                        details = EMPLOYEE_DETAILS(
                                            EMPLOYEE_ID = dbdata.EMPLOYEE_ID,
                                            EMPLOYEE_NUMBER = row.get('Employee_Number') if row.get('Employee_Number') else dbdata.EMPLOYEE_NUMBER,
                                            FIRST_NAME = row.get('First_Name') if row.get('First_Name') else dbdata.FIRST_NAME,
                                            MIDDLE_NAME = middleName,# if data.get('Middle_Name') else dbdata.MIDDLE_NAME,
                                            LAST_NAME = row.get('Last_Name') if row.get('Last_Name') else dbdata.LAST_NAME,
                                            USER_ID = user.USER_ID,
                                            WORKER_TYPE = row.get('Worker_Type'),
                                            DATE_OF_BIRTH = row.get('Date_Of_Birth') if row.get('Date_Of_Birth') else dbdata.DATE_OF_BIRTH,
                                            MOBILE_NO = mobilenum if mobilenum else dbdata.MOBILE_NO,
                                            EFFECTIVE_START_DATE =  row['Effective_Start_Date'] if row['Effective_Start_Date'] else date.today(),
                                            EFFECTIVE_END_DATE = row['Effective_End_Date'] if row['Effective_End_Date'] else dbdata.EFFECTIVE_END_DATE ,
                                            JOB_LOCATION = row.get('Job_Location')if row.get('Job_Location') else dbdata.JOB_LOCATION,
                                            EMAIL_ID =email,
                                            CREATED_BY = 'HRName',
                                            LAST_UPDATED_BY = "HRName")
                        returndata.append(details)
                        returndta.append(details.serialize())
                        print("returndata(a)",returndata)
                if get_emp:
                    print("employee update")
                    dta = EMPLOYEE_DETAILS.query.filter(
                                                        (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == row.get('Employee_Number')) &
                                                        (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= row.get('Effective_Start_Date')) &
                                                        (row.get('Effective_Start_Date') <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)
                                                    ).first()
                    if Employee_number == dta.EMPLOYEE_NUMBER and email == dta.EMAIL_ID:
                        print("sdfghjkl;vbnm,")
                        print("dta",dta)
                        print("fields changing")
                        print("data",row)
                        dbESD = datetime.strptime(str(dta.EFFECTIVE_START_DATE), "%Y-%m-%d")
                        print("dbESD",dbESD)
                        Datedb = str(row['Effective_Start_Date'])
                        print("Datedb",Datedb)
                        Dated = datetime.strptime(Datedb, "%Y-%m-%d %H:%M:%S")
                        print("Dated",Dated)
                        if Dated == dbESD:
                            print("fields changing same day")
                            updateData = {
                                        'FIRST_NAME': row.get('First_Name'),
                                        'MIDDLE_NAME': middleName,
                                        'LAST_NAME': row.get('Last_Name'),
                                        'JOB_LOCATION': row.get('Job_Location'),
                                        'WORKER_TYPE': row.get('Worker_Type'),
                                        'EMAIL_ID': email,
                                        'DATE_OF_BIRTH' : row.get('Date_Of_Birth'),
                                        'MOBILE_NO' : mobilenum
                                    }
                            for key, value in updateData.items():
                                if getattr(dta, key) != value:
                                    setattr(dta, key, value)
                            db.session.commit()
                        if Dated != dbESD:
                            fdata = EMPLOYEE_DETAILS.query.filter(
                                                (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == row.get('Employee_Number'))&
                                                (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE > row.get('Effective_Start_Date'))
                                            ).order_by(EMPLOYEE_DETAILS.EFFECTIVE_START_DATE.asc()).first()
                            print("fields changing diff day")
                            print("middleName",middleName)
                   
                            print(fdata,"lkjnhbgvfc")
                            if not fdata:
                                print("inside else")
                                eed = row.get('Effective_End_Date')
                            else:
                                print("fdata",fdata)
                                fESD = datetime.strptime(str(fdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                                eed = fESD - timedelta(days=1)
                            dta = EMPLOYEE_DETAILS.query.filter(
                                                            (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == row.get('Employee_Number')) &
                                                            (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= row.get('Effective_Start_Date')) &
                                                            (row.get('Effective_Start_Date') <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)
                                                        ).first()
                            print("dta",dta)
                            Dated = str(row['Effective_Start_Date'])
                            print("Dated",Dated)
                            Datedb = datetime.strptime(Dated, "%Y-%m-%d %H:%M:%S")
                            print("Datedb",Datedb)
                            PrevEED = Datedb - timedelta(days=1)
                            dta.EFFECTIVE_END_DATE = PrevEED
                            details = EMPLOYEE_DETAILS(
                                                EMPLOYEE_ID = dbdata.EMPLOYEE_ID,
                                                EMPLOYEE_NUMBER = row.get('Employee_Number') if row.get('Employee_Number') else dbdata.EMPLOYEE_NUMBER,
                                                FIRST_NAME = row.get('First_Name') if row.get('First_Name') else dbdata.FIRST_NAME,
                                                MIDDLE_NAME = middleName,# if row.get('Middle_Name') else dbdata.MIDDLE_NAME,
                                                LAST_NAME = row.get('Last_Name') if row.get('Last_Name') else dbdata.LAST_NAME,
                                                USER_ID = user.USER_ID,
                                                WORKER_TYPE = row.get('Worker_Type') if row.get('Worker_Type') else dbdata.WORKER_TYPE,
                                                DATE_OF_BIRTH = row.get('Date_Of_Birth') if row.get('Date_Of_Birth') else dbdata.DATE_OF_BIRTH,
                                                MOBILE_NO = mobilenum if mobilenum else dbdata.MOBILE_NO,
                                                EFFECTIVE_START_DATE =  row['Effective_Start_Date'] if row['Effective_Start_Date'] else date.today(),
                                                EFFECTIVE_END_DATE = eed,
                                                JOB_LOCATION = row.get('Job_Location')if row.get('Job_Location') else dbdata.JOB_LOCATION,
                                                EMAIL_ID =email  if email else dbdata.EMAIL_ID,
                                                CREATED_BY = 'HRName',
                                                LAST_UPDATED_BY = "HRName")
                            returndata.append(details)
                            returndta.append(details.serialize())
   
                            print("returndata(b)",returndata)
                    if Employee_number == dta.EMPLOYEE_NUMBER and email != dta.EMAIL_ID:
                        print("lk,jhgfdfghjkl;lkjhgfdfghjkl;lkjhgccvbnm,")
                        empf = row.get('Employee_Number')
                        # emp[0] = 'C' or 'E'
                        # emp_num = emp[0] + emp[1:]
                        ddata = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMAIL_ID == email)& (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER != row.get('Employee_Number'))).all()
                        for i in ddata:
                            empb = i.EMPLOYEE_NUMBER
                            if empf[1:] != empb[1:]:
                                return jsonify({"error":f"email {email} already exist"}),400
 
                        # if ddata:
                        #     return jsonify({"error":f"email {email} already exist"}),400
                        else:
                            print("email changing")
                            # Dated = str(row['Effective_Start_Date'])
                            # Datedb = datetime.strptime(Dated, "%Y-%m-%d")
                            # dbESD = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                            dta = EMPLOYEE_DETAILS.query.filter(
                                                        (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == row.get('Employee_Number')) &
                                                        (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= row.get('Effective_Start_Date')) &
                                                        (row.get('Effective_Start_Date') <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)
                                                    ).first()
                            print("dta",dta)
                            dbESD = datetime.strptime(str(dta.EFFECTIVE_START_DATE), "%Y-%m-%d")
                            Datedb = str(row['Effective_Start_Date'])
                            print("Datedb",Datedb)
                            Dated = datetime.strptime(Datedb, "%Y-%m-%d %H:%M:%S")
                            print("Dated",Dated)
                            if Dated == dbESD:
                                print("email changing same day")
                                updateData = {
                                        'FIRST_NAME': row.get('First_Name'),
                                        'MIDDLE_NAME': middleName,
                                        'LAST_NAME': row.get('Last_Name'),
                                        'JOB_LOCATION': row.get('Job_Location'),
                                        'WORKER_TYPE': row.get('Worker_Type'),
                                        'EMAIL_ID': email,
                                        'DATE_OF_BIRTH' : row.get('Date_Of_Birth'),
                                        'MOBILE_NO' : mobilenum
                                    }
                                for key, value in updateData.items():
                                    if getattr(dta, key) != value:
                                        setattr(dta, key, value)
                                db.session.commit()
                   
                            # Dated = str(row['Effective_Start_Date'])
                            if Dated != dbESD:
                                print("email changing diff day")
                                dta = EMPLOYEE_DETAILS.query.filter(
                                                            (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == row.get('Employee_Number')) &
                                                            (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= row.get('Effective_Start_Date')) &
                                                            (row.get('Effective_Start_Date') <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)
                                                        ).first()
                                print("dta",dta)
                                # print("Dated",Dated)
                                # Datedb = datetime.strptime(row['Effective_Start_Date'], "%Y-%m-%d")
                                # print("Datedb",Datedb)
                                # dbESD = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                                Datedb = str(row['Effective_Start_Date'])
                                print("Datedb",Datedb)
                                Dated = datetime.strptime(Datedb, "%Y-%m-%d %H:%M:%S")
                                print("Dated",Dated)
                                PrevEED = Dated - timedelta(days=1)
                                dta.EFFECTIVE_END_DATE = PrevEED
                                fdata = EMPLOYEE_DETAILS.query.filter(
                                                (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == row.get('Employee_Number'))&
                                                (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE > row.get('Effective_Start_Date'))
                                            ).order_by(EMPLOYEE_DETAILS.EFFECTIVE_START_DATE.asc()).first()
                   
                                print(fdata,"lkjnhbgvfc")
                                if not fdata:
                                    print("inside else")
                                    eed = row.get('Effective_End_Date')
                                else:
                                    print("fdata",fdata)
                                    fESD = datetime.strptime(str(fdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                                    eed = fESD - timedelta(days=1)
                                print("row.get('Mobile_No')",row.get('Mobile_No'))
                                details = EMPLOYEE_DETAILS(
                                                    EMPLOYEE_ID = dbdata.EMPLOYEE_ID,
                                                    EMPLOYEE_NUMBER = row.get('Employee_Number') if row.get('Employee_Number') else dbdata.EMPLOYEE_NUMBER,
                                                    FIRST_NAME = row.get('First_Name') if row.get('First_Name') else dbdata.FIRST_NAME,
                                                    MIDDLE_NAME = middleName,# if row.get('Middle_Name') else dbdata.MIDDLE_NAME,
                                                    LAST_NAME = row.get('Last_Name') if row.get('Last_Name') else dbdata.LAST_NAME,
                                                    USER_ID = user.USER_ID,
                                                    WORKER_TYPE = row.get('Worker_Type') if row.get('Worker_Type') else dbdata.WORKER_TYPE,
                                                    DATE_OF_BIRTH = row.get('Date_Of_Birth') if row.get('Date_Of_Birth') else dbdata.DATE_OF_BIRTH,
                                                    MOBILE_NO = mobilenum if mobilenum else dbdata.MOBILE_NO,
                                                    EFFECTIVE_START_DATE =  row['Effective_Start_Date'] if row['Effective_Start_Date'] else date.today(),
                                                    EFFECTIVE_END_DATE = eed,
                                                    JOB_LOCATION = row.get('Job_Location')if row.get('Job_Location') else dbdata.JOB_LOCATION,
                                                    EMAIL_ID =email  if email else dbdata.EMAIL_ID,
                                                    CREATED_BY = 'HRName',
                                                    LAST_UPDATED_BY = "HRName")
                                returndata.append(details)
                                returndta.append(details.serialize())
                                print("returndata(c)",returndata)
 
            if not dbdata:
                print("adding candidate")
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if re.match(email_pattern, row['Email_Id']):
                        email = row.get('Email_Id')
                else:
                    return jsonify({"error":"Invalid email pattern"}),400
 
                print("row.get('Middle_Name')----->",row.get('Middle_Name'))
               
                if type(row.get('Middle_Name')) != float:
                    middleName = row.get('Middle_Name')
 
                else:
                    middleName = None
                print("type(row.get('Middle_Name'))",type(row.get('Middle_Name')),row.get('Middle_Name'))
           
                # DOB validation
                DOB = row['Date_Of_Birth']  # Assuming date format is YYYY-MM-DD
                # dob= datetime.strptime(DOB, '%Y-%m-%d')
                dob_year = DOB.date().year
                today = datetime.today()
                this_year = today.date().year
                min_age = this_year - dob_year
                if not min_age >= 18:
                    return jsonify({'error':f"You must be at least 18 years old."}),400
           
                # mobile pattern validation
                mobile = row['Mobile_No']
                mobile_no = mobile.replace("-", "")
                print("mobile_no",mobile_no)
                mobile_pattern = r'^(\+\d{1,3}[- ]?)?\d{10}$'
                if re.match(mobile_pattern,mobile_no):
                    mobilenum = mobile_no
                else:
                    return jsonify ({"error": 'Please enter valid mobile number'}),400
                mob_data = EMPLOYEE_DETAILS.query.filter(EMPLOYEE_DETAILS.MOBILE_NO == mobile_no).first()
                if mob_data:
                    return jsonify ({"error" : f'mobile number {mobile_no} already exist'}),400
                details = EMPLOYEE_DETAILS(EMPLOYEE_NUMBER = row['Employee_Number'],
                                    FIRST_NAME =row['First_Name'],
                                    MIDDLE_NAME = middleName,
                                    LAST_NAME =row['Last_Name'],
                                    JOB_LOCATION =row['Job_Location'],
                                    EFFECTIVE_START_DATE =row['Effective_Start_Date'],
                                    MOBILE_NO = mobilenum,
                                    DATE_OF_BIRTH = row.get('Date_Of_Birth'),
                                    USER_ID = user.USER_ID,
                                    EFFECTIVE_END_DATE = row.get('Effective_End_Date'),
                                    WORKER_TYPE = row['Worker_Type'],
                                    #    USER_ID =user.USER_ID,
                                    EMAIL_ID =email,
                                    CREATED_BY = 'HR',
                                    LAST_UPDATED_BY = 'HR')
               
                returndata.append(details)
                print("details",details)
                returndta.append(details.serialize())
 
        print("returndata",returndata)
        for i in returndata:
            db.session.add(i)
        # db.session.add(returndata)
        db.session.commit()
        return jsonify({"message":"success", "data":returndta}),201
    except Exception as e:
        return jsonify({'error':str(e)}),500

#update bulk
def bulk_update():
    try:
        excel = request.files['EXCEL']
        df = pd.read_excel(excel,sheet_name=0)
        print("df[Name]",df)
        userEmail='superadmin@gmail.com'
        print(userEmail)
        user = Admin.query.filter_by(EMAIL_ID=userEmail).first()
        print("user.USER_ID",user.USER_ID)
        alldata = EMPLOYEE_DETAILS.query.all()
        if alldata:
            returndata = []
            returndta =[]
            print("returndata123",returndata)
            for index,row in df.iterrows():
                # returndata = []
                # print("returndata123",returndata)
                print("row",row)
                Employee_number = row.get('Employee_Number')
                dbdata = EMPLOYEE_DETAILS.query.filter(EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == Employee_number).first()
                print("dbdata",dbdata)
                eed = row.get('Effective_End_Date')
                emp_no = row.get('Emp_Number')
                # email pattern validation
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if re.match(email_pattern, row['Email_Id']):
                        email = row.get('Email_Id')
                else:
                    return jsonify({"error":"Invalid email pattern"}),400
 
                print("row.get('Middle_Name')----->",row.get('Middle_Name'))
               
                if type(row.get('Middle_Name')) != NoneType:
                    middleName = row.get('Middle_Name')
 
                else:
                    middleName = None
                print("type(row.get('Middle_Name'))",type(row.get('Middle_Name')),row.get('Middle_Name'))
           
                # DOB validation
                DOB = row['Date_Of_Birth']  # Assuming date format is YYYY-MM-DD
                # dob= datetime.strptime(DOB, '%Y-%m-%d')
                dob_year = DOB.date().year
                today = datetime.today()
                this_year = today.date().year
                min_age = this_year - dob_year
                if not min_age >= 18:
                    return jsonify({'error':f"You must be at least 18 years old."}),400
           
                # mobile pattern validation
                mobile = row['Mobile_No']
                mobile_no = mobile.replace("-", "")
                print("mobile_no",mobile_no)
                mobile_pattern = r'^(\+\d{1,3}[- ]?)?\d{10}$'
                if re.match(mobile_pattern,mobile_no):
                    mobilenum = mobile_no
                else:
                    return jsonify ({"error": 'Please enter valid mobile number'}),400
                mob_data = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.MOBILE_NO == mobile_no)).first()
                if mobile_no != dbdata.MOBILE_NO:
                    if mob_data:
                        return jsonify ({"error" : f'mobile number {mobile_no} already exist'}),400
                if emp_no:
                    email_data = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMAIL_ID == email)).first()
                    if email_data:
                        return jsonify ({"error" : f'email {email} already exist'}),400
                    dbESD = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                    Datedb = str(row['Effective_Start_Date'])
                    print("Datedb",Datedb)
                    Dated = datetime.strptime(Datedb, "%Y-%m-%d %H:%M:%S")
                    print("Dated",Dated)
                    PrevEED = Dated - timedelta(days=1)
                    if dbESD >= Dated:
                        return jsonify({"message":"Effective Start Date shouldn't be earlier or same as candidate's Effective Start Date "})
                    elif dbESD < Dated:
                        dbdata.EFFECTIVE_END_DATE = PrevEED
                   
                    details = EMPLOYEE_DETAILS(
                                        EMPLOYEE_ID = dbdata.EMPLOYEE_ID,
                                        EMPLOYEE_NUMBER = row.get('Emp_Number') if row.get('Emp_Number') else dbdata.EMPLOYEE_NUMBER,
                                        FIRST_NAME = row.get('First_Name') if row.get('First_Name') else dbdata.FIRST_NAME,
                                        MIDDLE_NAME = middleName,# if data.get('Middle_Name') else dbdata.MIDDLE_NAME,
                                        LAST_NAME = row.get('Last_Name') if row.get('Last_Name') else dbdata.LAST_NAME,
                                        USER_ID = user.USER_ID,
                                        WORKER_TYPE = row.get('Worker_Type'),
                                        DATE_OF_BIRTH = row.get('Date_Of_Birth') if row.get('Date_Of_Birth') else dbdata.DATE_OF_BIRTH,
                                        MOBILE_NO = mobilenum if mobilenum else dbdata.MOBILE_NO,
                                        EFFECTIVE_START_DATE =  row['Effective_Start_Date'] if row['Effective_Start_Date'] else date.today(),
                                        EFFECTIVE_END_DATE = eed,
                                        JOB_LOCATION = row.get('Job_Location')if row.get('Job_Location') else dbdata.JOB_LOCATION,
                                        EMAIL_ID =email,
                                        CREATED_BY = 'HRName',
                                        LAST_UPDATED_BY = "HRName")
                    returndata.append(details)
                    returndta.append(details.serialize())
                    print("returndata(a)",returndata)
                if not emp_no:
                    if Employee_number == dbdata.EMPLOYEE_NUMBER and email == dbdata.EMAIL_ID:
                        print("fields changing")
                        print("data",row)
                        dbESD = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                        print("dbESD",dbESD)
                        Datedb = str(row['Effective_Start_Date'])
                        print("Datedb",Datedb)
                        Dated = datetime.strptime(Datedb, "%Y-%m-%d %H:%M:%S")
                        print("Dated",Dated)
                        if Dated == dbESD:
                            print("fields changing same day")
                            for i in row:
                                print("i",i)
                                cap = i.upper()
                                new_value = row.get(i)
                                print("new_value",new_value)
                                if getattr(dbdata,cap) != new_value:
                                    print("new_value",new_value)
                                    setattr(dbdata,cap,new_value)
                   
                        fdata = EMPLOYEE_DETAILS.query.filter(
                                            (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == row.get('Employee_Number'))&
                                            (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE > row.get('Effective_Start_Date'))
                                        ).order_by(EMPLOYEE_DETAILS.EFFECTIVE_START_DATE.asc()).first()
                        print("fields changing diff day")
                        print("middleName",middleName)
                   
                        print(fdata,"lkjnhbgvfc")
                        if not fdata:
                            print("inside else")
                            eed = row.get('Effective_End_Date')
                        else:
                            print("fdata",fdata)
                            fESD = datetime.strptime(str(fdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                            eed = fESD - timedelta(days=1)
                        Dated = str(row['Effective_Start_Date'])
                        print("Dated",Dated)
                        Datedb = datetime.strptime(Dated, "%Y-%m-%d %H:%M:%S")
                        print("Datedb",Datedb)
                        PrevEED = Datedb - timedelta(days=1)
                        dbdata.EFFECTIVE_END_DATE = PrevEED
                        details = EMPLOYEE_DETAILS(
                                            EMPLOYEE_ID = dbdata.EMPLOYEE_ID,
                                            EMPLOYEE_NUMBER = row.get('Employee_Number') if row.get('Employee_Number') else dbdata.EMPLOYEE_NUMBER,
                                            FIRST_NAME = row.get('First_Name') if row.get('First_Name') else dbdata.FIRST_NAME,
                                            MIDDLE_NAME = middleName,# if row.get('Middle_Name') else dbdata.MIDDLE_NAME,
                                            LAST_NAME = row.get('Last_Name') if row.get('Last_Name') else dbdata.LAST_NAME,
                                            USER_ID = user.USER_ID,
                                            WORKER_TYPE = row.get('Worker_Type') if row.get('Worker_Type') else dbdata.WORKER_TYPE,
                                            DATE_OF_BIRTH = row.get('Date_Of_Birth') if row.get('Date_Of_Birth') else dbdata.DATE_OF_BIRTH,
                                            MOBILE_NO = mobilenum if mobilenum else dbdata.MOBILE_NO,
                                            EFFECTIVE_START_DATE =  row['Effective_Start_Date'] if row['Effective_Start_Date'] else date.today(),
                                            EFFECTIVE_END_DATE = eed,
                                            JOB_LOCATION = row.get('Job_Location')if row.get('Job_Location') else dbdata.JOB_LOCATION,
                                            EMAIL_ID =email  if email else dbdata.EMAIL_ID,
                                            CREATED_BY = 'HRName',
                                            LAST_UPDATED_BY = "HRName")
                        returndata.append(details)
                        returndta.append(details.serialize())
 
                        print("returndata(b)",returndata)
                    if Employee_number == dbdata.EMPLOYEE_NUMBER and email != dbdata.EMAIL_ID:
                        ddata = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMAIL_ID == email)& (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER != row.get('Employee_Number'))).first()
                        if ddata:
                            return jsonify({"error":f"email {email} already exist"}),400
                        else:
                            print("email changing")
                            # Dated = str(row['Effective_Start_Date'])
                            # Datedb = datetime.strptime(Dated, "%Y-%m-%d")
                            # dbESD = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                            dbESD = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                            Datedb = str(row['Effective_Start_Date'])
                            print("Datedb",Datedb)
                            Dated = datetime.strptime(Datedb, "%Y-%m-%d %H:%M:%S")
                            print("Dated",Dated)
                            if Dated == dbESD:
                                print("email changing same day")
                                for i in row:
                                    print("i",i)
                                    cap = i.upper()
                                    new_value = row.get(i)
                                    print("new_value",new_value)
                                    if getattr(dbdata,cap) != new_value:
                                        print("new_value",new_value)
                                        setattr(dbdata,cap,new_value)
                       
                            # Dated = str(row['Effective_Start_Date'])
                            print("email changing diff day")
                            # print("Dated",Dated)
                            # Datedb = datetime.strptime(row['Effective_Start_Date'], "%Y-%m-%d")
                            # print("Datedb",Datedb)
                            # dbESD = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                            Datedb = str(row['Effective_Start_Date'])
                            print("Datedb",Datedb)
                            Dated = datetime.strptime(Datedb, "%Y-%m-%d %H:%M:%S")
                            print("Dated",Dated)
                            PrevEED = Dated - timedelta(days=1)
                            dbdata.EFFECTIVE_END_DATE = PrevEED
                            fdata = EMPLOYEE_DETAILS.query.filter(
                                            (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == row.get('Employee_Number'))&
                                            (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE > row.get('Effective_Start_Date'))
                                        ).order_by(EMPLOYEE_DETAILS.EFFECTIVE_START_DATE.asc()).first()
                   
                            print(fdata,"lkjnhbgvfc")
                            if not fdata:
                                print("inside else")
                                eed = row.get('Effective_End_Date')
                            else:
                                print("fdata",fdata)
                                fESD = datetime.strptime(str(fdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                                eed = fESD - timedelta(days=1)
                            print("row.get('Mobile_No')",row.get('Mobile_No'))
                            details = EMPLOYEE_DETAILS(
                                                EMPLOYEE_ID = dbdata.EMPLOYEE_ID,
                                                EMPLOYEE_NUMBER = row.get('Employee_Number') if row.get('Employee_Number') else dbdata.EMPLOYEE_NUMBER,
                                                FIRST_NAME = row.get('First_Name') if row.get('First_Name') else dbdata.FIRST_NAME,
                                                MIDDLE_NAME = middleName,# if row.get('Middle_Name') else dbdata.MIDDLE_NAME,
                                                LAST_NAME = row.get('Last_Name') if row.get('Last_Name') else dbdata.LAST_NAME,
                                                USER_ID = user.USER_ID,
                                                WORKER_TYPE = row.get('Worker_Type') if row.get('Worker_Type') else dbdata.WORKER_TYPE,
                                                DATE_OF_BIRTH = row.get('Date_Of_Birth') if row.get('Date_Of_Birth') else dbdata.DATE_OF_BIRTH,
                                                MOBILE_NO = mobilenum if mobilenum else dbdata.MOBILE_NO,
                                                EFFECTIVE_START_DATE =  row['Effective_Start_Date'] if row['Effective_Start_Date'] else date.today(),
                                                EFFECTIVE_END_DATE = eed,
                                                JOB_LOCATION = row.get('Job_Location')if row.get('Job_Location') else dbdata.JOB_LOCATION,
                                                EMAIL_ID =email  if email else dbdata.EMAIL_ID,
                                                CREATED_BY = 'HRName',
                                                LAST_UPDATED_BY = "HRName")
                            returndata.append(details)
                            returndta.append(details.serialize())
                            print("returndata(c)",returndata)
        print("returndata",returndata)
        for i in returndata:
            db.session.add(i)
        # db.session.add(returndata)
        db.session.commit()
        return jsonify({"message":"Updated successfully", "data":returndta}),201
    except Exception as e:
        return jsonify({'error':str(e)}),500  



def getEmployeedetails(id):
    try:
        # data =Employement_Details.query.get(id)
        today = date.today()
        data = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMPLOYEE_ID==id) & (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= today) &(today <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)).first()
 
        print('data',data)
        if not data:
            return jsonify({'message': f'data {id} not found'}),404
        print("data.serialize()",data.serialize())
        return jsonify({'data' : data.serialize()}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500

# get all employees[GET Method]
def getEmployee():
    try:
        get=EMPLOYEE_DETAILS.query.all()
        returndata=[]
        if not get:
            return jsonify({'message': f'person {id} not found'}),404
        for i in get:
            returndata.append(i.serialize())
        return jsonify({'data': returndata}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500

# get employee by id[GET Method]
def getEmployeeById(id):
    try:
        person =EMPLOYEE_DETAILS.query.get(id)
        print('person',person)
        if not person:
            return jsonify({'message': f'person {id} not found'}),404
        print("person.serialize()",person.serialize())
        return jsonify({'data' : person.serialize()}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    
# update employee details by id[PUT Method]
def updateemp(id):
    try:
        print(EMPLOYEE_DETAILS.EMPLOYEE_ID)
        print("fdghjklkjhgf")
        data = request.json
        print("data",data)
 
        # email pattern validation
        e_id = data.get('Email_Id')
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, data['Email_Id']):
                email = data.get('Email_Id')
       
        # DOB validation
        DOB = data['Date_Of_Birth']  # Assuming date format is YYYY-MM-DD
        dob= datetime.strptime(DOB, '%Y-%m-%d')
        dob_year = dob.date().year
        today = datetime.today()
        this_year = today.date().year
        min_age = this_year - dob_year
        if not min_age >= 18:
            return jsonify({'error':f"You must be at least 18 years old."}),400
       
        # mobile pattern validation
        mobile_no = data['Mobile_No']
        mobile_pattern = r'^(\+\d{1,3}[- ]?)?\d{10}$'
        if not re.match(mobile_pattern,mobile_no):
            return jsonify ({"error": 'Please enter valid mobile number'}),400
       
        # checking mobile number in database
        mob_data = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMPLOYEE_ID != id) & (EMPLOYEE_DETAILS.MOBILE_NO == mobile_no)).first()
        if mob_data:
            return jsonify ({"error" : f'mobile number {mobile_no} already exist'}),400
        # to get recent record
        today = date.today()
        esd = data.get('Effective_Start_Date')
        dbdata = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMPLOYEE_ID == id)
                                                       & (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == data.get('Employee_Number'))
                                                       & (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= esd)
                                                       & (esd <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)).first()
       
        print("dbdata1st",dbdata)
        if not dbdata:
            print("insidenot if")
            dbdata = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMPLOYEE_ID == id)
                                            #    & (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == data.get('Employee_Number'))
                                            & (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= today)
                                            & (today <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)).first()
        print("dbdata",dbdata)
       
        print("data.get('Effective_Start_Date')",type(data.get('Effective_Start_Date')))
        userEmail='sravanchekuri449@gmail.com'
        print(userEmail)
        user = Admin.query.filter_by(EMAIL_ID=userEmail).first()
        # user = Admin.query.get(1)
        print("user.USER_ID",user.USER_ID)
       
        # existing_emp = EMPLOYEE_DETAILS.query.filter_by(EMPLOYEE_NO =data.get('Employee_No')).first()
        # print("dbdata",d
        # bdata)
        if  dbdata.EMAIL_ID == e_id and dbdata.EMPLOYEE_NUMBER == data.get('Employee_Number'):
            # return jsonify({"message":"email already exist"})
       
            print("data",data)
            Dated = str(data['Effective_Start_Date'])
            Datedb = datetime.strptime(Dated, "%Y-%m-%d")
            dbESD = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
       
            if dbESD <= Datedb and data.get('Employee_Number').startswith('C'):
               
                print("dfghj",data.get('Employee_Number').startswith('C'))
                for i in data:
                    print("i",i)
                    cap = i.upper()
                    new_value = data.get(i)
                    print("new_value",new_value)
                    if getattr(dbdata,cap) != new_value:
                        print("new_value",new_value)
                        setattr(dbdata,cap,new_value)
                db.session.commit()
                return jsonify({"message": "update existing record", "data":dbdata.serialize()}),200
           
            if not data.get('Employee_Number').startswith('C') and dbdata.EMPLOYEE_NUMBER == data.get('Employee_Number'):
                Datedb = str(data['Effective_Start_Date'])
                Datedb = datetime.strptime(Datedb, "%Y-%m-%d")
                dbESD = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                if dbESD == Datedb:
                    fdata = EMPLOYEE_DETAILS.query.filter(
                                   (EMPLOYEE_DETAILS.EMPLOYEE_ID == id) &
                                    (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == data.get('Employee_Number'))&
                                    (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE > data.get('Effective_Start_Date'))
                                ).order_by(EMPLOYEE_DETAILS.EFFECTIVE_START_DATE.asc()).first()
               
                    print(fdata,"lkjnhbgvfc")
                    if not fdata:
                        print("inside else")
                        eed = data.get('Effective_End_Date')
                    else:
                        print("fdata",fdata)
                        fESD = datetime.strptime(str(fdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                        eed = fESD - timedelta(days=1)
 
                    updateData = {
                                        'EMPLOYEE_NUMBER': data.get('Employee_Number'),
                                        'FIRST_NAME': data.get('First_Name'),
                                    'MIDDLE_NAME': data.get('Middle_Name'),
                                    'LAST_NAME': data.get('Last_Name'),
                                    'WORKER_TYPE': data.get('Worker_Type'),
                                    'DATE_OF_BIRTH': data.get('Date_Of_Birth'),
                                    'MOBILE_NO':  data.get('Mobile_No'),
                                    'JOB_LOCATION':  data.get('Job_Location'),
                                    'EMAIL_ID':  data.get('Email_Id')
                                    }
                    for i in updateData:
                        print("i",i)
                        # cap = i.upper()
                        new_value = updateData.get(i)
                        print("new_value",new_value)
                        if getattr(dbdata,i) != new_value:
                            print("new_value",new_value)
                            setattr(dbdata,i,new_value)
                    db.session.commit()
                    return jsonify({"message": "update existing record", "data":dbdata.serialize()}),200
                dbEED = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMPLOYEE_ID == id)
                                               & (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == data.get('Employee_Number'))
                                            & (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= data.get('Effective_Start_Date'))
                                            & (data.get('Effective_Start_Date') <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)).first()
                print("data['Effective_Start_Date']",data['Effective_Start_Date'])
                Dated = str(data['Effective_Start_Date'])
                print("Dated",Dated)
                Datedb = datetime.strptime(data['Effective_Start_Date'], "%Y-%m-%d")
                print("Datedb",Datedb)
                PrevEED = Datedb - timedelta(days=1)
                dbEED.EFFECTIVE_END_DATE = PrevEED
 
                fdata = EMPLOYEE_DETAILS.query.filter(
                                   (EMPLOYEE_DETAILS.EMPLOYEE_ID == id) &
                                    (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == data.get('Employee_Number'))&
                                    (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE > data.get('Effective_Start_Date'))
                                ).order_by(EMPLOYEE_DETAILS.EFFECTIVE_START_DATE.asc()).first()
               
                print(fdata,"lkjnhbgvfc")
                if not fdata:
                    print("inside else")
                    eed = data.get('Effective_End_Date')
                else:
                    print("fdata",fdata)
                    fESD = datetime.strptime(str(fdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                    eed = fESD - timedelta(days=1)
 
                details = EMPLOYEE_DETAILS(
                            EMPLOYEE_ID = dbdata.EMPLOYEE_ID,
                            EMPLOYEE_NUMBER = data.get('Employee_Number') if data.get('Employee_Number') else dbdata.EMPLOYEE_NUMBER,
                            FIRST_NAME = data.get('First_Name') if data.get('First_Name') else dbdata.FIRST_NAME,
                            MIDDLE_NAME = data.get('Middle_Name'),# if data.get('Middle_Name') else dbdata.MIDDLE_NAME,
                            LAST_NAME = data.get('Last_Name') if data.get('Last_Name') else dbdata.LAST_NAME,
                            USER_ID = user.USER_ID,
                            WORKER_TYPE = data.get('Worker_Type') if data.get('Worker_Type') else dbdata.WORKER_TYPE,
                            DATE_OF_BIRTH = data.get('Date_Of_Birth') if data.get('Date_Of_Birth') else dbdata.DATE_OF_BIRTH,
                            MOBILE_NO = data.get('Mobile_No') if data.get('Mobile_No') else dbdata.MOBILE_NO,
                            EFFECTIVE_START_DATE =  data['Effective_Start_Date'] if data['Effective_Start_Date'] else date.today(),
                            EFFECTIVE_END_DATE = eed,
                            JOB_LOCATION = data.get('Job_Location')if data.get('Job_Location') else dbdata.JOB_LOCATION,
                            EMAIL_ID =email  if email else dbdata.EMAIL_ID,
                            CREATED_BY = 'HRName',
                            LAST_UPDATED_BY = "HRName")
           
                db.session.add(details)
                db.session.commit()
                return jsonify({"message":f"{data.get('Employee_Number')} newrecord added successfully", "data":details.serialize()}),201
           
 
            else:
                for i in data:
                    print("i",i)
                    cap = i.upper()
                    new_value = data.get(i)
                    print("new_value",new_value)
                    if getattr(dbdata,cap) != new_value:
                        print("new_value",new_value)
                        setattr(dbdata,cap,new_value)
                db.session.commit()
                return jsonify({"message": "update existing record", "data":dbdata.serialize()}),200
        else:
            # ssss=EMPLOYEE_DETAILS.EMPLOYEE_ID
 
            print("ssss")
            existing_email = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMAIL_ID == e_id) & (EMPLOYEE_DETAILS.EMPLOYEE_ID != id)).first()
            # existing_email = EMPLOYEE_DETAILS.query.all()
            today = date.today()
            # existing_email = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMPLOYEE_ID==id) & (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= today) &(today <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)).first()
 
            print("existing_email122",existing_email,existing_email,id)
            if existing_email:
            # if existing_email.EMAIL_ID == e_id and existing_email.EMPLOYEE_ID != id:
                return jsonify({"message":"email already exist"})
            else:
                print("insideelse",existing_email,data)
                print("dbdata.EFFECTIVE_START_DATE",type(dbdata.EFFECTIVE_START_DATE))
                print("data['Effective_Start_Date']",type(data['Effective_Start_Date']))
                print("data['Effective_Start_Date']",data)
                Datedb = str(data['Effective_Start_Date'])
                print("Datedb---<>",Datedb,dbdata.EMPLOYEE_NUMBER)
                # Convert Date_Of_Joining to a datetime object
                Datedb = datetime.strptime(Datedb, "%Y-%m-%d")
                print("Datedb",type(Datedb))
                dbESD = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                print("dbESD",type(dbESD))
                if dbESD <= Datedb and data.get('Employee_Number').startswith('C'):
                   
                    print("dfghj",data.get('Employee_Number').startswith('C'))
                    for i in data:
                        print("i",i)
                        cap = i.upper()
                        new_value = data.get(i)
                        print("new_value",new_value)
                        if getattr(dbdata,cap) != new_value:
                            print("new_value",new_value)
                            setattr(dbdata,cap,new_value)
                    db.session.commit()
                    return jsonify({"message": "update existing record", "data":dbdata.serialize()}),200
 
                # if not data.get('Employee_No').startswith('C'):
                if not data.get('Employee_Number').startswith('C') and dbdata.EMPLOYEE_NUMBER == data.get('Employee_Number'):
                    Datedb = str(data['Effective_Start_Date'])
                    Datedb = datetime.strptime(Datedb, "%Y-%m-%d")
                    dbESD = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                    if dbESD == Datedb:
                        print("dfgdghjjkkhj")
 
                        fdata = EMPLOYEE_DETAILS.query.filter(
                                   (EMPLOYEE_DETAILS.EMPLOYEE_ID == id) &
                                    (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == data.get('Employee_Number'))&
                                    (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE > data.get('Effective_Start_Date'))
                                ).order_by(EMPLOYEE_DETAILS.EFFECTIVE_START_DATE.asc()).first()
                        if not fdata:
                            print("inside else")
                            eed = data.get('Effective_End_Date')
                        else:
                            print("fdata",fdata)
                            fESD = datetime.strptime(str(fdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                            eed = fESD - timedelta(days=1)
 
                        updateData = {
                                        'EMPLOYEE_NUMBER': data.get('Employee_Number'),
                                        'FIRST_NAME': data.get('First_Name'),
                                    'MIDDLE_NAME': data.get('Middle_Name'),
                                    'LAST_NAME': data.get('Last_Name'),
                                    'WORKER_TYPE': data.get('Worker_Type'),
                                    'DATE_OF_BIRTH': data.get('Date_Of_Birth'),
                                    'MOBILE_NO':  data.get('Mobile_No'),
                                    'JOB_LOCATION':  data.get('Job_Location'),
                                    'EMAIL_ID':  data.get('Email_Id')
                                    }
                        for i in updateData:
                            print("i",i)
                            # cap = i.upper()
                            new_value = updateData.get(i)
                            print("new_value",new_value)
                            if getattr(dbdata,i) != new_value:
                                print("new_value",new_value)
                                setattr(dbdata,i,new_value)
                        db.session.commit()
                        return jsonify({"message": "update existing record", "data":dbdata.serialize()}),200
                    if dbESD < Datedb:
                        dbEED = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMPLOYEE_ID == id)
                                               & (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == data.get('Employee_Number'))
                                            & (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= data.get('Effective_Start_Date'))
                                            & (data.get('Effective_Start_Date') <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)).first()
                        Datedb = str(data['Effective_Start_Date'])
                        print("Datedb-->",Datedb)
                        # Convert Date_Of_Joining to a datetime object
                        Datedb = datetime.strptime(Datedb, "%Y-%m-%d")
                        print("erfgnsgison")
                        # Subtract one day from the Date_Of_Joining
                        # if data.get('Employee_No').startswith('C'):
                        #     dbdata.EFFECTIVE_END_DATE = dbdata.EFFECTIVE_START_DATE
                        # else:
                        #     PrevEED = Datedb - timedelta(days=1)
                        #     dbdata.EFFECTIVE_END_DATE = PrevEED
                        PrevEED = Datedb - timedelta(days=1)
                        dbEED.EFFECTIVE_END_DATE = PrevEED
                        print("erfgnsgisonsdv")
 
                        fdata = EMPLOYEE_DETAILS.query.filter(
                                   (EMPLOYEE_DETAILS.EMPLOYEE_ID == id) &
                                    (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == data.get('Employee_Number'))&
                                    (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE > data.get('Effective_Start_Date'))
                                ).order_by(EMPLOYEE_DETAILS.EFFECTIVE_START_DATE.asc()).first()
               
               
                        print(fdata,"lkjnhbgvfc")
                        if not fdata:
                            print("inside else")
                            eed = data.get('Effective_End_Date')
                        else:
                            print("fdata",fdata)
                            fESD = datetime.strptime(str(fdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                            eed = fESD - timedelta(days=1)
 
 
                        details = EMPLOYEE_DETAILS(
                                    EMPLOYEE_ID = dbdata.EMPLOYEE_ID,
       
                                    EMPLOYEE_NUMBER = data.get('Employee_Number') if data.get('Employee_Number') else dbdata.EMPLOYEE_NUMBER,
                                    FIRST_NAME = data.get('First_Name') if data.get('First_Name') else dbdata.FIRST_NAME,
                                    MIDDLE_NAME = data.get('Middle_Name') if data.get('Middle_Name') else dbdata.MIDDLE_NAME,
                                    LAST_NAME = data.get('Last_Name') if data.get('Last_Name') else dbdata.LAST_NAME,
                                    USER_ID = user.USER_ID,
                                    WORKER_TYPE = data.get('Worker_Type') if data.get('Worker_Type') else dbdata.WORKER_TYPE,
                                 
                                    MOBILE_NO = data.get('Mobile_No') if data.get('Mobile_No') else dbdata.MOBILE_NO,
                                    DATE_OF_BIRTH = data.get('Date_Of_Birth') if data.get('Date_Of_Birth') else dbdata.DATE_OF_BIRTH,
                                    EFFECTIVE_START_DATE =  data.get('Effective_Start_Date') if data.get('Effective_Start_Date') else date.today(),
                                    EFFECTIVE_END_DATE = eed,
                                    JOB_LOCATION = data.get('Job_Location')if data.get('Job_Location') else dbdata.JOB_LOCATION,
                                    EMAIL_ID =email  if email else dbdata.EMAIL_ID,
                                    CREATED_BY = 'HRName',
                                    LAST_UPDATED_BY = "HRName")
                   
                        db.session.add(details)
                        db.session.commit()
                        print("erfgnsevsgisonsdv")
                        return jsonify({"message":f"{data.get('Employee_Number')} newrecord added successfully", "data":details.serialize()}),201
                if not data.get('Employee_Number').startswith('C') and dbdata.EMPLOYEE_NUMBER != data.get('Employee_Number'):
                    print("mnnbbtr",data)
                    empnum = data['Employee_Number']
                    empdb = EMPLOYEE_DETAILS.query.filter_by(EMPLOYEE_NUMBER = empnum).first()
                    if empdb:
                        return jsonify({'message':f'Employee Number {empnum} already exist '}), 400
                    Datedb = str(data['Effective_Start_Date'])
                    Datedb = datetime.strptime(Datedb, "%Y-%m-%d")
                    dbESD = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                    Datedb = str(data['Effective_Start_Date'])
                    print("Datedb",Datedb)
                    # Convert Date_Of_Joining to a datetime object
                    Datedb = datetime.strptime(Datedb, "%Y-%m-%d")
                    PrevEED = Datedb - timedelta(days=1)
                    if dbESD >= Datedb:
                        return jsonify({"message":"Effective Start Date shouldn't be earlier or same as candidate's Effective Start Date "})
                    elif dbESD < Datedb:
                        dbdata.EFFECTIVE_END_DATE = PrevEED
                    # else:
                    #     return jsonify ({"error":"Effective start date shouldn't be earlier than candidate's Effective start date"})
   
                    print("dbdata.Employee_Number",dbdata.EMPLOYEE_NUMBER)
                    empnum = data['Employee_Number']
                    empdb = EMPLOYEE_DETAILS.query.filter_by(EMPLOYEE_NUMBER = empnum).first()
                    if empdb:
                        return jsonify({'message':f'Employee Number {empnum} already exist '}), 400
                    details = EMPLOYEE_DETAILS(
                                EMPLOYEE_ID = dbdata.EMPLOYEE_ID,
   
                                EMPLOYEE_NUMBER = data.get('Employee_Number') if data.get('Employee_Number') else dbdata.EMPLOYEE_NUMBER,
                                FIRST_NAME = data.get('First_Name') if data.get('First_Name') else dbdata.FIRST_NAME,
                                MIDDLE_NAME = data.get('Middle_Name') if data.get('Middle_Name') else dbdata.MIDDLE_NAME,
                                LAST_NAME = data.get('Last_Name') if data.get('Last_Name') else dbdata.LAST_NAME,
                                WORKER_TYPE = data.get('Worker_Type') if data.get('Worker_Type') else dbdata.WORKER_TYPE,
                                USER_ID = user.USER_ID,
                                DATE_OF_BIRTH = data.get('Date_Of_Birth') if data.get('Date_Of_Birth') else dbdata.DATE_OF_BIRTH,
                                MOBILE_NO = data.get('Mobile_No') if data.get('Mobile_No') else dbdata.MOBILE_NO,
                                EFFECTIVE_START_DATE =  data.get('Effective_Start_Date') if data.get('Effective_Start_Date') else date.today(),
                                EFFECTIVE_END_DATE = data.get('Effective_End_Date') if data.get('Effective_End_Date') else date(4712, 12, 31),
                                JOB_LOCATION = data.get('Job_Location')if data.get('Job_Location') else dbdata.JOB_LOCATION,
                                EMAIL_ID =email  if email else dbdata.EMAIL_ID,
                                CREATED_BY = 'HRName',
                                LAST_UPDATED_BY = "HRName")
               
                    db.session.add(details)
                    db.session.commit()
                    return jsonify({"message":f"{data.get('Employee_Number')} newrecord added successfully", "data":details.serialize()}),201      
 
    except Exception as e:
        return jsonify({'error':str(e)}),500


# get all employees[GET Method]
def getEmployee():
    try:
        today = date.today()
        get=EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= today) &(today <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)).all()
        # get = EMPLOYEE_DETAILS.query.filter(today < EMPLOYEE_DETAILS.EFFECTIVE_END_DATE).all()
        # get = EMPLOYEE_DETAILS.query.filter(EMPLOYEE_DETAILS.EFFECTIVE_END_DATE == date(4712,12,31)).all()
        returndata=[]
        if not get:
            return jsonify({'message': f'person {id} not found'}),404
        for i in get:
            returndata.append(i.serialize())
        return jsonify({'data': returndata}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    

def getEmpdetails(id):
    try:
        # data =Employement_Details.query.get(id)
        today = date.today()
        data = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMPLOYEE_ID==id) & (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= today) &(today <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)).first()
 
        print('data',data)
        if not data:
            return jsonify({'message': f'data {id} not found'}),404
        print("data.serialize()",data.serialize())
        return jsonify({'data' : data.serialize()}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500



def getEmployeedetails(id,date,enddate):
    try:
        print("kjnhbgvf")
        # data = request.form
        ESD = date
        EED = enddate
        print("ESD",ESD)
        get = EMPLOYEE_DETAILS.query.filter(
                                   (EMPLOYEE_DETAILS.EMPLOYEE_ID == id) &
                                    (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= ESD)&
                                    (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= EED)
                                ).order_by(EMPLOYEE_DETAILS.EFFECTIVE_START_DATE.desc()).first()
       
        print("get", get)
        if not get:
            return jsonify({'message': 'data not found'}), 404
        print("data.serialize()", get.serialize())
        return jsonify({'data': get.serialize()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500  
    
def SearchEmployeedetails(empNum,date,enddate):
    try:
        # data = request.json
        ESD = date
        emp_no = empNum
        # emp_no = request.args.get('emp_no')
        # ESD = request.args.get('date')
        # date1 = request.args.get('enddate')
        print("ESD",type(ESD),type(enddate))
        EED = '4712-12-31' if enddate == 'undefined' else enddate
        print("EED",EED)
        returndata = {}
        get = EMPLOYEE_DETAILS.query.filter(
                                   (EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == emp_no) &
                                    (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= ESD)&
                                    (EMPLOYEE_DETAILS.EFFECTIVE_END_DATE <= EED)
                                ).order_by(EMPLOYEE_DETAILS.EFFECTIVE_START_DATE.desc()).first()
       
        print("get", get)
        if not get:
            return jsonify({'message': 'Data not Found'}), 404
        returndata['EMPLOYEE_DETAILS'] =get.serialize()
        get2 = Employement_Details.query.filter(
                                   (Employement_Details.EMPLOYEE_ID == get.EMPLOYEE_ID) &
                                    (Employement_Details.EFFECTIVE_START_DATE <= ESD)&
                                    (Employement_Details.EFFECTIVE_END_DATE <= EED)
                                ).order_by(Employement_Details.EFFECTIVE_START_DATE.desc()).first()
        if get2:
            returndata['Employement_Details'] =get2.serialize()
 
        get3 = Address_Details.query.filter(
                                   (Address_Details.EMPLOYEE_ID == get.EMPLOYEE_ID) &
                                   (Address_Details.ADDRESS_TYPE == 'Permanent')&
                                    (Address_Details.DATE_FROM <= ESD)&
                                    (Address_Details.DATE_TO <= EED)
                                ).order_by(Address_Details.DATE_FROM.desc()).first()
        if get3:
            returndata['Permanent_Address_Details'] =get3.serialize()
       
        get4 = Address_Details.query.filter(
                                   (Address_Details.EMPLOYEE_ID == get.EMPLOYEE_ID) &
                                   (Address_Details.ADDRESS_TYPE == 'Present')&
                                    (Address_Details.DATE_FROM <= ESD)&
                                    (Address_Details.DATE_TO <= EED)
                                ).order_by(Address_Details.DATE_FROM.desc()).first()
        if get4:
            returndata['Present_Address_Details'] =get4.serialize()
 
       
        print("data.serialize()", returndata)
        return returndata, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def searchemp_num(num):
    try:
        emp_num = num
        print("emp_num",emp_num)
        returndata=[]
        get = EMPLOYEE_DETAILS.query.filter(func.lower(EMPLOYEE_DETAILS.EMPLOYEE_NUMBER).startswith(emp_num.lower())).all()
        if not get:
            return jsonify({"message":"employee not found"}),404
        for i in get:
            returndata.append(i.serialize())
        return jsonify(returndata), 200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    
# search employee[GET Method]
def filterPersons(search_data):
   
    search_data = search_data
    print('type(search_data)',type(search_data))
    person_list = []
    # Use filter and filter conditions for efficient querying
    today = date.today()
    persons = EMPLOYEE_DETAILS.query.filter((
        (EMPLOYEE_DETAILS.EMPLOYEE_NO == search_data) |
        (func.lower(EMPLOYEE_DETAILS.FIRST_NAME).startswith(search_data.lower()))) &
        # | (func.lower(Fields.location).startswith(search_data.lower()))
       
        # | (Fields.LAST_NAME.startswith(search_data))
        #| (PersonData.DATE_OF_BIRTH.contains(search_data))
        (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= today) &
    (today <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)
    ).all()
   
    for person in persons:
            person_dict = person.serialize()
            person_list.append(person_dict)
    return jsonify(person_list), 200

# delete employee by id[DELETE Method]




    # try:
    #         a = Fields.query.get(id)
    #         if not a:
    #             return jsonify({'message': f'Person with id {id} not found'}), 404
            
    #         data = request.json
    #         print("data", data)

    #         updateData = {}
    #         for key in ['MIDDLE_NAME', 'LAST_NAME', 'DATE_OF_JOINING', 'LOCATION', 'EMAIL', 'CREATED_BY', 'LAST_UPDATED_BY']:
    #             if key in data:
    #                 updateData[key] = data[key]
            
    #         print("update", a.serialize())

    #         for key, value in updateData.items():
    #             setattr(a, key, value)

    #         db.session.commit()
    #         return jsonify({'data': a.serialize()}), 200
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500    

# def getexcel1():
#     try:
#         # Fetch data from the EMPLOYEE_DETAILS table
#         empDetails = EMPLOYEE_DETAILS.query.limit(3).all()
       
#         # Convert the data to a list of dictionaries
#         data_list = []
#         for emp in empDetails:
#             data_list.append({
#                 'Employee_Number': emp.EMPLOYEE_NUMBER,
#                 'Effective_Start_Date' : emp.EFFECTIVE_START_DATE,
#                 'Effective_End_Date' : emp.EFFECTIVE_END_DATE,
#                 'First_Name' : emp.FIRST_NAME,
#                 'Middle_Name' : emp.MIDDLE_NAME,
#                 'Last_Name' : emp.LAST_NAME,
#                 'Date_Of_Birth' : emp.DATE_OF_BIRTH,
#                 'Job_Location' : emp.JOB_LOCATION,
#                 'Worker_Type' : emp.WORKER_TYPE,
#                 'Mobile_No' : emp.MOBILE_NO,
#                 'Email_Id' : emp.EMAIL_ID,
#                 'Created_By' : emp.CREATED_BY,
#                 'Last_Updated_By' : emp.LAST_UPDATED_BY,
#             })
       
#         # Create a DataFrame from the list of dictionaries
#         df = pd.DataFrame(data_list)
#         # Get the absolute path to the directory where the script is located
#         script_dir = os.path.dirname(os.path.abspath(__file__))
 
#         # Construct the absolute path to the output Excel file
#         excel_file_path = os.path.join(script_dir, 'output.xlsx')
#         # Export DataFrame to Excel
#         # excel_file_path = 'output.xlsx'
#         df.to_excel(excel_file_path, index=False)
       
#         # Send the Excel file as a response
#         return send_file(excel_file_path, as_attachment=True, download_name='output.xlsx')
   
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

