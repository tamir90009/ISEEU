from collectors.collector import Collector
import os
import subprocess
import shutil
import pwd


class FileMetadataCollector(Collector):

    # this func gets the metadata of file using os.staf and the two
    # other functions and save it to file in the destination
    @staticmethod
    def collect(dst_path, file_list, subject):
        for f in file_list:
            d = {}
            try:
                st = os.stat(f)
                d["file_path"] = f
                d["permissions"] = get_permissions(f)
                d["owner"] = st.st_uid
                d["atime"] = st.st_atime
                d["mtime"] = st.st_mtime
                d["ctime"] = st.st_ctime
                d["size"] = st.st_size
                d["attr"] = get_attr(f)
            except Exception as e:
                raise Exception("problem in getting the metadata for the file :{} - collector: {}".format(f, str(e)))

            # write the data to file in destination
            with open('{}/files_meta_data/{}'.format(dst_path, subject), 'a') as current_file:
                current_file.write('{}\n'.format(d))

def get_permissions(file_path):
    # this func gets the permissions of file using ls -l command and returns it
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
    # this func gets the attributes of file using lsattr command and returns it
    try:
        task = subprocess.Popen("lsattr -R {}".format(file_path),
                                shell=True,
                                stdout=subprocess.PIPE)
        file_attr = task.stdout.read()
        return file_attr.decode().split(' ')[0]
    except Exception as e:
        raise Exception("problem in getting the attributes for the file:{} - collector: {}".format(file_path, str(e)))
    return ''

