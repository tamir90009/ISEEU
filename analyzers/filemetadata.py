from analyzers.analyzer import Analyzer
import json
import os
import socket
from additionalscripts.datasend import datasend
import re

DEST = '/tmp'


class FileMetaDataAnalyzer(Analyzer):

    '''
    this func save the parsed meta data and save it as json file
    '''
    @staticmethod
    def analyze(files_meta_data, dst_path=DEST):
        try:
            analyzed_data = attr_check(files_meta_data)
            with open(os.path.join(dst_path, '{}_metadata.json'.format(socket.gethostname())), 'w+') as jf:
                for subject in analyzed_data.keys():
                    for line in analyzed_data[subject]:
                        analyzed_data[subject][line]['source'] = subject
                        jf.write(json.dumps(analyzed_data[subject][line]) + '\n')
            datasend(os.path.join(dst_path, '{}_metadata.json'.format(socket.gethostname())), 'metadata')
        except Exception as e:
            raise Exception("problem in writing analytic data of file_meta_data - analyzer :{}".format(str(e)))


def attr_check(data):
    logs = data
    for subject in data.keys():
        for ln in data[subject].keys():
            suspicious_attr = ['a', 'd', 'i', 'u']
            try:
                for attr in re.findall('[A-z]', logs[subject][ln]['attributes']):
                    if attr in suspicious_attr:
                        logs[subject][ln]['suspicious'] = True
                        break
            except Exception as e:
                raise Exception("problem in analyze attributes of file_meta_data - analyzer :{}".format(str(e)))
    return logs
