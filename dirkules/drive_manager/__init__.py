import subprocess


def _is_healthy(device):
    """
    This function returns for given device e.g. "/dev/sda" the answer of the question: Is this drive healthy?
    It will use the output of the linux tool "smartctl".
    :param device: The device you actually wanna check
    :type device: str
    :return: healthy information
    :rtype: bool
    """
    smartctl = subprocess.run(["sudo", "smartctl", "-H", device], shell=False, timeout=20, check=True,
                              universal_newlines=True, stdout=subprocess.PIPE)
    if any('PASSED' in line for line in smartctl.stdout.splitlines()):
        return True
    else:
        return False


class DriveManager:
    def __init__(self, db_drives):
        self.db_drives = db_drives
        self.sorted_drive_dict = None

    def get_all_drives(self):
        drives = list()
        drive_dict = list()
        keys = [
            'name', 'model', 'serial', 'size', 'rota', 'rm', 'hotplug', 'state',
            'smart'
        ]

        lsblk = subprocess.Popen(
            ["sudo lsblk -I 8 -d -b -o NAME,MODEL,SERIAL,SIZE,ROTA,RM,HOTPLUG"],
            stdout=subprocess.PIPE,
            shell=True,
            universal_newlines=True)
        while True:
            line = lsblk.stdout.readline()
            if line != '':
                drives.append(line.rstrip())
            else:
                break
        lsblk.stdout.close()
        del drives[0]
        for line in drives:
            new_line = ' '.join(line.split())
            new_line = new_line.split(" ")
            while len(new_line) > 7:
                new_line[1] = new_line[1] + " " + new_line[2]
                del new_line[2]
            values = []
            for i in range(len(keys) - 2):
                if new_line[i] == "0":
                    values.append(False)
                elif new_line[i] == "1":
                    values.append(True)
                else:
                    values.append(new_line[i])
            values.append("running")
            values.append(_is_healthy("/dev/" + values[0]))
            drive_dict.append(dict(zip(keys, values)))
        self.sorted_drive_dict = sorted(drive_dict, key=lambda drive: drive['name'])
        return self.sorted_drive_dict
