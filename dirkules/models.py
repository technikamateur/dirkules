import time

from dirkules import db


class Drive(db.Model):
   __tablename__ = 'drives'
   id = db.Column(Integer, primary_key=True)
   path = db.Column(String)
   storage = db.Column(Integer)
   message = db.Column(String)
   observed = db.Column(Boolean)
   statuse = relationship("Drive_status")

class Drive_status(db.Model):
    __tablename__ = 'drive_status'
    id = Column(Integer, primary_key=True)
    drive_id = Column(Integer, ForeignKey('drive.id'))
