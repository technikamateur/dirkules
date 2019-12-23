import datetime
import subprocess
from time import sleep

from dirkules import scheduler

from . import manager
from dirkules.models import Pool
from flask import Blueprint, render_template, abort, redirect, url_for, request

from .validation import PoolAddForm

bp_pools = Blueprint('pools', __name__, template_folder='templates')


@bp_pools.route('/', methods=['GET'])
def index():
    return render_template('pools/index.html', pools=Pool.query.all())


@bp_pools.route('/<pool>', methods=['GET'])
def detail(pool):
    try:
        db_pool = Pool.query.get_or_404(int(pool))
    except ValueError:
        abort(500, description="Expected int, but got {}: {}.".format(type(pool), pool))
    return render_template('pools/detail.html', pool=db_pool)


@bp_pools.route('/add', methods=['GET', 'POST'])
def add():
    form = PoolAddForm(request.form)
    form.drives.choices = manager.get_empty_drives()
    if request.method == 'POST' and form.validate():
        try:
            manager.create_btrfs_pool(form)
        except subprocess.CalledProcessError as e:
            abort(500, description="While creating a pool, the following exception occured: {}".format(e))
        except subprocess.TimeoutExpired as e:
            abort(500, description="Pool creation took too long: {}".format(e))
        scheduler.get_job("refresh_disks").modify(next_run_time=datetime.datetime.now())
        sleep(1)
        return redirect(url_for('.index'))
    return render_template('pools/pool_add.html', form=form)
