from datetime import datetime
from config import db
from app import Flask_app
from sqlalchemy.orm import relationship



class Address_Details(db.Model):
   __tablename__ = "addressdetails"
 
 
   ADDRESS_ID = db.Column(db.Integer, autoincrement=True, primary_key=True)                    
   EMPLOYEE_ID = db.Column(db.Integer, db.ForeignKey('employeedetails.EMPLOYEE_ID'))
   DATE_FROM = db.Column(db.Date, primary_key=True)        
   DATE_TO = db.Column(db.Date, primary_key=True)        
   ADDRESS_TYPE   = db.Column(db.String(150))    
   ADDRESS = db.Column(db.String(150),nullable=False)  
   CITY  = db.Column(db.String(150),nullable=False)
   STATE = db.Column(db.String(150),nullable=False)            
   COUNTRY = db.Column(db.String(150),nullable=False)        
   PIN_CODE = db.Column(db.String(15),nullable=False)            
   CREATED_BY = db.Column(db.String(150))
   LAST_UPDATED_BY = db.Column(db.String(150))
   CREATION_DATE = db.Column(db.DateTime, default=datetime.now)
   LAST_UPDATED_DATE = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
 
 
   def serialize(self):
      return{
         "ADDRESS_ID" : self.ADDRESS_ID,
         "EMPLOYEE_ID" : self.EMPLOYEE_ID,
         "ADDRESS_TYPE" : self.ADDRESS_TYPE,
         "ADDRESS" : self.ADDRESS,
         "CITY" : self.CITY,
         "STATE" : self.STATE,
         "COUNTRY" : self.COUNTRY,
         "PIN_CODE" : self.PIN_CODE,
         "DATE_FROM" : self.DATE_FROM,
         "DATE_TO" :self.DATE_TO,
         "CREATED_BY" : self.CREATED_BY,
         "LAST_UPDATED_BY" : self.LAST_UPDATED_BY,
         "CREATION_DATE" : self.CREATION_DATE,
         "LAST_UPDATED_DATE" : self.LAST_UPDATED_DATE
      }





class Employement_Details(db.Model):
   __tablename__ = 'employementdetails'
 
   ASSIGNMENT_ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
   EMPLOYEE_ID = db.Column(db.Integer, db.ForeignKey('employeedetails.EMPLOYEE_ID'))
   EFFECTIVE_START_DATE = db.Column(db.Date, primary_key=True)
   EFFECTIVE_END_DATE = db.Column(db.Date, primary_key=True)
   DATE_OF_JOINING = db.Column(db.Date, nullable = False)
   ORGANIZATION_NAME = db.Column(db.String(300), nullable = False)
   DESIGNATION = db.Column(db.String(400), nullable = False )
   DEPARTMENT =db.Column(db.String(400))
   PERSON_TYPE = db.Column(db.String(70), nullable = False)
   CONFIRMATION_DATE = db.Column(db.Date)
   CTC = db.Column(db.Float(precision=2), nullable = False)
   STATUS = db.Column(db.String(40))
   PROBATION_PERIOD = db.Column(db.String(30), nullable = False)
   NOTICE_PERIOD = db.Column(db.String(30))
   CURRENT_COMPANY_EXPERIENCE = db.Column(db.String(30))
   PREVIOUS_EXPERIENCE = db.Column(db.String(30))
   TOTAL_EXPERIENCE = db.Column(db.String(30))
   PRE_ANNUAL_SALARY = db.Column(db.String(30))
   CREATED_BY = db.Column(db.String(300))
   LAST_UPDATED_BY = db.Column(db.String(300))
   CREATION_DATE = db.Column(db.DateTime, default=datetime.now)                  
   LAST_UPDATED_DATE = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
 
 
   def serialize(self):
      return{
         "ASSIGNMENT_ID" : self.ASSIGNMENT_ID,
         "EMPLOYEE_ID" : self.EMPLOYEE_ID,
         "ORGANIZATION_NAME" : self.ORGANIZATION_NAME,
         "DESIGNATION" : self.DESIGNATION,
         "DATE_OF_JOINING" : self.DATE_OF_JOINING,
         "PERSON_TYPE" : self.PERSON_TYPE,
         "DEPARTMENT" : self.DEPARTMENT,
         "CONFIRMATION_DATE" : self.CONFIRMATION_DATE,
         "STATUS" : self.STATUS,
         "PROBATION_PERIOD" : self.PROBATION_PERIOD,
         "NOTICE_PERIOD" : self.NOTICE_PERIOD,
         "CURRENT_COMPANY_EXPERIENCE" : self.CURRENT_COMPANY_EXPERIENCE,
         "PREVIOUS_EXPERIENCE" : self.PREVIOUS_EXPERIENCE,
         "TOTAL_EXPERIENCE" : self.TOTAL_EXPERIENCE,
         "CTC" : self.CTC,
         "PRE_ANNUAL_SALARY" : self.PRE_ANNUAL_SALARY,
         "EFFECTIVE_START_DATE" : self.EFFECTIVE_START_DATE,
         "EFFECTIVE_END_DATE" : self.EFFECTIVE_END_DATE,
         "CREATED_BY" : self.CREATED_BY,
         "LAST_UPDATED_BY" : self.LAST_UPDATED_BY,
         "CREATION_DATE" : self.CREATION_DATE,
         "LAST_UPDATED_DATE" : self.LAST_UPDATED_DATE
      }   