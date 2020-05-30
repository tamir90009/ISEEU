import os
import string
from collectors.collector import Collector

#files to exlude:
#global unfamiliar chars for hidden files search:
UNFAMILIARSTRINGS = string.punctuation + ' '
#HOMEPATH = r"/home"
PATH = r'/'


class HiddenFilesCollector(Collector):

    @staticmethod
    #Finding Hidden files founction, By defual search from home:
    def collect(dst_path):
        try:
            hidden_files = {}
            # Recurseive search on file system:
            for root, dictonaries, filenames in os.walk(PATH):
                for filename in filenames:
                    if filename[0] in UNFAMILIARSTRINGS:
                        # Movine the files from the same directory into a list:
                        if root not in [*hidden_files]:
                            hidden_files.update({root : [filename]})
                        else:
                            hidden_files[root].append(filename)
            # Returning the hidden files values
            with open("{}.json".format(dst_path), "w") as fp:
                fp.write('\n'.join(hidden_files))
        except:
            raise Exception("Error: Uknown Path")

