import importlib
import time
import subprocess as sub
import os
from additionalscripts.softwareinstaller import softwareinstaller
import site



def free_dpkg_lock():
    try:
        lsof_out = sub.check_output(['lsof', '/var/lib/dpkg/lock'])
        pid = lsof_out.decode('ascii').split('\n')[-2].split()[1]
        if pid.isdigit():
            sub.check_output(['kill', pid])
            time.sleep(2)
            sub.check_output(['kill', '-9',pid])
        else:
            raise Exception('free_dpkg_lock parsing is not good in case - \n %s' % lsof_out.decode('ascii'))
    except Exception as e:
        print(e)


def wait_for_module(module_name):
    installed = False
    while not installed:
        try:
            importlib.import_module(module_name)
        except:
            print('%s - not yet' % module_name)
            print(importlib.reload(site))
            time.sleep(10)


def install_offline(profile):
    free_dpkg_lock()
    archive_path = os.path.join('additionalscripts/archives', profile)
    softwareinstaller.dpkg_install(archive_path)
    softwareinstaller.pmanual_install('additionalscripts/python_packages/setuptools-49.3.1')
    softwareinstaller.pmanual_install('additionalscripts/python_packages/pycparser-2.20')
    softwareinstaller.pmanual_install('additionalscripts/python_packages/cffi-1.14.1')
    softwareinstaller.pmanual_install('additionalscripts/python_packages/bcrypt-3.1.7')
    softwareinstaller.pmanual_install('additionalscripts/python_packages/cryptography-3.0')
    softwareinstaller.pmanual_install('additionalscripts/python_packages/paramiko-2.7.1')
    # wait_for_module('paramiko')
    softwareinstaller.pmanual_install('additionalscripts/python_packages/pretty-cron-1.2.0')
    # wait_for_module('pretty-cron')


def install():
    # software_installer = softwareinstaller()
    try:
        # for apt in ['net-tools', 'clamav', 'clamav-daemon', 'rkhunter', 'chkrootkit', 'python3-pip', 'qemu-kvm', 'qemu',
        #             'virt-manager', 'virt-viewer', 'libvirt-bin']:
        for apt in ['net-tools', 'clamav', 'clamav-daemon', 'rkhunter', 'chkrootkit', 'python3-pip']:
            if apt == 'rkhunter':
                sub.Popen('apt-get -y --no-install-recommends install rkhunter', stdin=sub.PIPE, stdout=sub.PIPE,
                          stderr=sub.PIPE, shell=True)
            else:
                softwareinstaller.apt_install(apt)
    except Exception as e:
        raise Exception("error with get_apt " + str(e))
    if not os.path.exists('/tmp/maldetect-current.tar.gz'):
        try:
            sub.Popen('wget -O "/tmp/maldetect-current.tar.gz" "http://www.rfxn.com/downloads/maldetect-current.tar.gz"',stdin=sub.PIPE,shell=True)
        except Exception as e:
            raise Exception("Problem getting maldet " + str(e))
    time.sleep(5)
    try:
        sub.Popen('tar zxvf /tmp/maldetect-current.tar.gz -C /tmp', stdin=sub.PIPE, shell=True)
    except Exception as e:
        raise Exception("problem while extracting mal det " + str(e))
    time.sleep(5)
    p = sub.Popen('ls /tmp', stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE,
                  shell=True)
    out, err = p.communicate()
    if err:
        raise Exception("problem while running ls" + str(err))
    try:
        for file in out.decode('utf-8').splitlines():
            if 'maldetect-' in file and 'tar.gz' not in file:
                c = sub.Popen('/tmp/{0}/install.sh'.format(file), cwd=r'/tmp/{0}/'.format(file), stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE
                              , shell=True)
                out,err = c.communicate()
                if out:

                    print(out)

    except Exception as e:
        raise Exception("error while trying to install maldetect " + str(e))
    try:
        for pip in ['pretty-cron', 'paramiko']:
            softwareinstaller.pip_install(pip)
    except Exception as e:
        raise Exception("error with pip install pretty_cron " + str(e))


