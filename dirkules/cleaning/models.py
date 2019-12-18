import datetime

from dirkules import db


class Cleaning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    path = db.Column(db.String)
    # active: 0 means inactive - do not execute
    active = db.Column(db.Boolean)
    # time means last execution
    time = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)

    def __init__(self, name, path, active=False):
        self.name = name
        self.path = path
        self.active = active

    def change_active(self):
        if self.active:
            self.active = False
        else:
            self.active = True
