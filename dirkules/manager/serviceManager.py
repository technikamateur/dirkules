import subprocess
import dirkules.manager.cleaning as cleaningMan


def service_state():
    service = dict()
    result = subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
    out, err = result.communicate()
    if ('nzbget' in str(out)):
        service.update({"nzbget": True})
    else:
        service.update({"nzbget": False})
    if ('smbd' in str(out)):
        service.update({"samba": True})
    else:
        service.update({"samba": False})
    # now dirkules internal services
    if cleaningMan.running():
        service.update({"Dirkules cleaning service": True})
    else:
        service.update({"Dirkules cleaning service": False})
    return service
