
from analyzers.analyzer import Analyzer
from additionalscripts.datasend import datasend
import json
import os
import socket


DEST = r'/tmp'

class ClamAVAnalyzer(Analyzer):

    @staticmethod
    def analyze(paths, dest_path=DEST):
        try:
            with open(os.path.join(dest_path, "{}_clamav.json".format(socket.gethostname())), "w") as fp:
                to_json = {}
                i = 0
                for path in paths:
                    if not ('not found' in path['status'].lower() or 'ok' in path['status'].lower()
                            or 'none' in path['status'].lower() or 'checking' in path['status'].lower()):
                        to_json[i] = path
                        fp.write(json.dumps(to_json[i]) + '\n')
                        i += 1

            datasend(os.path.join(dest_path, "{}_clamav.json".format(socket.gethostname())),'clamav')
        except Exception as e:
            raise Exception("problem in clamav analyzer - analyze :" + str(e))
        try:
            dst_path_meta_data = "{}/MetaData".format("/".join(dest_path.split('/')[:-1]))
            os.makedirs(dst_path_meta_data, exist_ok=True)
            for f in paths:
                try:
                    with open('{}/Clamav.txt'.format(dst_path_meta_data), "a+") as meta_data_file:
                        meta_data_file.write('{}\n'.format(f["path"]))
                except:
                    pass
        except Exception as e:
            raise Exception("Error with metadata function in ClamAV " + str(e))