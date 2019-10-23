from dirkules import db


class SambaGlobal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    element = db.Column(db.String)
    value = db.Column(db.String)

    def __init__(self, element, value):
        self.element = element
        self.value = value


class SambaShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    recycle = db.Column(db.Boolean)
    btrfs = db.Column(db.Boolean)
    options = db.relationship('SambaOption', order_by="SambaOption.id", backref="samba_share", lazy="select",
                              cascade="all, delete-orphan")

    def __init__(self, name, path, recycle=False, btrfs=False):
        self.name = name
        self.path = path
        self.recycle = recycle
        self.btrfs = btrfs


class SambaOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sambashare_id = db.Column(db.Integer, db.ForeignKey('samba_share.id'))
    option = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)

