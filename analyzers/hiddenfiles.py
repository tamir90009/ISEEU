from additionalscripts.datasend import datasend
from analyzers.analyzer import Analyzer
import json
import os
import socket

DEST = r'/temp'



class HiddenFilesAnalyzer(Analyzer):

    @staticmethod
    def analyze(paths, dest_path=DEST):
        try:
            File = open(r'collectors/exclude.txt', 'r')
            exclude = File.read().replace(r"\n", "").replace(r'/home/test', r'/home/{0}'.format(os.getlogin()))
        except Exception as e:
            raise Exception("Exclude file not exist " + str(e))

        try:
            with open(os.path.join(dest_path, "{}_hiddenfiles.json".format(socket.gethostname())), "w") as fp:
                to_json = {}
                i = 0
                for hidden_file in paths:
                    if hidden_file not in exclude:
                        to_json[i] = hidden_file
                        fp.write(json.dumps(to_json[i]) + '\n')
                        i += 1
            datasend(os.path.join(dest_path, "{}_hiddenfiles.json".format(socket.gethostname())),'hiddenfiles')
        except Exception as e:
            raise Exception("problem in hidden files analyzer - analyze :" + str(e))
        try:
            dst_path_meta_data = "{}/MetaData".format("/".join(dest_path.split('/')[:-1]))
            os.makedirs(dst_path_meta_data, exist_ok=True)
            for f in paths:
                if f not in exclude:
                    with open('{}/HiddenFiles.txt'.format(dst_path_meta_data), "a+") as meta_data_file:
                        meta_data_file.write('{}\n'.format(f))
        except Exception as e:
            raise Exception("problem in writing the data to file- analyzer: {}".format(str(e)))
