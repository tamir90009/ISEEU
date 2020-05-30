from additionalscripts.datasend import datasend
from analyzers.analyzer import Analyzer
import json
import os
import socket

DEST = r'/temp'
try:
    File = open(r'exclude.txt','r')
    exclude = File.read().replace(r"\n","").replace(r'/home/test',r'/home/{0}'.format(os.getlogin()))
except Exception as e:
    raise Exception("Exclude file not exist " + e)


class HiddenFilesAnalyzer(Analyzer):

    @staticmethod
    def analyze(paths, dest_path=DEST):
        try:


            with open(os.path.join(dest_path, "{}_hidden_files.json".format(socket.gethostname())), "w") as fp:
                to_json = {}
                i = 0
                for hidden_file in paths:
                    if hidden_file not in exclude:
                        to_json[i] = hidden_file
                        i += 1
                fp.write(json.dumps(to_json))
            datasend("./{}_hidden_files.json".format(socket.gethostname()), "/home/elk/Temp/output")

        except Exception as e:
            print("problem in hidden files analyzer - analyze :", e)