from analyzers.analyzer import Analyzer
import os
import socket
import json

DEST = '/tmp'


class BinaryListAnalyzer(Analyzer):
    '''
    this func will get the autorunpaths from the parser in a list and send the data to file attribute check and write
    to json (which will be send to ES)
    '''

    @staticmethod
    def analyze(paths, dest_path=DEST):
        try:

            # write a file for es collection
            BinaryListAnalyzer.write_to_files(paths, dest_path, "{}_binary_list.json".format(socket.gethostname()))
            # write for Meta data examination
            dst_path_meta_data = "{}/MetaData".format("/".join(dest_path.split('/')[:-1]))
            os.makedirs(dst_path_meta_data, exist_ok=True)
            BinaryListAnalyzer.write_to_files(paths,dst_path_meta_data, "BinaryList.txt")


        except Exception as e:
            print("problem in bianrylist analyzer - analyze :", e)

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
                    i += 1
                json.dump(to_json, fp, indent=4)

        except Exception as e:
            print("problem in binarylist analyzer -write to files , path:{},error:{} ".format(os.path.join(dst_path,name),e))
