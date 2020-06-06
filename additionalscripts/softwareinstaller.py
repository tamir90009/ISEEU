import subprocess

class softwareinstaller(object):

    def install(self, software_path):
        raise NotImplemented

    def apt_install(self, package_name):
        #todo: check errors
        subprocess.call(["sudo", "apt-get", "--assume-yes", "install", package_name])

    def pip_install(self, module_name):
        subprocess.call(["sudo", "pip3", "install", module_name])