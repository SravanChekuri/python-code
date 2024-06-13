from datetime import date, timedelta
import json
import mimetypes
from sqlalchemy import func
from flask import jsonify, request, send_file, session
from config import db
from Model.employeeData import *
from Model.empProfile import *
from Model.userData import Admin
from Model.template import *
from io import BytesIO
import pandas as pd
import re
import pythoncom
import os
import win32com.client
from mimetypes import guess_type
# from bson import json_util
# import magic
# from pyRTF import *


def addtemplate():
    try:
        file = request.files['TEMPLATE']
        temp = file.read()
        print(temp)
        temp_name = request.form['letterType']
        dbdata = Template.query.filter_by(TEMPLATE_NAME = temp_name ).first()
        if dbdata:
            dbdata.TEMPLATE_ID = dbdata.TEMPLATE_ID
            dbdata.TEMPLATE_NAME = dbdata.TEMPLATE_NAME
            dbdata.TEMPLATE_TYPE = file.mimetype
            dbdata.TEMPLATE_SIZE = len(temp)
            dbdata.TEMPLATE = temp
            dbdata.LAST_UPDATED_BY = 'HR'
            db.session.commit()
 
            return jsonify(f'{dbdata.TEMPLATE_NAME} template updated successfully'), 200
 
        details = Template(
            TEMPLATE_ID = request.form['letterId'],
            TEMPLATE_NAME = request.form['letterType'],
            TEMPLATE_TYPE = file.mimetype,
            TEMPLATE_SIZE = len(temp),
            TEMPLATE = temp,
            CREATED_BY = 'HR',
            LAST_UPDATED_BY = 'HR'
        )
        db.session.add(details)
        db.session.commit()
 
        return jsonify('template added successfully'),201
   
    except Exception as e:
        return jsonify({'error':str(e)}),500
 

def temp(TEMPLATE_ID):
    try:
        # temp = Template.query.filter_by(Template_name = Template_name).first()
        temp = Template.query.get(TEMPLATE_ID)
        print("Template_name",temp)

        file_obj = BytesIO(temp.TEMPLATE)
        
 
    # Return the file as a response
        return send_file(file_obj, mimetype=temp.TEMPLATE_TYPE)
    except Exception as e: 
        return jsonify({'error':str(e)}),500

def gettemplate():
    try:
        returndata =[]
        get = Template.query.all()
        print("get",get)
        if not get:
            return jsonify({"error":"templates not found"}),400
        for i in get:
            print("i",i)
            returndata.append(i.serialize())
        return jsonify({'data': returndata}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    
def getexcel1():
    try:
        # Fetch data from the EMPLOYEE_DETAILS table
        empDetails = EMPLOYEE_DETAILS.query.limit(3).all()
       
        # Convert the data to a list of dictionaries
        data_list = []
        for emp in empDetails:
            data_list.append({
                'Employee_Number': emp.EMPLOYEE_NUMBER,
                'Effective_Start_Date' : emp.EFFECTIVE_START_DATE,
                'Effective_End_Date' : emp.EFFECTIVE_END_DATE,
                'First_Name' : emp.FIRST_NAME,
                'Middle_Name' : emp.MIDDLE_NAME,
                'Last_Name' : emp.LAST_NAME,
                'Date_Of_Birth' : emp.DATE_OF_BIRTH,
                'Job_Location' : emp.JOB_LOCATION,
                'Worker_Type' : emp.WORKER_TYPE,
                'Mobile_No' : emp.MOBILE_NO,
                'Email_Id' : emp.EMAIL_ID,
                'Created_By' : emp.CREATED_BY,
                'Last_Updated_By' : emp.LAST_UPDATED_BY,
            })
       
        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data_list)
        # Get the absolute path to the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
 
        # Construct the absolute path to the output Excel file
        excel_file_path = os.path.join(script_dir, 'output.xlsx')
        # Export DataFrame to Excel
        # excel_file_path = 'output.xlsx'
        df.to_excel(excel_file_path, index=False)
       
        # Send the Excel file as a response
        return send_file(excel_file_path, as_attachment=True, download_name='output.xlsx')
   
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def getletter(empNumber):
    try:
        print("xcvm")
        returndata =[]
        # data = request.json
        # num = data.get('Employee_Number')
        num = empNumber
        emp_num = EMPLOYEE_DETAILS.query.filter(EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == num).first()
        if not emp_num:
            return jsonify({"error":"employee not found"}),404
        emp_id = emp_num.EMPLOYEE_ID
        get = Letter.query.filter(Letter.EMPLOYEE_ID == emp_id).all()
        if not get:
            return jsonify({"error":"letters not found"}),404
        for i in get:
            returndata.append(i.serialize())
        return jsonify({'data': returndata}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    
def convertrtf(TEMPLATE_ID):
    try:
        temp = Template.query.filter(Template.TEMPLATE_ID==TEMPLATE_ID).one()
        if not temp:
            return jsonify({'error':'template not found'}),404
        print("temp",temp)
        x = temp.TEMPLATE
        print("x",x)
        

        file_obj = BytesIO(x)

        rtf_file_name = 'rtffile.rtf'
        pdf_file_name = 'pdffile.pdf'
        rtf_file_path = os.path.join(os.getcwd(), rtf_file_name)
        print("rtf_file_path",rtf_file_path)
        with open(rtf_file_path, 'wb') as file:
                file.write(file_obj.read())
        

        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(rtf_file_path)
        
        pdfpath = os.path.join(os.getcwd(), pdf_file_name)
        doc.SaveAs(pdfpath, FileFormat=17)
        print("pdfpath",pdfpath)
        doc.Close()
        word.Quit()
        pythoncom.CoUninitialize()
        os.remove(rtf_file_path)

        with open (pdfpath,'rb') as file:
            a = file.read()

        file_obj = BytesIO(a)
        mimetype = mimetypes.MimeTypes().guess_type(pdf_file_name)[0]
        os.remove(pdfpath)
    # Return the file as a response
        return send_file(file_obj, mimetype=mimetype)    
    except Exception as e: 
        return jsonify({'error':str(e)}),500




def updatetemp(id):
    try:
        update = Template.query.get(id)
        data = request.files['TEMPLATE']
        temp = data.read()
       
        update.TEMPLATE = temp
        db.session.commit()
        return jsonify({'message': 'template changed successfully'}),200

    except Exception as e:
        return jsonify ({'error':str(e)}),500






def add_data_pdf():
    # if request.form['letterType'] == "Offerletter":
 
    # if request.form['letterType'] == "Offerletter":
 
    # if request.form['letterType'] == "Offerletter":
 
    try:
        dataa = request.json
        Emp_Number = dataa['Employee_Number']
        today = date.today()
        data = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == Emp_Number) & (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= today) &(today <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)).first()
        print("data",data)
        emp_id = data.EMPLOYEE_ID
        template = dataa['letterType']
        temp_Id = dataa['letterId']
        temp = Template.query.filter(Template.TEMPLATE_ID==temp_Id).one()
        print("temp",temp)
        var = temp.TEMPLATE
        DOJ = data.DATE_OF_JOINING
        confirmation_date = DOJ + timedelta(days = 365)
 
        # var = request.files['RTF']
        # filename = var.filename.split("-")
        # print("var.filename",f'{filename[0]}-{filename[1]}')
        text = var.decode('utf-8')
        First_Name = data.FIRST_NAME
        print("First_Name",First_Name)
        Middle_Name = data.MIDDLE_NAME
        if data.MIDDLE_NAME is None:
            Middle_Name = ""
        else:
            Middle_Name = data.MIDDLE_NAME
        print(Middle_Name,"Middle_Name")
        Last_Name = data.LAST_NAME
        Employee_Name = First_Name +" "+Middle_Name+" "+Last_Name
        print("Employee_Name",Employee_Name)
        Name = First_Name + Middle_Name
 
        Basic_ratio = 0.5
        hra_ratio = 0.4
       
        a = dataa['CTC']
        print("ctc",a)
        Total_Base_annum = int(a)
        Total_Base_mon = round(Total_Base_annum / 12)
        print("Total_Base_mon",Total_Base_mon)
 
       
        Basic_salary_Annum =round(Total_Base_annum * Basic_ratio)
 
        Basic_month = round(Total_Base_mon * Basic_ratio)
        print("Basic_month",Basic_month)
 
        House_rent_annum = round(Basic_salary_Annum * hra_ratio)
        House_rent_mon = round(Basic_month * hra_ratio)
        print("House_rent_mon",House_rent_mon)
       
        Special_annum = round(Basic_salary_Annum - House_rent_annum)
        Special_mon =round(Basic_month - House_rent_mon)
        print("Special_mon")
 
        Gross_annum =round(Basic_salary_Annum + House_rent_annum + Special_annum)
        Gross_mon = round(Basic_month + House_rent_mon + Special_mon)
        print("Gross_mon",Gross_mon)
 
       
        Company_contribution_m = "-"
        Company_contribution_a = "-"
        Gratuity_annum = round(Basic_salary_Annum * 0.0481)
        Gratuity_month = round(Basic_month * 0.0481)
        print("Gratuity_month",Gratuity_month)
        Insurance_annum = 0
        Insurance_month = 0
        if Gross_mon > 21000:
            Insurance_annum = 25000
            Insurance_month = round(Insurance_annum / 12)
 
       
        print("Insurance_month",Insurance_month)
        Performance_incentiive_annum = "-"
        Performance_incentive_mon = "-"
        print("Performance_incentive_mon",Performance_incentive_mon)
 
        Total_Cost_Company_annum = round(Total_Base_annum + Gratuity_annum + Insurance_annum)
        Total_Cost_Company_mon = round(Total_Base_mon + Gratuity_month + Insurance_month)
        print("Total_Cost_Company_mon",Total_Cost_Company_mon)
           
        details = {
 
       
            'EMPLOYEE_NAME':Employee_Name,
            'NAME' : Name,
            'CURRENT_DATE' : today or '2024-03-03',
            'PERSONAL_EMAIL' : data.EMAIL_ID,
            'LOCATION' : data.LOCATION,
            'DATE_OF_JOINING':data.DATE_OF_JOINING,
            'TB_annum': "{:,.0f}".format(Total_Base_annum),
            'TB_mon': "{:,.0f}".format(Total_Base_mon),
            'BS_annum' :"{:,.0f}".format(Basic_salary_Annum),
            'BS_mon' : "{:,.0f}".format(Basic_month),
            'HRA_annum' : "{:,.0f}".format(House_rent_annum),
            'HRA_mon' : "{:,.0f}".format(House_rent_mon),
            'SP_annum' : "{:,.0f}".format(Special_annum),
            'SP_mon' : "{:,.0f}".format(Special_mon),
            'GC_annum' : "{:,.0f}".format(Gross_annum),
            'CONFIRMATION_DATE' : confirmation_date,
            'G_mon' : "{:,.0f}".format(Gross_mon),
            'PFM' : Company_contribution_m or 12,
            'PFA' : Company_contribution_a or 13,
            'GRATUITY_annum' : "{:,.0f}".format(Gratuity_annum),
            'GRATUITY_mon' : "{:,.0f}".format(Gratuity_month),
            'INSURANCE_annum' : "{:,.0f}".format(Insurance_annum),
            'INSURANCE_mon' : "{:,.0f}".format(Insurance_month),
            'PI_annum' : Performance_incentiive_annum,
            'PI_mon' : Performance_incentive_mon,
            'CTC_annum' : "{:,.0f}".format(Total_Cost_Company_annum),
            'CTC_mon' : "{:,.0f}".format(Total_Cost_Company_mon)
        }
        print("details-->",details)
        # print("data",type(data.Date))
 
       
         
        for key, value in details.items():
            print("key",key,value)
           
            text= re.sub(fr'\b{key}\b',str(value),text)
           
        print("os.path",os.path,os.getcwd())
        rtf_file_name = 'rtffile.rtf'
        pdf_file_name = 'pdffile.pdf'
        rtf_file_path = os.path.join(os.getcwd(), rtf_file_name)
        print("rtf_file_path",rtf_file_path)
        with open(rtf_file_path, 'wb') as file:
                file.write(text.encode('UTF-8'))
       
 
        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(rtf_file_path)
       
        pdfpath = os.path.join(os.getcwd(), pdf_file_name)
        doc.SaveAs(pdfpath, FileFormat=17)
        print("pdfpath",pdfpath)
        doc.Close()
        word.Quit()
        pythoncom.CoUninitialize()
        os.remove(rtf_file_path)
 
        with open ('C:\\Angular\\HRIT- Project\\pdffile.pdf','rb') as file:
            a = file.read()
 
        # file_obj = BytesIO(a)
        mimetype = mimetypes.MimeTypes().guess_type(pdf_file_name)[0]
        dbdata = Letter.query.filter_by(EMPLOYEE_ID = emp_id, LETTER_NAME = template).first()
 
        if dbdata:
            print("inside if", dbdata, dbdata.EMPLOYEE_ID)
            dbdata.EMPLOYEE_ID = dbdata.EMPLOYEE_ID
            dbdata.TEMPLATE_ID = dbdata.TEMPLATE_ID
            dbdata.LETTER_NAME = dbdata.LETTER_NAME
            dbdata.LETTER_SIZE = len(a)
            dbdata.LETTER_TYPE = mimetype
            dbdata.LETTER = a
            dbdata.CREATED_BY = 'HR'
            dbdata.LAST_UPDATED_BY = 'HR'
            print("inside if", dbdata, dbdata.EMPLOYEE_ID,dbdata.LETTER_SIZE)
            db.session.commit()
            return jsonify({"message":"letter generated succcessfully & Updated to db"}), 200
 
        new_pdf = Letter(
                        EMPLOYEE_ID=emp_id,
                        TEMPLATE_ID = temp_Id,
                        LETTER_NAME = template,
                        LETTER_SIZE = len(a),
                        LETTER_TYPE = mimetype,
                        LETTER = a,
                        CREATED_BY = 'HR',
                        LAST_UPDATED_BY = 'HR'
                        )
        db.session.add(new_pdf)
        db.session.commit()
       
        os.remove(pdfpath)
        return jsonify({"message":"letter succcessfully generated & added to db"}), 201
    # Return the file as a response
        # return send_file(file_obj, mimetype=mimetype)    
    except Exception as e:
        return jsonify({'error':str(e)}),500

def Generateletter():
    try:
       
        frontend_data = request.json
        print("frontend_data",frontend_data)
        Emp_Number = frontend_data['Employee_Number']
        today = date.today()
        # formatted_date = today.strftime("%B %d, %Y")
        # print("temp",formatted_date)
        # return 'string'
        data = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == Emp_Number) & (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= today) &(today <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)).first()
        print("data",data)
        if not data:
            return jsonify ({"error":"employee not found"}),404
        Letter_type = frontend_data['letterType']
        temp_Id = frontend_data['letterId']
        temp = Template.query.filter(Template.TEMPLATE_ID==temp_Id).one()
        print("temp",temp)
        var = temp.TEMPLATE
        text = var.decode('utf-8')
 
        getemployement_details = Employement_Details.query.filter((Employement_Details.EMPLOYEE_ID == data.EMPLOYEE_ID) & (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= today) &(today <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)).first()
        if not getemployement_details:
            return jsonify ({"error":"employement details not found"}),404
        First_Name = data.FIRST_NAME
        print("First_Name",First_Name)
        # Middle_Name = data.MIDDLE_NAME
        Middle_Name = "" if data.MIDDLE_NAME is None else data.MIDDLE_NAME
        print(Middle_Name,"Middle_Name")
        Last_Name = data.LAST_NAME
        Employee_Name = First_Name +" "+Middle_Name+" "+Last_Name
        print("Employee_Name",Employee_Name)
        Name = First_Name + Middle_Name
        Basic_ratio = 0.5
        hra_ratio = 0.4
       
        getemployement_details = Employement_Details.query.filter((Employement_Details.EMPLOYEE_ID == data.EMPLOYEE_ID)
                                                                  & (Employement_Details.EFFECTIVE_START_DATE <= today)
                                                                  &(today <= Employement_Details.EFFECTIVE_END_DATE)).first()
        print("getemployement_details",getemployement_details)
        if not getemployement_details:
            return jsonify ({"error":"employement deatils not found"}),404
        a = getemployement_details.CTC
        # a = request.form.get('CTC')
        print("ctc",a)
        Total_Base_annum = int(a)
        Total_Base_mon = round(Total_Base_annum / 12)
        print("Total_Base_mon",Total_Base_mon)
 
       
        Basic_salary_Annum =round(Total_Base_annum * Basic_ratio)
 
        Basic_month = round(Total_Base_mon * Basic_ratio)
        print("Basic_month",Basic_month)
 
        House_rent_annum = round(Basic_salary_Annum * hra_ratio)
        House_rent_mon = round(Basic_month * hra_ratio)
        print("House_rent_mon",House_rent_mon)
       
        Special_annum = round(Basic_salary_Annum - House_rent_annum)
        Special_mon =round(Basic_month - House_rent_mon)
        print("Special_mon")
 
        Gross_annum =round(Basic_salary_Annum + House_rent_annum + Special_annum)
        Gross_mon = round(Basic_month + House_rent_mon + Special_mon)
        print("Gross_mon",Gross_mon)
 
       
        Company_contribution_m = "-"
        Company_contribution_a = "-"
        Gratuity_annum = round(Basic_salary_Annum * 0.0481)
        Gratuity_month = round(Basic_month * 0.0481)
        print("Gratuity_month",Gratuity_month)
        Insurance_annum = 0
        Insurance_month = 0
        if Gross_mon > 21000:
            Insurance_annum = 25000
            Insurance_month = round(Insurance_annum / 12)
 
       
        print("Insurance_month",Insurance_month)
        Performance_incentiive_annum = "-"
        Performance_incentive_mon = "-"
        print("Performance_incentive_mon",Performance_incentive_mon)
 
        Total_Cost_Company_annum = round(Total_Base_annum + Gratuity_annum + Insurance_annum)
        Total_Cost_Company_mon = round(Total_Base_mon + Gratuity_month + Insurance_month)
        print("Total_Cost_Company_mon",Total_Cost_Company_mon, getemployement_details.ORGANIZATION_NAME[:13])
       
        Effective_start_date = getemployement_details.EFFECTIVE_START_DATE
        formatted_date = Effective_start_date.strftime("%B %d, %Y")
        print("formatted_date",formatted_date)
           
        details = {        
            'EMPLOYEE_NAME':Employee_Name,
            'NAME' : Name,
            'CURRENT_DATE' : today,
            'PERSONAL_EMAIL' : data.EMAIL_ID,
            'EMPLOYEE_NO' : frontend_data['Employee_Number'],
            'JOB_LOCATION' : data.JOB_LOCATION,
            'DATE_OF_JOINING':getemployement_details.DATE_OF_JOINING,
            'TB_annum': "{:,.0f}".format(Total_Base_annum),
            'TB_mon': "{:,.0f}".format(Total_Base_mon),
            'BS_annum' :"{:,.0f}".format(Basic_salary_Annum),
            'BS_mon' : "{:,.0f}".format(Basic_month),
            'HRA_annum' : "{:,.0f}".format(House_rent_annum),
            'HRA_mon' : "{:,.0f}".format(House_rent_mon),
            'SP_annum' : "{:,.0f}".format(Special_annum),
            'SP_mon' : "{:,.0f}".format(Special_mon),
            'GC_annum' : "{:,.0f}".format(Gross_annum),
            'G_mon' : "{:,.0f}".format(Gross_mon),
            'PFM' : Company_contribution_m or 12,
            'PFA' : Company_contribution_a or 13,
            'EFFECTIVE_START_DATE' : formatted_date,
            'DESIGNATION' : getemployement_details.DESIGNATION,
            'PROBATION_PERIOD' : getemployement_details.PROBATION_PERIOD,
            'ORGANIZATION_NAME' : getemployement_details.ORGANIZATION_NAME,
            'ORGANIZATION_NAME_TRIM' : getemployement_details.ORGANIZATION_NAME[:13],
            'CURRENT_COMPANY_EXPERIENCE' : getemployement_details.CURRENT_COMPANY_EXPERIENCE,
            'NOTICE_PERIOD' : getemployement_details.NOTICE_PERIOD,
            'CONFIRMATION_DATE' : getemployement_details.CONFIRMATION_DATE,
            'PRE_ANNUAL_SALARY' : getemployement_details.PRE_ANNUAL_SALARY,
            'Ctc' : getemployement_details.CTC,
            'GRATUITY_annum' : "{:,.0f}".format(Gratuity_annum),
            'GRATUITY_mon' : "{:,.0f}".format(Gratuity_month),
            'INSURANCE_annum' : "{:,.0f}".format(Insurance_annum),
            'INSURANCE_mon' : "{:,.0f}".format(Insurance_month),
            'PI_annum' : Performance_incentiive_annum,
            'LAST_UPDATED_BY' : getemployement_details.LAST_UPDATED_BY,
            'PI_mon' : Performance_incentive_mon,
            'CTC_annum' : "{:,.0f}".format(Total_Cost_Company_annum),
            'CTC_mon' : "{:,.0f}".format(Total_Cost_Company_mon)
        }
        print("Offer details-->",details)
 
        for key, value in details.items():
            print("key",key,value)
           
            text= re.sub(fr'\b{key}\b',str(value),text)
 
 
        print("os.path",os.path,os.getcwd())
        rtf_file_name = 'rtffile.rtf'
        pdf_file_name = 'pdffile.pdf'
        rtf_file_path = os.path.join(os.getcwd(), rtf_file_name)
        print("rtf_file_path",rtf_file_path)
        with open(rtf_file_path, 'wb') as file:
                file.write(text.encode('UTF-8'))
       
 
        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(rtf_file_path)
       
        pdfpath = os.path.join(os.getcwd(), pdf_file_name)
        doc.SaveAs(pdfpath, FileFormat=17)
        print("pdfpath",pdfpath)
        # with open ('D:\\Sample\\HRIT-Project\\sourceCode\\pdffile.pdf','rb') as file:
        with open (pdfpath,'rb') as file:
            a = file.read()
        doc.Close()
        word.Quit()
        pythoncom.CoUninitialize()
        os.remove(rtf_file_path)
        os.remove(pdfpath)
       
 
        # file_obj = BytesIO(a)
        mimetype = mimetypes.MimeTypes().guess_type(pdf_file_name)[0]
        dbdata = Letter.query.filter_by(EMPLOYEE_ID = data.EMPLOYEE_ID, LETTER_NAME = Letter_type).first()
 
        if dbdata:
            print("inside if", dbdata, dbdata.EMPLOYEE_ID)
            dbdata.EMPLOYEE_ID = dbdata.EMPLOYEE_ID
            dbdata.TEMPLATE_ID = dbdata.TEMPLATE_ID
            dbdata.LETTER_NAME = dbdata.LETTER_NAME
            dbdata.LETTER_SIZE = len(a)
            dbdata.LETTER_TYPE = mimetype
            dbdata.LETTER = a
            dbdata.CREATED_BY = 'HR'
            dbdata.LAST_UPDATED_BY = 'HR'
            print("inside if", dbdata, dbdata.EMPLOYEE_ID,dbdata.LETTER_SIZE)
            db.session.commit()
            return jsonify({"message":"letter generated succcessfully & Updated to db"}), 200
 
        new_pdf = Letter(
                        EMPLOYEE_ID=data.EMPLOYEE_ID,
                        TEMPLATE_ID = temp_Id,
                        LETTER_NAME = Letter_type,
                        LETTER_SIZE = len(a),
                        LETTER_TYPE = mimetype,
                        LETTER = a,
                        CREATED_BY = 'HR',
                        LAST_UPDATED_BY = 'HR'
                        )
        db.session.add(new_pdf)
        db.session.commit()
       
        # os.remove(pdfpath)
        return jsonify({"message":"letter succcessfully generated & added to db"}), 201
    # Return the file as a response
        # return send_file(file_obj, mimetype=mimetype)    
    except Exception as e:
        return jsonify({'error':str(e)}),500

def viewpdf():
    try:
        temp_Id = request.args.get('param1')
        Emp_Number = request.args.get('param2')
        print('Emp_Number---->',temp_Id,Emp_Number)
        today = date.today()
        data = EMPLOYEE_DETAILS.query.filter((EMPLOYEE_DETAILS.EMPLOYEE_NUMBER == Emp_Number) & (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= today) &(today <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)).first()
        print("data",data)
        if not data:
            return jsonify ({"error":"employee not found"}),404
        emp_id = data.EMPLOYEE_ID
        # temp_Id = dataa['letterId']
        letter = Letter.query.filter((Letter.EMPLOYEE_ID == emp_id) & (Letter.TEMPLATE_ID == temp_Id)).first()
        print('letter',letter)
        if not letter:
            return jsonify ({"error":"letter not found"}),404
        pdf = letter.LETTER
        # pdfread = pdf.read()
 
        file_obj = BytesIO(pdf)
        # mimetype = mimetypes.MimeTypes().guess_type(pdf)[0]
        return send_file(file_obj, mimetype=letter.LETTER_TYPE)
    except Exception as e:
        return jsonify({'error':str(e)}),500