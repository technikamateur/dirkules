import datetime
import subprocess
from time import sleep
from flask import render_template, redirect, request, url_for, flash, abort
from dirkules import app, db, scheduler
import dirkules.manager.serviceManager as servMan
import dirkules.manager.cleaning as cleaningMan
from dirkules.models import Drive, Cleaning, SambaShare, Pool
import dirkules.manager.viewManager as viewManager
from dirkules.validation.validators import CleaningForm, SambaCleaningForm, SambaAddForm, PoolAddForm
from dirkules.config import staticDir


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=str(e))


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', error=str(e))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', service=servMan.service_state())


@app.route('/drives', methods=['GET'])
def drives():
    drives = Drive.query.all()
    return render_template('drives.html', drives=drives)


@app.route('/pools', methods=['GET'])
def pools():
    pools = Pool.query.all()
    return render_template('pools.html', pools=pools)


@app.route('/pool/<pool>', methods=['GET'])
def pool(pool):
    db_pool = Pool.query.get(pool)
    if db_pool is None:
        abort(404, description="Pool with ID {} could not be found.".format(pool))
    pool_health = viewManager.get_pool_health(db_pool.drives)
    return render_template('pool.html', pool=db_pool, health=pool_health)


@app.route('/pools/add', methods=['GET', 'POST'])
def add_pool():
    form = PoolAddForm(request.form)
    form.drives.choices = viewManager.get_empty_drives()
    if request.method == 'POST' and form.validate():
        try:
            viewManager.create_btrfs_pool(form)
        except subprocess.CalledProcessError as e:
            abort(500, description="While creating a pool, the following exception occured: {}".format(e))
        except subprocess.TimeoutExpired as e:
            abort(500, description="Pool creation took too long: {}".format(e))
        scheduler.get_job("refresh_disks").modify(next_run_time=datetime.datetime.now())
        sleep(1)
        return redirect(url_for('pools'))
    return render_template('pool_add.html', form=form)


@app.route('/about', methods=['GET'])
def about():
    version = "1.0"
    return render_template('about.html', version=version)


@app.route('/partitions/<part>', methods=['GET'])
def partitions(part):
    name = part.replace("_", "/")
    drive = db.session.query(Drive).filter(Drive.name == name).scalar()
    return render_template('partitions.html', parts=drive.partitions)


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
        viewManager.create_cleaning_obj(form.jobname.data, form.path.data, form.active.data)
        return redirect(url_for('cleaning'))
    return render_template('add_cleaning.html', form=form)


@app.route('/samba', methods=['GET'])
def samba():
    shares = SambaShare.query.order_by(db.asc(db.collate(SambaShare.name, 'NOCASE'))).all()
    return render_template('samba.html', shares=shares)


@app.route('/samba/global', methods=['GET', 'POST'])
def samba_global():
    form = SambaCleaningForm(request.form)
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


@app.route('/samba/add', methods=['GET', 'POST'])
def samba_add():
    form = SambaAddForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('samba'))
    return render_template('samba_add.html', form=form)
