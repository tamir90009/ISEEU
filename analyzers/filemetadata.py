from analyzers.analyzer import Analyzer
import json
import os
import socket

DEST = '/tmp'


class FileMetaDataAnalyzer(Analyzer):

    # this func save the parsed meta data and save it as json file
    @staticmethod
    def analyze(files_meta_data, dst_path=DEST):
        try:
            analyzed_data = attr_check(files_meta_data)
            os.makedirs('{}/files_meta_data'.format(dst_path), exist_ok=True)
            for subject in analyzed_data.keys():
                with open('{}/files_meta_data/{}_{}.json'.format(dst_path, socket.gethostname(), subject), 'w') as jf:
                    json.dump(analyzed_data[subject], jf)
        except Exception as e:
            raise Exception("problem in writing analytic data of file_meta_data - analyzer :{}".format(str(e)))


def attr_check(data):
    logs = data
    for subject in data.keys():
        for ln in data[subject].keys():
            try:
                if ('a' in logs[subject][ln]['attributes']) or ('d' in logs[subject][ln]['attributes']) or\
                        ('i' in logs[subject][ln]['attributes']) or ('u' in logs[subject][ln]['attributes']):
                    logs[subject][ln]['suspicious'] = True
            except Exception as e:
                raise Exception("problem in analyze attributes of file_meta_data - analyzer :{}".format(str(e)))
    return logs
