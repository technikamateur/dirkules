import datetime

from flask_wtf import CSRFProtect
import dirkules.config as config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
csrf = CSRFProtect()
csrf.init_app(app)
app_version = app.config["VERSION"]

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)

import dirkules.models
import dirkules.samba.models
import dirkules.cleaning.models

# create db if not exists
db.create_all()
# start scheduler
scheduler.start()
# import views
import dirkules.views

from .drives.views import bp_drives as bp_drives
from .samba.views import bp_samba as bp_samba
from .cleaning.views import bp_cleaning as bp_cleaning

app.register_blueprint(bp_drives, url_prefix='/drives')
app.register_blueprint(bp_samba, url_prefix='/samba')
app.register_blueprint(bp_cleaning, url_prefix='/cleaning')

from dirkules.models import Drive


@app.before_request
def check_drives():
    if Drive.query.first() is None:
        scheduler.get_job("refresh_disks").modify(next_run_time=datetime.datetime.now())
