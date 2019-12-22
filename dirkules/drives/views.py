import dirkules.drives.manager as manager
from dirkules.models import Drive
from flask import Blueprint, request, url_for, redirect, render_template, abort

bp_drives = Blueprint('drives', __name__, template_folder='templates')


@bp_drives.route('/', methods=['GET'])
def index():
    delete = request.args.get('delete')
    if delete is not None:
        try:
            manager.delete_drive_by_id(int(delete))
        except ValueError:
            abort(500, description="Expected int, but got {}: {}.".format(type(delete), delete))
        return redirect(url_for('.index'))
    return render_template('drives/index.html', drives=Drive.query.all())


@bp_drives.route('/<drive_id>', methods=['GET'])
def detail(drive_id):
    try:
        drive = manager.get_drive_by_id(int(drive_id))
    except ValueError:
        abort(500, description="Expected int, but got {}: {}.".format(type(drive_id), drive_id))
    return render_template('drives/detail.html', parts=drive.partitions)
