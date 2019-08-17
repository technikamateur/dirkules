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
    last_update = db.Column(DateTime)
    missing = db.Column(db.Boolean)
    partitions = db.relationship('Partitions', order_by="Partitions.id", backref="drive", lazy="select")

    def __init__(self, name, model, serial, size, rota, rm, hotplug, state, smart, time, missing=False):
        self.name = name
        self.model = model
        self.serial = serial
        self.size = size
        self.rota = rota
        self.rm = rm
        self.hotplug = hotplug
        self.state = state
        self.smart = smart
        self.last_update = time
        self.missing = missing

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.smart == other.smart
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Partitions(db.Model):
    __tablename__ = 'partitions'
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drives.id'), nullable=False)
    name = db.Column(db.String)
    fs = db.Column(db.String)
    size = db.Column(db.Integer)
    uuid = db.Column(db.String)
    mountpoint = db.Column(db.String)
    label = db.Column(db.String)

    def __init__(self, drive_id, name, label, fs, size, uuid, mpoint, drive):
        self.drive_id = drive_id
        self.name = name
        self.label = label
        self.fs = fs
        self.size = size
        self.uuid = uuid
        self.mountpoint = mpoint
        self.drive = drive


class Pool(db.Model):
    __tablename__ = 'pool'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    size = db.Column(db.Integer)
    free = db.Column(db.Integer)
    data_raid = db.Column(db.String)
    meta_raid = db.Column(db.String)
    data_ratio = db.Column(db.Float)
    meta_ratio = db.Column(db.Float)
    fs = db.Column(db.String)
    mountpoint = db.Column(db.String)
    mountopt = db.Column(db.String)
    drives = db.Column(db.String)

    def __init__(self, label, size, free, data_raid, data_ratio, meta_raid, meta_ratio, fs, mountpoint, mountopt,
                 drives):
        self.label = label
        self.size = size
        self.free = free
        self.data_raid = data_raid
        self.data_ratio = data_ratio
        self.meta_raid = meta_raid
        self.meta_ratio = meta_ratio
        self.fs = fs
        self.mountpoint = mountpoint
        self.mountopt = mountopt
        self.drives = drives


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
