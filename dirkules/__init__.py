import dirkules.config as config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import dirkules.com

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

import dirkules.models
db.create_all()
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
communicator = com.TelegramCom(app)


#@app.before_first_request
from dirkules import tasks


# from dirkules.models import Time
# from sqlalchemy.orm.exc import NoResultFound
#
# try:
#     Time.query.one()
# except NoResultFound:
#     db.session.add(Time("Drives"))
#     db.session.commit()

import dirkules.views
