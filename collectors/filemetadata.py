from collectors.collector import Collector
import os
import subprocess
from pathlib import Path
import shutil
import pwd
import glob
import hashlib

class FileMetaDataCollector(Collector):

    '''
    this func gets the metadata of file using os.staf and the two
    other functions and save it to file in the destination
    '''
    @staticmethod
    def collect(dst_path):
        tasks_files = glob.glob("{}/MetaData/*.txt".format("/".join(dst_path.split('/')[:-1])))
        for tf in tasks_files:
            with open(tf, "r") as task:
                files_list = task.readlines()
            files_list = list(set(map(lambda x: x[:-1], files_list)))
            subject = tf.split("/")[-1][:-4]
            for file in files_list:
                file = file.strip('\"')
                if os.path.isfile(file):
                    data = {}
                    try:
                        st = os.stat(file)
                        data["file_path"] = file
                        data["permissions"] = get_permissions(file)
                        data["owner"] = st.st_uid
                        data["atime"] = st.st_atime
                        data["mtime"] = st.st_mtime
                        data["ctime"] = st.st_ctime
                        data["size"] = st.st_size
                        data["attr"] = ''
                        if not os.path.islink(file):
                            data["attr"] = get_attr(file)
                        data["sha1"] = hashlib.sha1(open(file, 'rb').read()).hexdigest()
                    except Exception as e:
                        print("problem in getting the metadata for the file :{} - collector: {}".format(file, str(e)))
                    os.makedirs(dst_path, exist_ok=True)
                    with open('{}/{}'.format(dst_path, subject), "a+") as current_file:
                        current_file.write('{}\n'.format(data))
                else:
                    print('file not found: %s' % file)


def get_permissions(file_path):
    '''
    this func gets the permissions of file using ls -l command and returns it
    '''
    try:
        task = subprocess.Popen("ls -l {}".format(file_path),
                                shell=True,
                                stdout=subprocess.PIPE)
        file_attr = task.stdout.read()
        return file_attr.decode()[1:10]
    except Exception as e:
        raise Exception("problem in getting the permissions for the file:{} - collector: {}".format(file_path, str(e)))
    return ''


def get_attr(file_path):
    '''
    this func gets the attributes of file using lsattr command and returns it
    '''
    try:
        task = subprocess.Popen("lsattr -R {}".format(file_path),
                                shell=True,
                                stdout=subprocess.PIPE)
        file_attr = task.stdout.read()
        return file_attr.decode().split(' ')[0]
    except Exception as e:
        raise Exception("problem in getting the attributes for the file:{} - collector: {}".format(file_path, str(e)))
    return ''

