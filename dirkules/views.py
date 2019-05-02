from flask import Flask, render_template, redirect, request, url_for, flash
from dirkules import app, db
import dirkules.driveManagement.driveController as drico
import dirkules.serviceManagement.serviceManager as servMan
from dirkules.models import Drive, Cleaning, SambaShare
import dirkules.viewManager.viewManager as viewManager
from dirkules.validation.validators import CleaningForm, samba_cleaning_form
from sqlalchemy import asc, collate
from dirkules.config import staticDir


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', service=servMan.service_state())


@app.route('/drives', methods=['GET'])
def drives():
    dbDrives = []
    print(Drive.query.all())
    for drive in Drive.query.all():
        d = viewManager.db_object_as_dict(drive)
        dbDrives.append(d)
    return render_template('drives.html', drives=dbDrives)


@app.route('/about', methods=['GET'])
def about():
    version = "1.0"
    return render_template('about.html', version=version)


@app.route('/partitions/<part>', methods=['GET'])
def partitions(part):
    part = part.replace("_", "/")
    parts = drico.getPartitions(part)
    return render_template('partitions.html', parts=parts)


@app.route('/cleaning', methods=['GET'])
def cleaning():
    remove = request.args.get('remove')
    changestate = request.args.get('changestate')
    if not (remove is not None and changestate is not None):
        if remove is not None:
            Cleaning.query.filter(Cleaning.id == int(remove)).delete()
            db.session.commit()
            return redirect(request.path, code=302)
        elif changestate is not None:
            job = Cleaning.query.get(int(changestate))
            if job.state == 0:
                job.state = 1
            else:
                job.state = 0
            db.session.commit()
            return redirect(request.path, code=302)
    else:
        flash("Auswahl nicht eindeutig!")
    elements = []
    for element in Cleaning.query.order_by(asc(collate(Cleaning.name, 'NOCASE'))).all():
        elements.append(viewManager.db_object_as_dict(element))
    return render_template('cleaning.html', elements=elements)


@app.route('/add_cleaning', methods=['GET', 'POST'])
def add_cleaning():
    form = CleaningForm(request.form)
    if request.method == 'POST' and form.validate():
        viewManager.create_cleaning_obj(form.jobname.data, form.path.data, form.active.data)
        return redirect(url_for('cleaning'))
    return render_template('add_cleaning.html', form=form)

@app.route('/samba', methods=['GET'])
def samba():
    shares = []
    for share in SambaShare.query.order_by(asc(collate(SambaShare.name, 'NOCASE'))).all():
        shares.append(viewManager.db_object_as_dict(share))
    return render_template('samba.html', shares=shares)

@app.route('/samba/global', methods=['GET', 'POST'])
def samba_global():
    db.session.add(SambaShare("global"))
    db.session.commit()
    form = samba_cleaning_form(request.form)
    if request.method == 'POST' and form.validate():
        print("Input:")
        print(form.workgroup.data)
        print(form.server_string.data)
        return redirect(url_for('samba_global'))
    file = open(staticDir + "/conf/samba_global.conf")
    conf = list()
    while True:
        line = file.readline()
        if line != '':
            conf.append(line.rstrip())
        else:
            break
    return render_template('samba_global.html', form=form, conf=conf)