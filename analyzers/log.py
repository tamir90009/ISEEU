from analyzers.analyzer import Analyzer
import json
import re
import socket
import os
import re
from additionalscripts.datasend import datasend

DEST = '/tmp'


class LogAnalyzer(Analyzer):
    '''
    this func gets the data from the parser and dst_path,
    its runs over the data and runs analytics to check if the data is suspicious and save it as json file to fst_path
    '''

    @staticmethod
    def analyze(logs_data, dst_path=DEST):
        try:
            auth_log_data = LogAnalyzer.auth_log_analyzer(logs_data['auth'])
            syslog_data = LogAnalyzer.syslog_anlyzer(logs_data['syslog'])
            with open(os.path.join(dst_path, '{}_authlog.json'.format(socket.gethostname())), 'w') as jf:
                for line in auth_log_data:
                    auth_log_data[line]['source_log'] = 'auth log'
                    jf.write(json.dumps(auth_log_data[line]) + '\n')
            datasend(os.path.join(dst_path, '{}_authlog.json'.format(socket.gethostname())), 'authlog')
            with open(os.path.join(dst_path, '{}_syslog.json'.format(socket.gethostname())), 'w') as jf:
                for line in syslog_data:
                    syslog_data[line]['source_log']='syslog'
                    jf.write(json.dumps(syslog_data[line]) + '\n')
            datasend(os.path.join(dst_path, '{}_syslog.json'.format(socket.gethostname())), 'syslog')
        except Exception as e:
            raise Exception("problem in writing analytic data of logs_data - analyzer: {}".format(str(e)))

    '''
    this func gets data from auth.log and check by few analytics if it suspicious or not
    '''
    @staticmethod
    def auth_log_analyzer(auth_log_data):
        suspicious_message = ['COMMAND=/usr/sbin/useradd', 'COMMAND=/usr/bin/passwd', 'password changed for',
                           'COMMAND=/usr/sbin/usermod -a -G sudo', 'COMMAND=/usr/sbin/usermod -aG sudo',
                           "add \'\w+\' to group 'sudo'", "add \'\w+\' to shadow group 'sudo'",
                           'COMMAND=/usr/bin/crontab -e', 'new user:', 'COMMAND=/bin/chmod 777']
        logs = auth_log_data
        for ln in auth_log_data.keys():
            ln = int(ln)
            try:
                if 'authentication failure' in logs[ln]['log_message']:
                    if 'suspicious' in logs[ln].keys():
                        continue
                    else:
                        data_check = {}
                        for i in range(ln, ln + 10):
                            if i in auth_log_data.keys():
                                data_check[i] = logs[i]
                        analyzed_data = LogAnalyzer.failure(data_check)
                        for i in range(ln, ln + 10):
                            if i in analyzed_data.keys():
                                logs[i] = analyzed_data[i]
                    continue
                else:
                    for message in suspicious_message:
                        if re.findall(message, logs[ln]['log_message']) == []:
                            logs[ln]['suspicious'] = False
                        else:
                        #if message in logs[ln]['log_message']:
                            logs[ln]['suspicious'] = True
                            continue
                    continue
            except Exception as e:
                raise Exception("problem in analyze data of auth.log number: {} - analyzer: {}".format(ln, str(e)))
        return logs

    '''
    this func gets data from syslog and check by few analytics if it suspicious or not
    '''
    @staticmethod
    def syslog_anlyzer(syslog_data):
        logs = syslog_data
        for ln in syslog_data.keys():
            try:
                if 'dhcp' in logs[ln]['log_message'].lower():
                    logs[ln]['important'] = True
                    continue
                if 'error' in logs[ln]['log_message'].lower():
                    logs[ln]['warning'] = True
                    continue
                if 'usb' in logs[ln]['log_message'].lower():
                    logs[ln]['warning'] = True
                    continue
            except Exception as e:
                raise Exception("problem in analyze data of syslog number: {} - analyzer: {}".format(ln, str(e)))
        return logs

    '''
    this func gets logs from auth.log that is about failure login and check by few analytics if it suspicious or not
    '''
    @staticmethod
    def failure(failure_logs):
        return_log = failure_logs
        try:
            logs_keys = list(failure_logs.keys())
            suspicious_list = [logs_keys[0]]
            user = re.findall('\suser=([^\W]+)', failure_logs[logs_keys[0]]['log_message'])[0]
            if user:
                count = 1
            else:
                count = 0
            for log_num in logs_keys[1:]:
                message = failure_logs[log_num]['log_message']
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
