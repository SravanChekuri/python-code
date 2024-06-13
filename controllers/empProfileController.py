from base64 import encode
from datetime import date, timedelta
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import pandas as pd
from sqlalchemy import func
from flask import jsonify, request, session
from config import db
from Model.employeeData import *
from Model.userData import Admin
from Model.empProfile import *

# def addaddress():
#     try:
#         data = request.json
#         if not data:
#             return jsonify ({'error': 'data is required'}),400
        
#         details = Address(EMPLOYEE_ID
#                           ADDRESS_TYPE
#                           ADDRESS
#                           CITY
#                           STATE
#                           COUNTRY
#                           PIN_CODE
#                           DATE_FROM
#                           DATE_TO
#                           CREATED_BY
#                           LAST_UPDATED_BY)




def employementdetails(id):
    try:
        # dbdata = EMPLOYEE_DETAILS.query.get(id)
        # Employee_Id = dbdata.EMPLOYEE_ID
        # print("Employee_Id",Employee_Id)
        today = date.today()
        print("xcvbn")
        data = request.json
        print("data",data)
        esd =data['Effective_Start_Date']
        dbemp =  Employement_Details.query.filter((Employement_Details.EMPLOYEE_ID==id) & (Employement_Details.EFFECTIVE_START_DATE <= esd) &(esd <= Employement_Details.EFFECTIVE_END_DATE)).first()
        # print("dbemp",dbemp.ASSIGNMENT_ID)
        # dbDOJ = Employement_Details.query.filter((Employement_Details.EMPLOYEE_ID == id)& (Employement_Details.EFFECTIVE_START_DATE <= esd) &(esd <= Employement_Details.EFFECTIVE_END_DATE)).first()
        DOJ = str(data.get('Date_Of_Joining'))
        DOJstrp = datetime.strptime(DOJ, "%Y-%m-%d")
        print("DOJ",DOJstrp)
        
       
        if dbemp:
            probation_period = str(data.get('Probation_Period'))
            digits = re.findall(r'\d+', probation_period)
            prob_int = int(digits[0])
            confirmation_date = DOJstrp + timedelta(days = prob_int * 30 )
            Dated = str(data['Effective_Start_Date'])
            Datedb = datetime.strptime(Dated, "%Y-%m-%d")
            dat = datetime.strptime(str(dbemp.EFFECTIVE_START_DATE), "%Y-%m-%d")
            print("dfghj",dat,Datedb)
            if dat == Datedb:
 
                updateData = {
                                'ORGANIZATION_NAME': data.get('Organization_Name'),
                                'DESIGNATION': data.get('Designation'),
                                'PERSON_TYPE': data.get('Person_Type'),
                            'CONFIRMATION_DATE': confirmation_date,
                            'STATUS': data.get('Status'),
                            'PROBATION_PERIOD': data.get('Probation_Period'),
                            'DATE_OF_JOINING': data.get('Date_Of_Joining'),
                            'NOTICE_PERIOD':  data.get('Notice_Period'),
                            'CURRENT_COMPANY_EXPERIENCE':  data.get('Current_Company_Experience'),
                            'PREVIOUS_EXPERIENCE':  data.get('Previous_Experience'),
                            'TOTAL_EXPERIENCE':  data.get('Total_Experience'),
                            'DEPARTMENT':  data.get('Department'),
                            'PRE_ANNUAL_SALARY':  data.get('Pre_Annual_Salary'),
                            'CTC':  data.get('Ctc')
                            }
                for i in updateData:
                        print("i",i)
                        # cap = i.upper()
                        new_value = updateData.get(i)
                        print("new_value",new_value)
                        if getattr(dbemp,i) != new_value:
                            print("new_value",new_value)
                            setattr(dbemp,i,new_value)
                db.session.commit()
                return jsonify({"message": "update existing record", "data":dbemp.serialize()}),200
            else:
                dbEED =  Employement_Details.query.filter((Employement_Details.EMPLOYEE_ID==id) & (Employement_Details.EFFECTIVE_START_DATE <= esd) &(esd <= Employement_Details.EFFECTIVE_END_DATE)).first()
                Dated = str(data['Effective_Start_Date'])
                print("Datedb",Datedb)
                Datedb = datetime.strptime(Dated, "%Y-%m-%d")
                PrevEED = Datedb - timedelta(days=1)
                dbEED.EFFECTIVE_END_DATE = PrevEED
 
                fdata = Employement_Details.query.filter(
                                   (Employement_Details.EMPLOYEE_ID == id) &
                                    (Employement_Details.EFFECTIVE_START_DATE > data.get('Effective_Start_Date'))
                                ).order_by(Employement_Details.EFFECTIVE_START_DATE.asc()).first()
               
                print(fdata,"lkjnhbgvfc")
                if not fdata:
                    print("inside else")
                    eed = data.get('Effective_End_Date')
                else:
                    print("fdata",fdata)
                    fESD = datetime.strptime(str(fdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                    eed = fESD - timedelta(days=1)
 
 
                details = Employement_Details(
                    EMPLOYEE_ID = data.get('Employee_Id'),
                    ORGANIZATION_NAME = data.get('Organization_Name'),
                    DESIGNATION = data.get('Designation'),
                    DEPARTMENT = data.get('Department'),
                    CONFIRMATION_DATE = confirmation_date,
                    PERSON_TYPE = data.get('Person_Type'),
                    STATUS = data.get('Status'),
                    CTC = data.get('Ctc'),
                    PROBATION_PERIOD = data.get('Probation_Period'),
                    NOTICE_PERIOD = data.get('Notice_Period'),
                    DATE_OF_JOINING = data.get('Date_Of_Joining'),
                    CURRENT_COMPANY_EXPERIENCE = data.get('Current_Company_Experience'),
                    PREVIOUS_EXPERIENCE = data.get('Previous_Experience'),
                    TOTAL_EXPERIENCE = data.get('Total_Experience'),
                    PRE_ANNUAL_SALARY = data.get('Pre_Annual_Salary'),
                    EFFECTIVE_START_DATE = data.get('Effective_Start_Date'),
                    EFFECTIVE_END_DATE = eed,
                    CREATED_BY = 'HR',
                    LAST_UPDATED_BY = 'HR'
               
                )
                db.session.add(details)
                db.session.commit()
                return jsonify({"message":f"{data['Employee_Id']} newrecord added successfully", "data":details.serialize()}),201
 
       
        print("dfghjk")
        details = Employement_Details(
            EMPLOYEE_ID = data.get('Employee_Id'),
            ORGANIZATION_NAME = data.get('Organization_Name'),
            DESIGNATION = data.get('Designation'),
            DEPARTMENT = data.get('Department'),
            # CONFIRMATION_DATE = confirmation_date,
            PERSON_TYPE = data.get('Person_Type'),
            STATUS = data.get('Status'),
            CTC = data.get('Ctc'),
            PROBATION_PERIOD = data.get('Probation_Period'),
            NOTICE_PERIOD = data.get('Notice_Period'),
            DATE_OF_JOINING = data.get('Date_Of_Joining'),
            CURRENT_COMPANY_EXPERIENCE = data.get('Current_Company_Experience'),
            PREVIOUS_EXPERIENCE = data.get('Previous_Experience'),
            TOTAL_EXPERIENCE = data.get('Total_Experience'),
            PRE_ANNUAL_SALARY = data.get('Pre_Annual_Salary'),
            EFFECTIVE_START_DATE = data.get('Effective_Start_Date'),
            EFFECTIVE_END_DATE = data.get('Effective_End_Date') if data.get('Effective_End_Date') else date(4712, 12, 31),
            CREATED_BY = 'HR',
            LAST_UPDATED_BY = 'HR'
        )
        db.session.add(details)
        db.session.commit()
        return jsonify({"message":f"{data['Employee_Id']} employement details added successfully", "data":details.serialize()}),201
 
    except Exception as e:
        return jsonify({'error':str(e)}),500

# def search_empnum(num):
#     try:
#         returndata=[]
#         search = EMPLOYEE_DETAILS.query.filter(EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == num).all()
#         if not search:
#             return jsonify({"error":"employee not found"}),400
#         if search:
#             for i in search:
#                 returndata.append(i.serialize())
#                 return jsonify({"data":returndata}),200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

def getEmployementdetail(id,date,enddate):
    try:
        # data = request.json
        ESD = date
        EED = enddate
        # ESD = request.args.get('Effective_Start_Date')
        print("ESD",ESD)
        get = Employement_Details.query.filter(
                                   (Employement_Details.EMPLOYEE_ID == id) &
                                    (Employement_Details.EFFECTIVE_START_DATE <= ESD)&
                                    (Employement_Details.EFFECTIVE_START_DATE <= EED)
                                ).order_by(Employement_Details.EFFECTIVE_START_DATE.desc()).first()
       
        print("get", get)
        if not get:
            return jsonify({'message': 'data not found'}), 404
        print("data.serialize()", get.serialize())
        return jsonify({'data': get.serialize()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def getEmployementdetails(id):
    try:
        # data =Employement_Details.query.get(id)
        today = date.today()
        data = Employement_Details.query.filter((Employement_Details.EMPLOYEE_ID == id) & (Employement_Details.EFFECTIVE_START_DATE <= today) &(today <= Employement_Details.EFFECTIVE_END_DATE)).first()
 
        print('data',data)
        if not data:
            return jsonify({'message': f'data {id} not found'}),404
        print("data.serialize()",data.serialize())
        return jsonify({'data' : data.serialize()}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500



def addressdetails(id):
    try:
        data = request.json
        address_type = data['Address_Type']
        print("address_type",address_type)
        today = date.today()
        esd = data['Date_From']
        dbdata =  Address_Details.query.filter((Address_Details.EMPLOYEE_ID==id)
                                               & (Address_Details.DATE_FROM <= today)
                                               & (today <= Address_Details.DATE_TO)
                                               & (Address_Details.ADDRESS_TYPE == address_type)
                                               
                                               ).first()
        # print("dbdata12",dbdata)
        # Employee_Id = dbdata.EMPLOYEE_ID
        # print("Employee_Id",Employee_Id)
       
       
           
        if data['Address_Type'] == 'Present':
            print("lokijhg")
            if dbdata:
                Dated = str(data['Date_From'])
                Datedb = datetime.strptime(Dated, "%Y-%m-%d")
                dat = datetime.strptime(str(dbdata.DATE_FROM), "%Y-%m-%d")
                if dat == Datedb:
                    updateData = {
                                'ADDRESS': data.get('Address'),
                                'CITY': data.get('City'),
                                'STATE': data.get('State'),
                            'COUNTRY': data.get('Country'),
                            'PIN_CODE' : data.get('Pin_Code')
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
                else:
                    Dated = str(data['Date_From'])
                    print("Datedb",Datedb)
                    Datedb = datetime.strptime(Dated, "%Y-%m-%d")
                    PrevEED = Datedb - timedelta(days=1)
                    dbdata.DATE_TO = PrevEED
 
                    fdata = Employement_Details.query.filter(
                                    (Employement_Details.EMPLOYEE_ID == id) &
                                        (Employement_Details.EFFECTIVE_START_DATE > data.get('Effective_Start_Date'))
                                    ).order_by(Employement_Details.EFFECTIVE_START_DATE.asc()).first()
               
                    print(fdata,"lkjnhbgvfc")
                    if not fdata:
                        print("inside else")
                        eed = data.get('Effective_End_Date')
                    else:
                        print("fdata",fdata)
                        fESD = datetime.strptime(str(fdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                        eed = fESD - timedelta(days=1)
                    details = Address_Details(
                        EMPLOYEE_ID = data.get('Employee_Id'),
                        ADDRESS_TYPE = data.get('Address_Type'),
                        ADDRESS = data.get('Address'),
                        CITY = data.get('City'),
                        STATE = data.get('State'),
                        COUNTRY = data.get('Country'),
                        PIN_CODE = data.get('Pin_Code'),
                        DATE_FROM = data.get('Date_From'),
                        DATE_TO = eed,
                        CREATED_BY = 'HR',
                        LAST_UPDATED_BY = 'HR'
                    )
                    db.session.add(details)
                    db.session.commit()
                    return jsonify({"message":f"{data.get('Employee_Id')} new record added successfully", "data":details.serialize()}),201
            details = Address_Details(
                        EMPLOYEE_ID = data.get('Employee_Id'),
                        ADDRESS_TYPE = data.get('Address_Type'),
                        ADDRESS = data.get('Address'),
                        CITY = data.get('City'),
                        STATE = data.get('State'),
                        COUNTRY = data.get('Country'),
                        PIN_CODE = data.get('Pin_Code'),
                        DATE_FROM = data.get('Date_From'),
                        DATE_TO = data.get('Date_To'),
                        CREATED_BY = 'HR',
                        LAST_UPDATED_BY = 'HR'
                    )
            db.session.add(details)
            db.session.commit()
            return jsonify({"message":f"{data.get('Employee_Id')} address details added successfully", "data":details.serialize()}),201
        elif data['Address_Type'] == 'Permanent':
            # print("inside elif",dbdata, data['Address_Type'],type(data['Address_Type']))
            if dbdata:
                Dated = str(data['Date_From'])
                Datedb = datetime.strptime(Dated, "%Y-%m-%d")
                dat = datetime.strptime(str(dbdata.DATE_FROM), "%Y-%m-%d")
                if dat == Datedb:
                    updateData = {
                                'ADDRESS': data.get('Address'),
                                'CITY': data.get('City'),
                                'STATE': data.get('State'),
                            'COUNTRY': data.get('Country'),
                            'PIN_CODE' : data.get('Pin_Code')
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
                else:
                    Dated = str(data['Date_From'])
                    print("Datedb",Datedb)
                    Datedb = datetime.strptime(Dated, "%Y-%m-%d")
                    PrevEED = Datedb - timedelta(days=1)
                    dbdata.DATE_TO = PrevEED
                    fdata = Employement_Details.query.filter(
                                    (Employement_Details.EMPLOYEE_ID == id) &
                                        (Employement_Details.EFFECTIVE_START_DATE > data.get('Effective_Start_Date'))
                                    ).order_by(Employement_Details.EFFECTIVE_START_DATE.asc()).first()
               
                    print(fdata,"lkjnhbgvfc")
                    if not fdata:
                        print("inside else")
                        eed = data.get('Effective_End_Date')
                    else:
                        print("fdata",fdata)
                        fESD = datetime.strptime(str(fdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                        eed = fESD - timedelta(days=1)
                    details = Address_Details(
                        EMPLOYEE_ID = data.get('Employee_Id'),
                        ADDRESS_TYPE = data.get('Address_Type'),
                        ADDRESS = data.get('Address'),
                        CITY = data.get('City'),
                        STATE = data.get('State'),
                        COUNTRY = data.get('Country'),
                        PIN_CODE = data.get('Pin_Code'),
                        DATE_FROM = data.get('Date_From'),
                        DATE_TO = eed,
                        CREATED_BY = 'HR',
                        LAST_UPDATED_BY = 'HR'
                    )
                    db.session.add(details)
                    print("details",details)
                    db.session.commit()
                    return jsonify({"message":f"{data.get('Employee_Id')} new record added successfully", "data":details.serialize()}),201
            details = Address_Details(
                        EMPLOYEE_ID = data.get('Employee_Id'),
                        ADDRESS_TYPE = data.get('Address_Type'),
                        ADDRESS = data.get('Address'),
                        CITY = data.get('City'),
                        STATE = data.get('State'),
                        COUNTRY = data.get('Country'),
                        PIN_CODE = data.get('Pin_Code'),
                        DATE_FROM = data.get('Date_From'),
                        DATE_TO = data.get('Date_To'),
                        CREATED_BY = 'HR',
                        LAST_UPDATED_BY = 'HR'
                    )
            db.session.add(details)
            print("details",details)
            db.session.commit()
            print("kjhgfd")
            return jsonify({"message":f"{data.get('Employee_Id')} address details added successfully", "data":details.serialize()}),201
    except Exception as e:
        return jsonify({'error':str(e)}),500