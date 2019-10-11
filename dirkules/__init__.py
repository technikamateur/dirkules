from flask_wtf import csrf, CSRFProtect
import dirkules.config as config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
csrf = CSRFProtect()
csrf.init_app(app)
app_version = app.config["version"]

import dirkules.models
import dirkules.samba.models

# create db if not exists
db.create_all()
# start scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
# import views
import dirkules.views

from dirkules.samba import bp_samba as bp_samba
app.register_blueprint(bp_samba, url_prefix='/samba')
