from analyzers.analyzer import Analyzer
from os import listdir
from os.path import isfile, join
import json
import re
import os
import socket

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
            with open(os.path.join(dest_path, "{}_system_info.json".format(socket.gethostname())), "w") as fp:
                system_data = SystemInfoAnalyzer.check_if_os_default(system_data,'users','user_name')
                system_data = SystemInfoAnalyzer.check_if_os_default(system_data, 'groups','group_name')
                json.dump(system_data, fp, indent=4)
                # TODO:call func that send it to file server and give it the json path

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
