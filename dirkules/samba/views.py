from dirkules import db

from dirkules.config import staticDir
from flask import render_template, url_for, request, redirect, flash
from dirkules.samba import bp_samba
from dirkules.samba import manager as smb_man
from dirkules.samba.models import SambaShare
from dirkules.samba.validation import SambaConfigForm, SambaAddForm


@bp_samba.route('/', methods=['GET'])
def index():
    e_share = request.args.get('enable')
    d_share = request.args.get('disable')
    shares = SambaShare.query.order_by(db.asc(db.collate(SambaShare.name, 'NOCASE'))).all()
    if not (e_share is not None and d_share is not None):
        if e_share is not None:
            try:
                e_share = int(e_share)
                share = smb_man.get_share_by_id(e_share)
                smb_man.enable_share(share)
            except ValueError:
                flash("ValueError: enable")
            except LookupError:
                flash("LookupError: id not valid")
            return redirect(url_for('.index'))
        elif d_share is not None:
            try:
                d_share = int(d_share)
                share = smb_man.get_share_by_id(d_share)
                smb_man.disable_share(share)
            except ValueError:
                flash("ValueError: disable")
            except LookupError:
                flash("LookupError: id not valid")
            return redirect(url_for('.index'))
    else:
        flash("Value Error: enable and disable set")
    return render_template('samba/index.html', shares=shares)


@bp_samba.route('/config', methods=['GET', 'POST'])
def config():
    form = SambaConfigForm(request.form)
    if request.method == 'POST' and form.validate():
        smb_man.set_samba_global(form.workgroup.data, form.server_string.data)
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
    form.path.choices = smb_man.get_pools()
    if request.method == 'POST' and form.validate():
        smb_man.create_share(form.name.data, form.path.data, form.user.data, form.dir_mask.data, form.create_mask.data,
                             form.writeable.data, form.btrfs.data, form.recycling.data)
        return redirect(url_for('.index'))
    return render_template('samba/add.html', form=form)


@bp_samba.route('/generate')
def generate():
    smb_man.generate_smb()
    return redirect(url_for('.index'))


@bp_samba.route('/remove', methods=['GET', 'POST'])
def remove():
    share_id = request.args.get('share')
    if share_id is None:
        flash("Can't remove drive without id.")
        return redirect(url_for('.index'))
    else:
        return render_template('samba/remove.html')
