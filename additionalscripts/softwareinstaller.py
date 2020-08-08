import subprocess
from time import sleep
import os

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
        try:
            subprocess.call(["pip3", "install", module_name])
            subprocess.call(["pip", "install", module_name])
        except Exception as e:
            print("Error with pip install: " + str(e))
    @staticmethod
    def dpkg_install(package_folder_path):
        try:
            subprocess.call(["dpkg", "-i", os.path.join(package_folder_path, '*')])
        except Exception as e:
            print("Error with dpkg install: " + str(e))

    @staticmethod
    def pmanual_install(pmodule_path):
        try:
            subprocess.call(["python3", os.path.join(pmodule_path, 'setup.py'), 'install'])
        except Exception as e:
            print("Error with python module: " + str(e))
