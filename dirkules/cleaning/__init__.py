from flask import Blueprint

bp_cleaning = Blueprint('cleaning', __name__, template_folder='templates')
from dirkules.cleaning import views
