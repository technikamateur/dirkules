import os
import subprocess


class DriveManager:
    """
    There should be only one DriveManager in your app.
    """
    smartctl_available = False

    def __init__(self):
        self.sorted_drive_dict = None
        self._check_required_tools()

    def _check_required_tools(self):
        """
        Checks for required tools:
        - smartmontools
        """
        if os.path.isfile('/usr/sbin/smartctl'):
            self.smartctl_available = True

    @staticmethod
    def _is_healthy(device):
        """
        This function returns for given device the answer of the question: Is this drive healthy?
        It will use the output of the linux tool "smartctl".
        :param device: The device you actually want to check
        :type device: str (e.g. "/dev/sda")
        :return: healthy information
        :rtype: bool
        """
        smartctl = subprocess.run(["sudo", "smartctl", "-H", device], shell=False, timeout=20, check=True,
                                  universal_newlines=True, stdout=subprocess.PIPE)
        if any('PASSED' in line for line in smartctl.stdout.splitlines()):
            return True
        else:
            return False

    def _update_drives(self):
        drive_dict = list()
        keys = [
            'name', 'model', 'serial', 'size', 'rota', 'rm', 'hotplug', 'state',
            'smart'
        ]
        lsblk = subprocess.run(["sudo", "lsblk", "-I", "8", "-d", "-b", "-o", "NAME,MODEL,SERIAL,SIZE,ROTA,RM,HOTPLUG"],
                               shell=False, timeout=45, check=True, universal_newlines=True, stdout=subprocess.PIPE)
        drives = lsblk.stdout.splitlines()
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
            values.append(self._is_healthy("/dev/" + values[0]))
            drive_dict.append(dict(zip(keys, values)))
        self.sorted_drive_dict = sorted(drive_dict, key=lambda drive: drive['name'])

    def get_all_drives(self):
        """
        Returns a standardized list of dictionaries which contains all information about all drives in the system.
        :rtype: list
        """
        self._update_drives()
        return self.sorted_drive_dict
