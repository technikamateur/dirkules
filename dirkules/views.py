from flask import render_template
from dirkules import app, app_version
import dirkules.manager.serviceManager as servMan


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=str(e))


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', error=str(e))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', service=servMan.service_state())


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', version=app_version)
