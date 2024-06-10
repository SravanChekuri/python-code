from datetime import datetime
from config import db
from app import Flask_app
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from werkzeug.security import generate_password_hash,check_password_hash




class Admin(db.Model):
   __tablename__ = "admindetails"
 
 
 
   USER_ID = db.Column(db.String(30), primary_key=True)
   EFFECTIVE_START_DATE = db.Column(db.DateTime, primary_key=True)
   EFFECTIVE_END_DATE = db.Column(db.DateTime, primary_key=True)
   FIRST_NAME = db.Column(db.String(150), nullable=False)
   MIDDLE_NAME = db.Column(db.String(150))
   LAST_NAME = db.Column(db.String(150))
   EMAIL_ID =db.Column(db.String(150), nullable=False,unique=True)
   PASSWORD = db.Column(db.String(100), nullable = False)
   MOBILE_NUMBER= db.Column(db.String(150))
   ROLE = db.Column(db.String(150), nullable=False)
   CREATED_BY =db.Column(db.String(150))
   LAST_UPDATED_BY =db.Column(db.String(150))
   CREATION_DATE = db.Column(db.DateTime, default=datetime.now)
   LAST_UPDATED_DATE = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
   
 
 
   def serialize(self):
       return{
           "USER_ID" : self.USER_ID,
           "FIRST_NAME" : self.FIRST_NAME,
           "MIDDLE_NAME" : self.MIDDLE_NAME,
           "LAST_NAME" : self.LAST_NAME,
        #    'password' : self.password,
           "EMAIL_ID" : self.EMAIL_ID,
           "MOBILE_NUMBER" : self.MOBILE_NUMBER,
           "EFFECTIVE_START_DATE" : self.EFFECTIVE_START_DATE,
           "EFFECTIVE_END_DATE" : self.EFFECTIVE_END_DATE,
           "CREATION_DATE" : self.CREATION_DATE,
           "CREATED_BY" : self.CREATED_BY,
           "LAST_UPDATED_DATE" : self.LAST_UPDATED_DATE,
           "LAST_UPDATED_BY" : self.LAST_UPDATED_BY
       }