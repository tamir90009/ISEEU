from additionalscripts.datasend import datasend
from analyzers.analyzer import Analyzer
import json
import os
import socket

DEST = "/tmp"



class RKHunterAnalyzer(Analyzer):

    @staticmethod
    def analyze(paths, dest_path=DEST):
        try:

            with open(os.path.join(dest_path, "{}_rkhunter.json".format(socket.gethostname())), "w") as fp:
                to_json = {}
                i = 0
                for path in paths:
                    if not ('not found' in path['status'].lower() or 'ok' in path['status'].lower()
                            or 'none' in path['status'].lower() or 'checking' in path['status'].lower()):
                        to_json[i] = path
                        fp.write(json.dumps(to_json[i]) + '\n')
                        i += 1
            datasend(os.path.join(dest_path, "{}_rkhunter.json".format(socket.gethostname())),'rkhunter')
        except Exception as e:
            raise Exception("problem in rkhunter analyzer - analyze :" + str(e))
        try:
            dst_path_meta_data = "{}/MetaData".format("/".join(dest_path.split('/')[:-1]))
            os.makedirs(dst_path_meta_data, exist_ok=True)
            for f in paths:
                try:
                    with open('{}/rkhunter.txt'.format(dst_path_meta_data), "a+") as meta_data_file:
                        meta_data_file.write('{}\n'.format(f["path"]))
                except:
                    pass
        except Exception as e:
            raise Exception("Error in rkhunter analyzer:metadata function " + str(e))