from flask import request, redirect, flash, render_template, url_for

from dirkules import app, db
from dirkules.cleaning.manager import create_cleaning_obj
from dirkules.cleaning.models import Cleaning


@app.route('/cleaning', methods=['GET'])
def cleaning():
    remove = request.args.get('remove')
    changestate = request.args.get('changestate')
    service = request.args.get('service')
    if not (remove is not None and changestate is not None):
        if remove is not None:
            try:
                remove = int(remove)
                Cleaning.query.filter(Cleaning.id == remove).delete()
                db.session.commit()
                return redirect(request.path, code=302)
            except ValueError:
                flash("Value Error: remove")
        elif changestate is not None:
            try:
                changestate = int(changestate)
                job = Cleaning.query.get(changestate)
                if job.state == 0:
                    job.state = 1
                else:
                    job.state = 0
                db.session.commit()
                return redirect(request.path, code=302)
            except ValueError:
                flash("Value Error: changestate")
    else:
        flash("Value Error: remove and changestate set")
    if service is not None:
        try:
            service = str(service)
            if service == "start":
                if not cleaningMan.running():
                    cleaningMan.enable()
                    return redirect(request.path, code=302)
                else:
                    flash("Error: Cleaning Service already running.")
            elif service == "pause":
                if cleaningMan.running():
                    cleaningMan.disable()
                    return redirect(request.path, code=302)
                else:
                    flash("Error: Cleaning Service already paused.")
            else:
                raise ValueError
        except ValueError:
            flash("Value Error: service")
    elements = Cleaning.query.order_by(db.asc(db.collate(Cleaning.name, 'NOCASE'))).all()
    return render_template('cleaning.html', elements=elements, task_running=cleaningMan.running())


@app.route('/add_cleaning', methods=['GET', 'POST'])
def add_cleaning():
    form = CleaningForm(request.form)
    if request.method == 'POST' and form.validate():
        create_cleaning_obj(form.jobname.data, form.path.data, form.active.data)
        return redirect(url_for('cleaning'))
    return render_template('add_cleaning.html', form=form)