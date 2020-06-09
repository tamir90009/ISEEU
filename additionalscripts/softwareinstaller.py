import subprocess

class softwareinstaller(object):
    @staticmethod
    def install(self, software_path):
        raise NotImplemented

    @staticmethod
    def apt_install(self, package_name):
        #todo: check errors
        subprocess.call(["apt-get", "--assume-yes", "install", package_name])

    @staticmethod
    def pip_install(self, module_name):
        subprocess.call(["pip3", "install", module_name])