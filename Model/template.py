from datetime import datetime
from config import db
from app import Flask_app
from sqlalchemy import Column, Integer, String, DateTime






class Template(db.Model):
   __tablename__ = 'templates'

   TEMPLATE_ID = db.Column(db.String(15),primary_key=True)
   TEMPLATE_NAME = db.Column(db.String(150),nullable = False)
   TEMPLATE = db.Column(db.LargeBinary(length=20 * (1024 * 1024)))
   TEMPLATE_SIZE = db.Column(db.Integer)
   TEMPLATE_TYPE = db.Column(db.String(150))
   CREATED_BY = db.Column(db.String(150))
   LAST_UPDATED_BY = db.Column(db.String(150))
   CREATION_DATE = db.Column(db.DateTime, default=datetime.now)
   LAST_UPDATED_DATE = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


def serialize(self):
        return{
            'TEMPLATE_ID' : self.TEMPLATE_ID,
            'TEMPLATE_NAME' : self.TEMPLATE_NAME,
            'TEMPLATE_SIZE' :self.TEMPLATE_SIZE,
            'TEMPLATE_TYPE' :self.TEMPLATE_TYPE,
            'CREATED_BY' : self.CREATED_BY,
            'CREATION_DATE' : self.CREATION_DATE,
            'LAST_UPDATED_BY' : self.LAST_UPDATED_BY,
            'LAST_UPDATED_DATE' : self.LAST_UPDATED_DATE
        }


class Letter(db.Model):
    __tablename__ = 'letters'
 
    LETTER_ID = db.Column(db.Integer,autoincrement=True, primary_key=True)
    EMPLOYEE_ID = db.Column(db.Integer, db.ForeignKey('employeedetails.EMPLOYEE_ID'))
    TEMPLATE_ID = db.Column(db.String(150), db.ForeignKey('templates.TEMPLATE_ID'))
    LETTER_SIZE = db.Column(db.Integer)
    LETTER_NAME = db.Column(db.String(150),nullable = False)
    LETTER = db.Column(db.LargeBinary(length=20 * (1024 * 1024)))
    LETTER_TYPE = db.Column(db.String(150))
    CREATED_BY = db.Column(db.String(150))
    LAST_UPDATED_BY = db.Column(db.String(150))
    CREATION_DATE = db.Column(db.DateTime, default=datetime.now)
    LAST_UPDATED_DATE = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
 
    def serialize(self):
        return{
            'LETTER_ID' : self.LETTER_ID,
            'EMPLOYEE_ID' : self.EMPLOYEE_ID,
            'TEMPLATE_ID' : self.TEMPLATE_ID,
            'LETTER_SIZE' :self.LETTER_SIZE,
            'LETTER_NAME' : self.LETTER_NAME,
            'LETTER' : self.LETTER,
            'LETTER_TYPE' : self.LETTER_TYPE,
            'CREATED_BY' : self.CREATED_BY,
            'LAST_UPDATED_BY' : self.LAST_UPDATED_BY,
            'CREATION_DATE' : self.CREATION_DATE,
            'LAST_UPDATED_DATE' : self.LAST_UPDATED_DATE
        }