import datetime
import subprocess
from time import sleep
from flask import render_template, redirect, request, url_for, flash, abort
from dirkules import app, db, scheduler, app_version
import dirkules.manager.serviceManager as servMan
import dirkules.manager.driveManager as driveMan
import dirkules.manager.cleaning as cleaningMan
from dirkules.models import Drive, Cleaning, Pool
import dirkules.manager.viewManager as viewManager
from dirkules.validation.validators import CleaningForm, PoolAddForm


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
    delete = request.args.get('delete')
    if delete is not None:
        try:
            drive = driveMan.get_drive_by_id(int(delete))
            driveMan.delete_drive(drive)
        except ValueError:
            abort(500, description="Expected int, but got {}.".format(delete))
        except LookupError:
            abort(500, description="Invalid drive id {}".format(delete))

    return render_template('drives.html', drives=Drive.query.all())


@app.route('/pools', methods=['GET'])
def pools():
    return render_template('pools.html', pools=Pool.query.all())


@app.route('/pool/<pool>', methods=['GET'])
def pool(pool):
    db_pool = Pool.query.get(pool)
    if db_pool is None:
        abort(404, description="Pool with ID {} could not be found.".format(pool))
    return render_template('pool.html', pool=db_pool)


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
    return render_template('about.html', version=app_version)


@app.route('/partitions/<part>', methods=['GET'])
def partitions(part):
    try:
        drive = driveMan.get_drive_by_id(int(part))
    except ValueError:
        abort(500, description="Expected int, but got {}.".format(part))
    except LookupError:
        abort(500, description="Invalid drive id {}".format(part))
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
