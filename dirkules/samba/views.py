from dirkules import db

from dirkules.config import staticDir
from flask import render_template, url_for, request, redirect
from dirkules.samba import bp_samba
from dirkules.samba.manager import set_samba_global, generate_smb
from dirkules.samba.models import SambaShare
from dirkules.samba.validation import SambaConfigForm, SambaAddForm


@bp_samba.route('/', methods=['GET'])
def index():
    shares = SambaShare.query.order_by(db.asc(db.collate(SambaShare.name, 'NOCASE'))).all()
    return render_template('samba/index.html', shares=shares)


@bp_samba.route('/config', methods=['GET', 'POST'])
def config():
    form = SambaConfigForm(request.form)
    if request.method == 'POST' and form.validate():
        set_samba_global(form.workgroup.data, form.server_string.data)
        return redirect(url_for('.index'))
    file = open(staticDir + "/conf/samba_global.conf", "r")
    conf = list()
    while True:
        line = file.readline()
        if line != '':
            conf.append(line.rstrip())
        else:
            break
    return render_template('samba/config.html', form=form, conf=conf)


@bp_samba.route('/add', methods=['GET', 'POST'])
def add():
    form = SambaAddForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('.index'))
    return render_template('samba/add.html', form=form)


@bp_samba.route('/generate')
def generate():
    generate_smb()
    return redirect(url_for('.index'))
