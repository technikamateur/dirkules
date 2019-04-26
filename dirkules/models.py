from dirkules import db
from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


class Drive(db.Model):
    __tablename__ = 'drives'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    model = db.Column(db.String)
    serial = db.Column(db.String)
    size = db.Column(db.Integer)
    rota = db.Column(db.Boolean)
    rm = db.Column(db.Boolean)
    hotplug = db.Column(db.Boolean)
    state = db.Column(db.String)
    smart = db.Column(db.Boolean)
    partitions = db.relationship("Partitions")

    def __init__(self, name, model, serial, size, rota, rm, hotplug, state, smart):
        self.name = name
        self.model = model
        self.serial = serial
        self.size = size
        self.rota = rota
        self.rm = rm
        self.hotplug = hotplug
        self.state = state
        self.smart = smart


class Partitions(db.Model):
    __tablename__ = 'partitions'
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drives.id'))
    name = db.Column(db.String)
    fs = db.Column(db.String)
    size =db.Column(db.String)
    uuid = db.Column(db.String)
    mountpoint = db.Column(db.String)
    label = db.Column(db.String)


class Time(db.Model):
    __tablename__ = 'time'
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String)
    time = db.Column(db.Integer, default=0, onupdate=1)

    def __init__(self, desc):
        self.desc = desc


class Cleaning(db.Model):
    __tablename__ = 'cleaning'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    path = db.Column(db.String)
    time = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, name, path):
        self.name = name
        self.path = path
