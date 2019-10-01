from dirkules import db

from dirkules.samba.models import SambaGlobal


def set_samba_global(workgroup, name):
    SambaGlobal.query.delete()
    workgroup = SambaGlobal("workgroup", workgroup)
    name = SambaGlobal("server string", "%h {}".format(name))
    db.session.add(workgroup)
    db.session.add(name)
    db.session.commit()
