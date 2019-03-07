import dirkules.config as config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

import dirkules.models
db.create_all()

from dirkules.models import Time
from sqlalchemy.orm.exc import NoResultFound

try:
    Time.query.one()
except NoResultFound:
    db.session.add(Time("Drives"))
    db.session.commit()

import dirkules.views
