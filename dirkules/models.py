import time
from dirkules import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Drive(Base):
   __tablename__ = 'drives'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String)
   path = db.Column(db.String)
   storage = db.Column(db.Integer)
   observed = db.Column(db.Boolean)
   statuse = db.relationship("Drive_status")

class Drive_status(Base):
    __tablename__ = 'drive_status'
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'))
    smart = db.Column(db.Boolean)
    operating_hours = db.Column(db.Integer)
    startups = db.Column(db.Integer)
    startups = db.Column(db.Integer)
    time = db.Column(db.Integer)
