import dirkules.config as config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import dirkules.TelegramCom

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

import dirkules.models

# create db if not exists
db.create_all()
# start communication
communicator = TelegramCom.TelegramCom(app)
# start scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
# import views
import dirkules.views
