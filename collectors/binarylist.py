from collectors.collector import Collector
from os import listdir
import os

class BinaryListCollector(Collector):

    '''
       this func will map all the binaries in the system
       it gets a destination path
       and write all the information (list of system binaries) to the path
    '''

    @staticmethod
    def collect(dst_path):
        try:
            bin_dir_list = BinaryListCollector.get_files_in_dir("/bin/")
            sbin_dir_list = BinaryListCollector.get_files_in_dir("/sbin/")

            bin_dir_list.extend(sbin_dir_list)
            with open("{}.json".format(dst_path),"w") as fp:
                fp.write('\n'.join(bin_dir_list))

        except Exception as e:
            print("problem in binarylist - collector :"+str(e))


    '''
     this func gets an binary dir file under it to list only the  files in it
     it returns a list of file names
     '''

    @staticmethod
    def get_files_in_dir(dir):
        try:
            bins = []
            for f in listdir(dir):
                bins.append(os.path.join(dir, f))
            return bins
        except Exception as e:
            print("problem in get_files_in_dir in binarylist - collector:" + str(e))

pp=BinaryListCollector.collect("/tmp/binarylist")