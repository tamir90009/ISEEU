import os
import string


#global unfamiliar chars for hidden files search:
UNFAMILIARSTRINGS = string.punctuation + ' '
#HOMEPATH = r"/home"

class HiddenFiles:

    def __init__(self):
        self._hidden_files = {}

#Finding Hidden files founction, By defual search from home:
    def find_hidden(self,path="/home"):
        try:
            hidden_files = {}
            #Recurseive search on file system:

            for root, dictonaries, filenames in os.walk(path):
                for filename in filenames:
                    #Classifaing files that start with unfimiliar char:
                    if filename[0] in UNFAMILIARSTRINGS:
                        #Movine the files from the same directory into a list:
                        if root not in [*hidden_files]:
                            hidden_files.update({root:[filename]})
                        else:
                            hidden_files[root].append(filename)


            #Returning the hidden files values
            self._hidden_files = hidden_files

        except:
            raise Exception("Error: Uknown Path")

    def print(self):

        for key in [*self._hidden_files]:
            print("dict: {0} , files:{1}".format(key,self._hidden_files[key]))

