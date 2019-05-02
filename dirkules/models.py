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
    size = db.Column(db.String)
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
    # state 0 means inactive - do not execute
    state = db.Column(db.Boolean)
    # time means last execution
    time = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, name, path, state):
        self.name = name
        self.path = path
        self.state = state


class SambaShare(db.Model):
    __tablename__ = 'samba_share'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    writeable = db.Column(db.Boolean)
    recycling = db.Column(db.Boolean)
    btrfs = db.Column(db.Boolean)
    options = db.relationship('SambaOptions', order_by="SambaOptions.id", backref="samba_share", lazy="select")

    def __init__(self, name, writeable=False, recycling=False, btrfs=False):
        self.name = name
        self.writeable = writeable
        self.recycling = recycling
        self.btrfs = btrfs


class SambaOptions(db.Model):
    __tablename__ = 'samba_options'
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    sambashare_id = db.Column(db.Integer, db.ForeignKey('samba_share.id'), nullable=False)
