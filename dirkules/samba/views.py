from dirkules import db

from dirkules.config import staticDir
from flask import render_template, url_for, request, redirect, flash
from dirkules.samba import bp_samba
from dirkules.samba import manager as smb_man
from dirkules.samba.models import SambaShare, SambaGlobal
from dirkules.samba.validation import SambaConfigForm, SambaAddForm, SambaRemovalForm


@bp_samba.route('/', methods=['GET'])
def index():
    e_share = request.args.get('enable')
    d_share = request.args.get('disable')
    shares = SambaShare.query.order_by(db.asc(db.collate(SambaShare.name, 'NOCASE'))).all()
    if not (e_share is not None and d_share is not None):
        if e_share is not None:
            try:
                e_share = int(e_share)
                share = SambaShare.query.get_or_404(e_share)
                smb_man.enable_share(share)
            except ValueError:
                flash("ValueError: enable", category="error")
            except LookupError:
                flash("LookupError: id not valid", category="error")
            return redirect(url_for('.index'))
        elif d_share is not None:
            try:
                d_share = int(d_share)
                share = SambaShare.query.get_or_404(d_share)
                smb_man.disable_share(share)
            except ValueError:
                flash("ValueError: disable", category="error")
            except LookupError:
                flash("LookupError: id not valid", category="error")
            return redirect(url_for('.index'))
    else:
        flash("Value Error: enable and disable set", category="error")
    return render_template('samba/index.html', shares=shares)


@bp_samba.route('/config', methods=['GET', 'POST'])
def config():
    form = SambaConfigForm(request.form)
    if SambaGlobal.query.first() is not None:
        form.workgroup.data = SambaGlobal.query.get(1)
        form.server_string.data = SambaGlobal.query.get(2)
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
    if SambaGlobal.query.first() is None:
        flash("Samba wurde nicht konfiguriert. Es wird der default fallback verwendet", category="warn")
    flash("Konfiguration erfolgreich generiert", category="positive")
    return redirect(url_for('.index'))


@bp_samba.route('/remove', methods=['GET', 'POST'])
def remove():
    share_id = request.args.get('share')
    show_modal = False
    if share_id is None:
        flash("Keine id angegeben. Möglicherweise ist der Verweis veraltet", category="error")
        return redirect(url_for('.index'))
    else:
        try:
            form = SambaRemovalForm(request.form)
            share_id = int(share_id)
            share = SambaShare.query.get_or_404(share_id)
            if request.method == 'POST':
                if form.validate():
                    smb_man.remove_share(share, remove_data=bool(form.remove_data.data))
                    return redirect(url_for('.index'))
                else:
                    show_modal = True
            return render_template('samba/remove.html', name=share.name, form=form, show_modal=show_modal)
        except ValueError:
            flash("ValueError: id is not an int", category="error")
        return redirect(url_for('.index'))
