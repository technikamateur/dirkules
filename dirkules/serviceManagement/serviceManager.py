import subprocess

def service_state():
    service = {}
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
    return service
