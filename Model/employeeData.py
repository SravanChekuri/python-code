from datetime import datetime
from config import db
from app import Flask_app
from sqlalchemy.orm import relationship
# from sqlalchemy import DateTime,Foreignkey
from werkzeug.security import generate_password_hash,check_password_hash

    






class EMPLOYEE_DETAILS(db.Model):
   __tablename__ = "employeedetails"
 
   EMPLOYEE_ID = db.Column(db.Integer,autoincrement=True, primary_key=True)
   EMPLOYEE_NUMBER = db.Column(db.String(15),nullable=False)
   EFFECTIVE_START_DATE = db.Column(db.Date, primary_key=True)
   EFFECTIVE_END_DATE = db.Column(db.Date, primary_key=True)
   FIRST_NAME = db.Column(db.String(150),nullable=False)
   MIDDLE_NAME = db.Column(db.String(150))
   LAST_NAME = db.Column(db.String(150),nullable=False)
   DATE_OF_BIRTH = db.Column(db.Date,nullable=False)
   JOB_LOCATION = db.Column(db.String(150))
   WORKER_TYPE = db.Column(db.String(15),nullable=False)
   MOBILE_NO = db.Column(db.String(10))
   USER_ID = db.Column(db.String(30), db.ForeignKey('admindetails.USER_ID'))
   EMAIL_ID = db.Column(db.String(150))
   CREATED_BY = db.Column(db.String(150))
   LAST_UPDATED_BY = db.Column(db.String(150))
   CREATION_DATE = db.Column(db.DateTime, default=datetime.now)
   LAST_UPDATED_DATE = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
   
 
 
   
   
 
   def serialize(self):
       return{
           "Employee_id" : self.EMPLOYEE_ID,
           "Employee_Number" : self.EMPLOYEE_NUMBER,
           "Employee_First_Name" : self.FIRST_NAME,
           "Middle_Name" : self.MIDDLE_NAME,
           "Last_Name" : self.LAST_NAME,
           'USER_ID' : self.USER_ID,
           "DATE_OF_BIRTH" : self.DATE_OF_BIRTH,
           "MOBILE_NO" : self.MOBILE_NO,
           "EFFECTIVE_START_DATE" : self.EFFECTIVE_START_DATE,
           "EFFECTIVE_END_DATE" : self.EFFECTIVE_END_DATE,
           "JOB_LOCATION" : self.JOB_LOCATION,
           "WORKER_TYPE" : self.WORKER_TYPE,
           "Email" : self.EMAIL_ID,
           "Creation_date" : self.CREATION_DATE,
           "Created_by" : self.CREATED_BY,
           "Last_Updated_Date" : self.LAST_UPDATED_DATE,
           "Last_Updated_by" : self.LAST_UPDATED_BY
       }

    



    
    