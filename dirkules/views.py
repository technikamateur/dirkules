from flask import Flask, render_template
from dirkules import app
import dirkules.driveManagement.driveController as drico
from dirkules.models import Drive


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/drives', methods=['GET'])
def drives():
    drives = drico.getAllDrives()
    #print(Drive.query.filter_by(device='/dev/sda').all())
    test = drico.getPartitions("/dev/sdb")
    print(test)
    return render_template('drives.html', drives=drives)


@app.route('/about', methods=['GET'])
def about():
    version = "1.0"
    return render_template('about.html', version=version)


@app.route('/partitions', methods=['GET'])
def partitions():
    return render_template('partitions.html')
