import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

baseDir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    baseDir, 'dirkules.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import dirkules.models
db.create_all()

import dirkules.views
