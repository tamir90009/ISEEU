from analyzers.analyzer import Analyzer
import os
import socket
import json
from additionalscripts.datasend import datasend

DEST = '/tmp'

class BinaryListAnalyzer(Analyzer):
    '''
    this func will get the binary list from the parser in a list and send the data to file attribute check and write
    to json (which will be send to ES)
    '''

    @staticmethod
    def analyze(paths, dest_path=DEST):
        try:

            # write a file for es collection
            BinaryListAnalyzer.write_to_files(paths, dest_path, "{}_binarylist.json".format(socket.gethostname()))
            # write for Meta data examination
            dst_path_meta_data = "{}/MetaData".format("/".join(dest_path.split('/')[:-1]))
            os.makedirs(dst_path_meta_data, exist_ok=True)
            BinaryListAnalyzer.write_to_files(paths, dst_path_meta_data, "BinaryList.txt")
            datasend(os.path.join(dest_path, "{}_binarylist.json".format(socket.gethostname())), "binarylist")

        except Exception as e:
            raise Exception("problem in bianrylist analyzer - analyze :", str(e))

    '''
    this func will write the paths list to a file which will the the metadata extractor monitors for deeper examination
    and write it to a file that will be collected to es 
    params: destination path for file 
    '''

    @staticmethod
    def write_to_files(paths, dst_path, name):
        try:
            with open(os.path.join(dst_path, name), "w") as fp:
                to_json = {}
                i = 0
                for path in paths:
                    to_json[i] = path
                    fp.write(json.dumps(to_json[i]) + '\n')
                    i += 1


        except Exception as e:
            print(
                "problem in binarylist analyzer -write to files, path:{},error:{} ".format(os.path.join(dst_path, name),
                                                                                           e))
