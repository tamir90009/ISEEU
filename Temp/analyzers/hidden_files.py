
from analyzers.analyzer import Analyzer
import json
import os
import socket

DEST = r'/temp'
try:
    File = open(r'exclude.txt','r')
    exclude = File.read().replace(r"\n","").replace(r'/home/test',r'/home/{0}'.format(os.getlogin()))
except:
    raise Exception("Exclude file not exist")

class HiddenFilesAnalyzer(Analyzer):

    @staticmethod
    def analyze(paths, dest_path=DEST):
        try:

            # TODO: return paths to noa's attr func
            with open(os.path.join(dest_path, "{}_hidden_files.json".format(socket.gethostname())), "w") as fp:
                to_json = {}
                i = 0
                for hidden_file in paths:
                    if hidden_file not in exclude:
                        to_json[i] = hidden_file
                        i += 1
                json.dump(to_json, fp, indent=4)

        except Exception as e:
            print("problem in hidden files analyzer - analyze :", e)