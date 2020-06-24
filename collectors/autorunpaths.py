from collectors.collector import Collector
from os import listdir
import os

AUTO_PATHS_MODIFY = ["/boot/grub/grub.cfg", "/etc/X11/xinit/xinitrc", "~/.bashrc", "/etc/bash.bashrc", "~/.bash_profile"]
AUTO_PATHS_DIRS = ["/etc/init.d/"]
HOME_DIR = "~/"

class AutoRunPathsCollector(Collector):


    '''
    this func get dst_path if needed , extract paths to auto runs  uses for persistence mechanism in linux and
    copy the paths to file for the parser to read
    '''
    @staticmethod
    def collect(dst_path):
        try:
            AutoRunPathsCollector.get_file_per_user()
            AutoRunPathsCollector.get_files_in_dir()

            with open("{}.json".format(dst_path),"w") as fp:
                fp.write('\n'.join(AUTO_PATHS_MODIFY))

        except Exception as e:
            print("problem in autorunpath collector - collect:{}".format(str(e)))


    '''
    this func gets an autorun dir and writes the file under it to the ist of autoruns
    '''
    @staticmethod
    def get_files_in_dir():
        try:
            for dir in AUTO_PATHS_DIRS:
                for f in listdir(dir):
                    AUTO_PATHS_MODIFY.append(os.path.join(dir, f))
        except Exception as e:
            print("problem in get_files_in_dir in autorunpaths - collector:{}".format(str(e)))

    '''
    this func get user profiles auto run files
    '''
    @staticmethod
    def get_file_per_user():
        try:
            users_list = AutoRunPathsCollector.users()
            for file in AUTO_PATHS_MODIFY:
                if HOME_DIR in file:
                    for u in users_list:
                        user_file = file.replace("~", u)
                        AUTO_PATHS_MODIFY.append(user_file)
                    AUTO_PATHS_MODIFY.remove(file)
        except Exception as e:
            print("problem in get_file_per_user in autorunpaths - collector:{}".format(str(e)))

    '''
    this func maps the users home directory list
    '''
    @staticmethod
    def users():
        try:
            users_homes = []
            for f in listdir("/home"):
                if f not in users_homes:
                    users_homes.append(os.path.join("/home", f))
            return users_homes
        except Exception as e:
            print("problem in users list in autorunpath -collector:{}".format(str(e)))



