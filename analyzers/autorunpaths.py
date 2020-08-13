from analyzers.analyzer import Analyzer
import os
import socket
import json
from additionalscripts.datasend import datasend

DEST = '/tmp'

WHITELIST = ['/etc/init.d/thermald', '/etc/init.d/irqbalance', '/etc/init.d/clamav-freshclam', '/etc/init.d/alsa-utils' \
    , '/etc/init.d/lightdm', '/etc/init.d/mountnfs-bootclean.sh', '/etc/init.d/reboot', \
             '/etc/init.d/keyboard-setup', '/etc/init.d/rsync', '/etc/init.d/kerneloops', \
             '/etc/init.d/checkroot-bootclean.sh', '/etc/init.d/apache2', '/etc/init.d/avahi-daemon', \
             '/etc/init.d/acpid', '/etc/init.d/vmware', '/etc/init.d/vmware-USBArbitrator', '/etc/init.d/.depend.stop', \
             '/etc/init.d/rc', '/etc/init.d/gdm3', '/etc/init.d/hwclock.sh', '/etc/init.d/grub-common', \
             '/etc/init.d/network-manager', '/etc/init.d/x11-common', '/etc/init.d/umountfs',
             '/etc/init.d/umountnfs.sh', \
             '/etc/init.d/unattended-upgrades', '/etc/init.d/hostname.sh', '/etc/init.d/resolvconf', '/etc/init.d/cron', \
             '/etc/init.d/.depend.start', '/etc/init.d/cgproxy', '/etc/init.d/mountall.sh', '/etc/init.d/dbus', \
             '/etc/init.d/mountdevsubfs.sh', '/etc/init.d/udev', '/etc/init.d/bluetooth',
             '/etc/init.d/apache-htcacheclean', \
             '/etc/init.d/bootmisc.sh', '/etc/init.d/networking', '/etc/init.d/console-setup', '/etc/init.d/README', \
             '/etc/init.d/checkfs.sh', '/etc/init.d/cgmanager', '/etc/init.d/dns-clean', '/etc/init.d/rcS', \
             '/etc/init.d/mountkernfs.sh', '/etc/init.d/rsyslog', '/etc/init.d/anacron',
             '/etc/init.d/vmware-workstation-server', \
             '/etc/init.d/virtualbox', '/etc/init.d/checkroot.sh', '/etc/init.d/killprocs', '/etc/init.d/mountnfs.sh', \
             '/etc/init.d/mountall-bootclean.sh', '/etc/init.d/brltty', '/etc/init.d/plymouth', '/etc/init.d/skeleton', \
             '/etc/init.d/rc.local', '/etc/init.d/saned', '/etc/init.d/procps', '/etc/init.d/whoopsie', \
             '/etc/init.d/urandom', '/etc/init.d/ondemand', '/etc/init.d/uuidd', '/etc/init.d/ufw',
             '/etc/init.d/apport', \
             '/etc/init.d/sendsigs', '/etc/init.d/halt', '/etc/init.d/apparmor', '/etc/init.d/pppd-dns',
             '/etc/init.d/cups-browsed', \
             '/etc/init.d/speech-dispatcher', '/etc/init.d/single', '/etc/init.d/cups', '/etc/init.d/plymouth-log', \
             '/etc/init.d/umountroot', '/etc/init.d/.depend.boot', '/etc/init.d/kmod', '/etc/init.d/agent-atomation']


class AutoRunPathsAnalyzer(Analyzer):
    '''
    this func will get the autorunpaths from the parser in a list and send the data to file attribute check and write
    to json (which will be send to ES)
    '''

    @staticmethod
    def analyze(paths, dest_path=DEST):
        try:
            relevent_paths = [x for x in paths if x not in WHITELIST]
            # writes to ES
            AutoRunPathsAnalyzer.write_to_files(relevent_paths, dest_path,
                                                "{}_autorunpaths.json".format(socket.gethostname()))
            datasend(os.path.join(dest_path, "{}_autorunpaths.json".format(socket.gethostname())), "autorunpaths")

            # writes for meta data check
            dst_path_metadata = "{}/MetaData".format("/".join(dest_path.split('/')[:-1]))
            os.makedirs(dst_path_metadata, exist_ok=True)
            AutoRunPathsAnalyzer.write_to_files(relevent_paths, dst_path_metadata, "AutoRunPaths.txt")


        except Exception as e:
            raise("problem in autorunpaths analyzer - analyze :", str(e))

    @staticmethod
    def write_to_files(paths, dest_path, name):
        try:
            with open(os.path.join(dest_path, name), "w") as fp:
                to_json = {}
                i = 0
                for path in paths:
                    to_json[i] = path
                    fp.write(json.dumps(to_json[i]) + '\n')
                    i += 1

        except Exception as e:
            raise("problem in autorunpaths analyzer- write to files :{} , dest path was :{}".format(str(e), dest_path))
