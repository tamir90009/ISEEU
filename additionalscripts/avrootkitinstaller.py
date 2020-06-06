import time
import subprocess as sub
import os
from additionalscripts.softwareinstaller import softwareinstaller


def install():
    try:
        software_installer = softwareinstaller()
        try:
            for apt in ['net-tools','clamav clamav-daemon','rkhunter -Y','chkrootkit']:
                software_installer.apt_install(apt)
        except Exception as e:
            raise Exception("error with get_apt " + str(e))
        if not os.path.exists('maldetect-current.tar.gz'):
            try:
                sub.Popen('wget "http://www.rfxn.com/downloads/maldetect-current.tar.gz"',stdin=sub.PIPE,shell=True)
            except Exception as e:
                raise Exception("Problem getting maldet " + str(e))
        time.sleep(5)
        try:
            sub.Popen('tar zxvf maldetect-current.tar.gz', stdin=sub.PIPE, shell=True)
        except Exception as e:
            raise Exception("problem while extracting mal det " + str(e))
        time.sleep(5)
        p = sub.Popen('ls', stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE,
                      shell=True)
        out, err = p.communicate()
        if err:
            raise Exception("problem while running ls" + str(err))
        for file in out.decode('utf-8').splitlines():
            if file.startswith('maldetect-') and 'tar.gz' not in file:
                sub.Popen('mv {0}/* /tmp'.format(file), stdin=sub.PIPE,
                          shell=True)
                time.sleep(5)
                c = sub.Popen('/tmp/install.sh'.format(file), stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE
                              , shell=True)
                out,err = c.communicate()
                if err:
                    raise Exception("error While instaling maldet" + str(err))

    except Exception as e:
        raise Exception("error while trying to install maldetect " + str(e))


install()