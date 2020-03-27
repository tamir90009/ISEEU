import subprocess

class softwareinstaller(object):

    def install(self, software_path):
        raise NotImplemented

    def git_install(self, package_name):
        #todo: check errors
        subprocess.call(["sudo", "apt-get","--assume-yes","install", package_name])