from analyzers.analyzer import Analyzer
import json
import re
import socket

DEST = '/tmp'

class LogAnalyzer(Analyzer):

    # this run over the parsed logs data, run analytics on the data to check if it suspicious and save it as json file
    @staticmethod
    def analyze(logs_data, dst_path=DEST):
        try:
            auth_log_data = auth_log_anlyzer(logs_data['auth'])
            syslog_data = syslog_anlyzer(logs_data['syslog'])
            with open('{}/{}_auth_log.json'.format(dst_path, socket.gethostname()), 'w') as jf:
                json.dump(auth_log_data, jf)
            with open('{}/{}_syslog.json'.format(dst_path, socket.gethostname()), 'w') as jf:
                json.dump(syslog_data, jf)
        except Exception as e:
            raise Exception("problem in writing analytic data of logs_data - analyzer: {}".format(str(e)))


def auth_log_anlyzer(data):
    logs = data
    for ln in data.keys():
        ln = int(ln)
        try:
            if 'authentication failure' in logs[ln]['message']:
                if 'suspicious' in logs[ln].keys():
                    continue
                else:
                    data_check = {}
                    for i in range(ln, ln+10):
                        if i in data.keys():
                            data_check[i] = logs[i]
                    analyzed_data = failure(data_check)
                    for i in range(ln, ln+10):
                        if i in analyzed_data.keys():
                            logs[i] = analyzed_data[i]
                continue
            elif 'COMMAND=/usr/sbin/useradd' in logs[ln]['message']:
                logs[ln]['suspicious'] = True
                continue
            elif 'COMMAND=/usr/bin/passwd' in logs[ln]['message']:
                logs[ln]['suspicious'] = True
                continue
            elif 'password changed for' in logs[ln]['message']:
                logs[ln]['suspicious'] = True
                continue
            elif 'COMMAND=/usr/sbin/usermod -a -G sudo' in logs[ln]['message']:
                logs[ln]['suspicious'] = True
                continue
            elif 'COMMAND=/usr/sbin/usermod -aG sudo' in logs[ln]['message']:
                logs[ln]['suspicious'] = True
                continue
            elif re.findall("add \'\w+\' to group 'sudo'", logs[ln]['message']):
                logs[ln]['suspicious'] = True
                continue
            elif re.findall("add \'\w+\' to shadow group 'sudo'", logs[ln]['message']):
                logs[ln]['suspicious'] = True
                continue
            elif 'COMMAND=/usr/bin/crontab -e' in logs[ln]['message']:
                logs[ln]['suspicious'] = True
                continue
        except Exception as e:
            raise Exception("problem in analyze data of auth.log number: {} - analyzer: {}".format(ln, str(e)))
    return logs


# def syslog_anlyzer(data):
def syslog_anlyzer(data):
    logs = data
    for ln in data.keys():
        try:
            if 'dhcp' in logs[ln]['message'].lower():
                logs[ln]['important'] = True
                continue
            if 'error' in logs[ln]['message'].lower():
                logs[ln]['warning'] = True
                continue
            if 'usb' in logs[ln]['message'].lower():
                logs[ln]['warning'] = True
                continue
        except Exception as e:
            raise Exception("problem in analyze data of syslog number: {} - analyzer: {}".format(ln, str(e)))
    return logs


def failure(logs):
    return_log = logs
    try:
        logs_keys = list(logs.keys())
        suspicious_list = [logs_keys[0]]
        user = re.findall('\suser=([^\W]+)', logs[logs_keys[0]]['message'])[0]
        if user:
            count = 1
        else:
            count = 0
        for log_num in logs_keys[1:]:
            message = logs[log_num]['message']
            if 'authentication failure' in message:
                if re.findall('\suser=([^\W]+)', message)[0] == user:
                    suspicious_list.append(log_num)
                    times = re.findall('message repeated (\d+)', message)
                    if times:
                        count += int(times[0])
                    else:
                        count += 1
        if count > 2:
            for s in suspicious_list:
                return_log[s]['suspicious'] = True
    except Exception as e:
        raise Exception("problem in analyze failure authentications in auth.log - analyzer: {}".format(str(e)))
    return return_log


