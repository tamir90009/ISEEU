import time
import subprocess as sub
import os
from additionalscripts.softwareinstaller import softwareinstaller


def install():
    # software_installer = softwareinstaller()

    try:
        for apt in ['net-tools', 'clamav', 'clamav-daemon', 'rkhunter', 'chkrootkit', 'python3-pip','python-pip']:
            if apt == 'rkhunter':
                sub.Popen('apt-get -y --no-install-recommends install rkhunter', stdin=sub.PIPE, stdout=sub.PIPE,
                          stderr=sub.PIPE, shell=True)
            elif apt == 'clamav-daemon':
                time.sleep(5)
                softwareinstaller.apt_install(apt)
            else:
                softwareinstaller.apt_install(apt)
    except Exception as e:
        print("error with get_apt " + str(e))
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
                print(out)
    except Exception as e:
        raise Exception("error while trying to install maldetect " + str(e))
    try:
        time.sleep(5)
        for pip in ['pretty-cron','paramiko']:
            softwareinstaller.pip_install(pip)
    except Exception as e:
        raise Exception("error with pip install pretty_cron " + str(e))


