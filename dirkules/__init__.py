import os

import dirkules.models
import dirkules.views
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

baseDir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    baseDir, 'dirkules.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()
