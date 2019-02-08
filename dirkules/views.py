from flask import Flask, render_template
from dirkules import app
import dirkules.driveManagement.driveController as drico

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/drives', methods=['GET'])
def drives():
    drives = drico.getAllDrives()
    return render_template('drives.html', drives=drives)

@app.route('/about', methods=['GET'])
def about():
    version = "1.0"
    return render_template('about.html', version=version)
