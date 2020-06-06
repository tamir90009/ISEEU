from analyzers.analyzer import Analyzer
import json
import os
import socket
from additionalscripts.datasend import datasend

OS_WHITELIST = ["root", "daemon", "bin", "sys", "sync", "games", "man", "lp", "mail", "news", "uucp", "proxy",
                "www-data", "backup", \
                "list", "irc", "gnats", "nobody", "syslog", "messagebus", "usbmux", "dnsmasq", "avahi-autoipd",
                "kernoops", \
                "rtkit", "saned", "whoopsie", "speech-dispatcher", "avahi", "lightdm", "colord", "hplip", "pulse",
                "clamav", \
                "gdm", "systemd-timesync", "systemd-network", "systemd-resolve", "systemd-bus-proxy", "uuidd", "apt", \
                "kvm", "input", "tts","tty","render", "crontab", "netdev", "ssl-cert", "ssh", "bluetooth", "scanner",
                "lpadmin","floppy" ,\
                "adm", "kmem", "floopy", "dialout", "cdrom", "fax", "voice", "tape", "sudo", "audio", "dip",\
                "nopasswdlogin","src","shadow", "operator", "utmp" , "adm", "disk","video","sasl","nogroup","fuse",\
                "mlocate","utempter","pulse-access","users", "plugdev", "staff", "geoclue", "debian-gdm","sambashare",\
                "wireshark","vboxusers","systemd-journal"]

DEST = '/tmp'


class SystemInfoAnalyzer(Analyzer):
    '''
    this func reads the system information and mark the user groups and names that are whitelisted by being default
     to the operation system
    input; gets system data - system information and the destination path
    '''

    @staticmethod
    def analyze(system_data, dest_path=DEST):

        try:
            system_data = SystemInfoAnalyzer.check_if_os_default(system_data, 'users', 'user_name')
            system_data = SystemInfoAnalyzer.check_if_os_default(system_data, 'groups', 'group_name')
            with open(os.path.join(dest_path, "{}_systeminfo.json".format(socket.gethostname())), "w") as fp:
                system_info = dict((k, system_data[k]) for k in ('architecture', 'host_name', 'kernel_version', 'distribution'))
                fp.write(json.dumps(system_info)+'\n')
            datasend(os.path.join(dest_path, "{}_systeminfo.json".format(socket.gethostname())), 'systeminfo')
            with open(os.path.join(dest_path, "{}_groups.json".format(socket.gethostname())), "w") as fp:
                for group in system_data['groups']:
                    fp.write(json.dumps(group) + '\n')
            datasend(os.path.join(dest_path, "{}_groups.json".format(socket.gethostname())), 'groups')
            with open(os.path.join(dest_path, "{}_users.json".format(socket.gethostname())), "w") as fp:
                for user in system_data['users']:
                    fp.write(json.dumps(user) + '\n')
            datasend(os.path.join(dest_path, "{}_users.json".format(socket.gethostname())), 'users')

        except Exception as e:
            raise Exception("problem in reading analytic  info - analyzer :{}".format(str(e)))

    '''
    this function will check if the specific object (users or  groups)
    are os default 
    as in input it det a dic that contains list of dictionary from system info collector 
    and returns the nue updated system_data with whitlested values
    field is the field that we compare by (between system object and information about the object -  like "user_name") 
    '''

    @staticmethod
    def check_if_os_default(system_data, object , field):
        try:
            for obj in system_data[object]:
                # print(user['user_name'])
                object_id = next((i for i, object in enumerate(system_data[object]) if
                                object[field] == obj[field]), None)
                if obj[field] in OS_WHITELIST:
                    system_data[object][object_id]['os_default'] = 'True'
                else:
                    system_data[object][object_id]['os_default'] = 'False'
            return system_data
        except Exception as e:
            raise Exception("problem in system info - check if os default for {} : {}".format(object, e))
