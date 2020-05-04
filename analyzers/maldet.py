
from analyzers.analyzer import Analyzer
import json
import os
import socket

DEST = r'/temp'

class MalDetAnalyzer(Analyzer):

    @staticmethod
    def analyze(paths, dest_path=DEST):
        try:
            # TODO: return paths to noa's attr func
            with open(os.path.join(dest_path, "{}_maldet.json".format(socket.gethostname())), "w") as fp:
                to_json = {}
                i = 0
                for path in paths:
                    if not ('not found' in path['status'].lower() or path['status'].lower() == 'ok'
                            or 'none' in path['status'].lower() or 'checking' in path['status'].lower()):
                        to_json[i] = path
                        i += 1
                json.dump(to_json, fp, indent=4)
        except Exception as e:
            print("problem in maldet analyzer - analyze :", e)