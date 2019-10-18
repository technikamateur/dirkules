from flask import Blueprint

bp_samba = Blueprint('samba', __name__, template_folder='templates')
from dirkules.samba import views
