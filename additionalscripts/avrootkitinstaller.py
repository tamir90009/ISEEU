import time
import subprocess as sub
import os
from Softwareinstaller import softwareinstaller


def install():
    try:
        try:
            softwareinstaller.get_apt('clamav')
            softwareinstaller.get_apt('clamav-daemon')
            softwareinstaller.get_apt('rkhunter')
            softwareinstaller.get_apt('tkrootkit')
        except Exception as e:
            raise ("error with get_apt " + e)
        if not os.path.exists('maldetect-current.tar.gz'):
            try:
                sub.Popen('wget "http://www.rfxn.com/downloads/maldetect-current.tar.gz"',stdin=sub.PIPE,shell=True)
            except Exception as e:
                raise Exception("Problem getting maldet " + e)
        time.sleep(5)
        try:
            sub.Popen('tar zxvf maldetect-current.tar.gz', stdin=sub.PIPE, shell=True)
        except Exception as e:
            raise Exception("problem while extracting mal det " + e)
        time.sleep(5)
        p = sub.Popen('ls', stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE,
                      shell=True)
        out, err = p.communicate()
        for file in out.decode('utf-8').splitlines():
            if file.startswith('maldetect-') and 'tar.gz' not in file:
                sub.Popen('mv {0}/* .'.format(file), stdin=sub.PIPE,
                          shell=True)
                time.sleep(5)
                c = sub.Popen('./{0}/install.sh'.format(file), stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE
                              , shell=True)
                out,err = c.communicate()

    except Exception as e:
        raise ("error while trying to install maldetect " + e)


install()