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
            current_cwd = os.getcwd()
            os.chdir(package_folder_path)
            p = subprocess.Popen(["dpkg -i *"], shell=True)
            p.wait()
            sleep(3)
            os.chdir(current_cwd)
        except Exception as e:
            print("Error with dpkg install: " + str(e))

    @staticmethod
    def pmanual_install(pmodule_path):
        import pip
        try:
            # current_cwd = os.getcwd()
            # os.chdir(pmodule_path)
            # p = subprocess.Popen(["python3", 'setup.py', 'install'])
            # p.wait()
            # sleep(3)
            # os.chdir(current_cwd)
            pip.main(['install', pmodule_path])
            sleep(3)
        except Exception as e:
            print("Error with python module: " + str(e))
