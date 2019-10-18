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
    writeable = db.Column(db.Boolean)
    recycling = db.Column(db.Boolean)
    btrfs = db.Column(db.Boolean)
    options = db.relationship('SambaOptions', order_by="SambaOptions.id", backref="samba_share", lazy="select",
                              cascade="all, delete-orphan")

    def __init__(self, name, writeable=False, recycling=False, btrfs=False):
        self.name = name
        self.writeable = writeable
        self.recycling = recycling
        self.btrfs = btrfs


class SambaOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    sambashare_id = db.Column(db.Integer, db.ForeignKey('samba_share.id'), nullable=False)
