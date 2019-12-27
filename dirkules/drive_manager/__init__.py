import os
import subprocess


class DriveManager:
    """
    There should be only one DriveManager in your app!
    """
    smartctl_available = False
    drive_keys = ['name', 'model', 'serial', 'size', 'rota', 'rm', 'hotplug', 'state', 'smart']
    part_keys = ['size', 'name', 'label', 'fs', 'uuid', 'mount']

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
            for i in range(len(self.drive_keys) - 2):
                if new_line[i] == "0":
                    values.append(False)
                elif new_line[i] == "1":
                    values.append(True)
                else:
                    values.append(new_line[i])
            values.append("running")
            values.append(self._is_healthy("/dev/" + values[0]))
            drive_dict.append(dict(zip(self.drive_keys, values)))
        self.sorted_drive_dict = sorted(drive_dict, key=lambda drive: drive['name'])

    def get_all_drives(self, cached=False):
        """
        Returns a standardized list of dictionaries which contains all information about all drives in the system.
        If cached is true it will return a cached version of the drives.
        :type cached: bool
        :rtype: list
        """
        if not cached or self.sorted_drive_dict is None:
            self._update_drives()
        return self.sorted_drive_dict

    def part_for_disk(self, device):
        """
        This function is used to return a standardized list of dictionaries which contains all information about
        this partition
        :param device: A device e.g. "/dev/sda"
        :type device: str
        :return: list of dictionaries (every dictionary represents a partition)
        :rtype: list
        """
        # lsblk /dev/sdd -l -b -o NAME,LABEL,FSTYPE,SIZE,UUID,MOUNTPOINT
        part_dict = list()
        lsblk = subprocess.run(["sudo", "lsblk", device, "-l", "-b", "-o", "SIZE,NAME,LABEL,FSTYPE,UUID,MOUNTPOINT"],
                               shell=False, timeout=45, check=True, universal_newlines=True, stdout=subprocess.PIPE)
        parts = lsblk.stdout.splitlines()
        del parts[1]
        element_length = list()
        counter = 0
        pre_value = " "
        for char in parts[0]:
            if char != " " and pre_value == " ":
                if len(element_length) == 0:
                    element_length.append(0)
                else:
                    element_length.append(counter)
            counter += 1
            pre_value = char
        element_length.append(len(parts[0]))
        del parts[0]
        for part in parts:
            values = list()
            for start, next_start in zip(element_length, element_length[1:]):
                if next_start == element_length[-1:][0]:
                    values.append(part[start:len(part)].strip())
                else:
                    values.append(part[start:(next_start - 1)].strip())
            part_dict.append(dict(zip(self.part_keys, values)))
        return part_dict
