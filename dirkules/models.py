from dirkules import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class Drive(db.Model):
    __tablename__ = 'drives'
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String)
    name = db.Column(db.String)
    size = db.Column(db.Integer)
    smart = db.Column(db.Boolean)
    partitions = db.relationship("Partitions")

    def __init__(self, device, name, smart, size):
        self.device = device
        self.name = name
        self.smart = smart
        self.size = size


class Partitions(db.Model):
    __tablename__ = 'partitions'
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drives.id'))
    name = db.Column(db.String)
    fs = db.Column(db.String)
    uuid = db.Column(db.String)
    mountpoint = db.Column(db.String)
    label = db.Column(db.String)


class Times(db.Model):
    __tablename__ = 'times'
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String)
    time = db.Column(db.Integer, default=0, onupdate=1)

    def __init__(self, desc, time):
        self.desc = desc
        self.time = time
