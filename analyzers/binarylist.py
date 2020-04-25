from analyzers.analyzer import Analyzer
import os
import socket
import json

class BinaryListAnalyzer(Analyzer):

    '''
    this func will get the autorunpaths from the parser in a list and send the data to file attribute check and write
    to json (which will be send to ES)
    '''
    @staticmethod
    def analyze(paths, dest_path=DEST):
        try:

            # TODO: return paths to noa's attr func
            with open(os.path.join(dest_path, "{}_binary_list.json".format(socket.gethostname())), "w") as fp:
                to_json = {}
                i=0
                for path in paths:
                    to_json[i] = path
                    i+=1
                json.dump(to_json, fp, indent=4)

        except Exception as e:
            print("problem in bianrylist analyzer - analyze :",e)