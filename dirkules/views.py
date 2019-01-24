from flask import Flask, render_template
from dirkules import app
import dirkules.monitoring.monitoringController as moco

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/monitoring', methods=['GET'])
def monitoring():
    drives = moco.getAllDrives()
    return render_template('monitoring.html', drives=drives)

@app.route('/about', methods=['GET'])
def about():
    version = "1.0"
    return render_template('about.html', version=version)
