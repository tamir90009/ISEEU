import subprocess
from time import sleep


class softwareinstaller(object):
    @staticmethod
    def install(software_path):
        raise NotImplemented

    @staticmethod
    def apt_install(package_name):
        #todo: check errors
        p = subprocess.Popen(["apt", "--assume-yes", "install", package_name])
        p.wait()
        sleep(3)

    @staticmethod
    def pip_install(module_name):
        subprocess.call(["pip3", "install", module_name])