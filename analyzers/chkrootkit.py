from additionalscripts.datasend import datasend
from analyzers.analyzer import Analyzer
import json
import os
import socket

DEST = r'/temp'

class CHKRootkitAnalyzer(Analyzer):

    @staticmethod
    def analyze(paths, dest_path=DEST):
        try:

            with open(os.path.join(dest_path, "{}_chkrootkit.json".format(socket.gethostname())), "w") as fp:
                to_json = {}
                i = 0
                for path in paths:
                    if not ('not found' in path['status'].lower() or path['status'].lower() == 'ok'
                            or 'none' in path['status'].lower() or 'checking' in path['status'].lower()):
                        to_json[i] = path
                        i += 1
                fp.write(json.dumps(to_json))
            datasend("./{}_chkrootkit.json".format(socket.gethostname()), "/home/elk/Temp/output")
        except Exception as e:
            raise  Exception("problem in chkrootkit analyzer - analyze :", e)