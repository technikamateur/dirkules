import datetime
import subprocess
from time import sleep
from flask import render_template, redirect, request, url_for, abort
from dirkules import app, scheduler, app_version
import dirkules.manager.serviceManager as servMan
import dirkules.manager.driveManager as driveMan
from dirkules.models import Drive, Pool
import dirkules.manager.viewManager as viewManager
from dirkules.validation.validators import PoolAddForm


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=str(e))


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', error=str(e))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', service=servMan.service_state())


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
