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


class Partitions(db.Model):
    __tablename__ = 'partitions'
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drives.id'))
    name = db.Column(db.String)
    fs = db.Column(db.String)
    uuid = db.Column(db.String)
    mountpoint = db.Column(db.String)
    label = db.Column(db.String)
