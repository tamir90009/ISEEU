from additionalscripts.datasend import datasend
from analyzers.analyzer import Analyzer
import json
import os
import socket

DEST = "/home/elk/Temp/output"



class RKHunterAnalyzer(Analyzer):

    @staticmethod
    def analyze(paths, dest_path=DEST):
        try:

            with open(os.path.join(dest_path, "{}_rkhunter.json".format(socket.gethostname())), "w") as fp:
                to_json = {}
                i = 0
                for path in paths:
                    if not ('not found' in path['status'].lower() or path['status'].lower() == 'ok'
                            or 'none' in path['status'].lower() or 'checking' in path['status'].lower()):
                        to_json[i] = path
                        fp.write(json.dumps(to_json[i]) + '\n')
                        i += 1
            datasend("./{}_rkhunter.json".format(socket.gethostname()))
        except Exception as e:
            raise Exception("problem in rkhunter analyzer - analyze :", e)