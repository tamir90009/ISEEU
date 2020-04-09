import random
import subprocess
import re
from threading import Lock


class VBoxController(object):
    mounted_devices = {}
    free_nbd = ["/dev/nbd0", "/dev/nbd1", "/dev/nbd2", "/dev/nbd3", "/dev/nbd4", "/dev/nbd5", "/dev/nbd6", "/dev/nbd7",
                "/dev/nbd8", "/dev/nbd9", "/dev/nbd10", "/dev/nbd11", "/dev/nbd12", "/dev/nbd13", "/dev/nbd14",
                "/dev/nbd15"]
    lock = Lock()
    @staticmethod
    def start(vmname, start_type="headless"):
        # start_type options are headless(default) or gui
        try:
            subprocess.check_output(["vboxmanage", "startvm", vmname, "--type", start_type])
        except Exception as e:
            raise Exception("VBoxController failed starting the machine %s %s" % (vmname, str(e)))

    @staticmethod
    def stop(vmname):
        try:
            subprocess.check_output(["vboxmanage", "controlvm", vmname, "poweroff"])
        except Exception as e:
            raise Exception("VBoxController failed stopping the machine %s %s" % (vmname, str(e)))

    @staticmethod
    def import_machine(vmname, vm_path):
        try:
            subprocess.check_output(["vboxmanage", "import", vm_path, "--vsys", "0", "--vmname", vmname])
        except Exception as e:
            raise Exception("Fail to import the vm %s" % (str(e)))

    @staticmethod
    def convert_raw_to_vbox(raw_path, output_file, hd_format="VDI"):
        # hd_format options are VDI(defualt), VMDK or VHD
        try:
            subprocess.check_output(["vboxmanage", "convertfromraw", raw_path, output_file, "--format", hd_format])
        except Exception as e:
            raise Exception("Fail to convert raw file %s" % (str(e)))

    @staticmethod
    def get_vm_home_path(vmname):
        try:
            output = subprocess.check_output(["vboxmanage", "showvminfo", vmname])
            re_m = re.findall("Config file:\s*(.*)\r\n", output)
            if re_m:
                return "/".join(re_m[0].split("/")[:-1])
            else:
                raise Exception("regex not good")
        except Exception as e:
            raise Exception("Fail to get vm home path %s" % (str(e)))

    def mount_files_from_machine(self, vmname, mount_path=None):
        # mount methodology came from https://www.cyrill-gremaud.ch/mount-virtualbox-image-drive-on-ubuntu-vdi/
        if not mount_path:
            mount_path = "/mnt/" + vmname
        self.lock.acquire()
        if mount_path in self.mounted_devices:
            raise Exception("something already mounted in %s" % mount_path)
        if not self.free_nbd:
            raise Exception("can't mount new images, please umount some images first %s" % mount_path)
        current_nbd = random.choice(self.free_nbd)
        self.free_nbd.remove(current_nbd)
        self.lock.release()
        try:
            vdi_path = self.get_vm_home_path(vmname)
        except Exception as e:
            raise e
        if not self.mounted_devices:
            try:
                subprocess.check_output(["modprobe", "nbd"])
            except Exception as e:
                raise Exception("Fail to start modprobe %s" % (str(e)))
        try:
            subprocess.check_output(["qemu-nbd", "-c", current_nbd, vdi_path])
        except Exception as e:
            raise Exception("Fail with qemu-nbd %s" % (str(e)))
        try:
            output = subprocess.check_output(["fdisk", "-l", current_nbd])
        except Exception as e:
            raise Exception("Fail with fdisk %s" % (str(e)))
        partition_to_mount = re.findall("\n(.*) \*  ", output)
        if not partition_to_mount:
            raise Exception("mount files from machine fdisk regex not good")
        try:
            subprocess.check_output(["mount", partition_to_mount[0], mount_path])
        except Exception as e:
            raise Exception("fail to mount %s to %s %s" % (partition_to_mount[0], mount_path, str(e)))
        self.mounted_devices[mount_path] = current_nbd

    def umount_files_from_machine(self, vmname, mount_path=None):
        if not mount_path:
            mount_path = "/mnt/" + vmname
        if mount_path not in self.mounted_devices:
            raise Exception("%s not mounted" % mount_path)
        try:
            subprocess.check_output(["umount", mount_path])
        except Exception as e:
            raise Exception("Fail to umount %s %s" % (mount_path, str(e)))
        try:
            subprocess.check_output(["qemu-nbd", "-d", self.mounted_devices[mount_path]])
        except Exception as e:
            raise Exception("Fail to umount qemu-nbd %s %s" % (mount_path, str(e)))
        self.lock.acquire()
        self.free_nbd.append(self.mounted_devices[mount_path])
        del self.mounted_devices[mount_path]
        self.lock.release()
        if not self.mounted_devices:
            try:
                subprocess.check_output(["modprobe", "-r", "nbd"])
            except Exception as e:
                raise Exception("Fail to modprobe -r nbd %s" % (str(e)))
