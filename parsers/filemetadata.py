from parsers.parser import Parser
import pwd
import time
import glob


class FileMetaDataParser(Parser):

    '''
    this func parse all the data from the file in destination into dictionary and return it
    '''
    @staticmethod
    def parse(dst_path):
        files = glob.glob('{}/*'.format(dst_path))
        data = {}
        for f in files:
            subject = f.split('/')[-1]
            try:
                with open(f, 'r') as current_file:
                    f_list = current_file.readlines()
            except Exception as e:
                raise Exception("no file of meta data in the dst_path- parser: {}".format(str(e)))
                continue

            for i in f_list:
                try:
                    cur_dict = eval(i)
                    data[subject] = {}
                    data[subject][cur_dict['file_path']] = {'file': cur_dict['file_path'],
                                                            'permissions': cur_dict['permissions'],
                                                            'owner': pwd.getpwuid(cur_dict['owner']).pw_name,
                                                            'access_time': time.asctime(time.localtime(cur_dict['atime'])),
                                                            'modified_time': time.asctime(time.localtime(cur_dict['mtime'])),
                                                            'information_change_time': time.asctime(time.localtime(cur_dict['ctime'])),
                                                            'size': cur_dict['size'], 'attributes': cur_dict['attr'],
                                                            'sha1': cur_dict['sha1']}
                except Exception as e:
                    raise Exception("problem in parse the data for: {} - parser: {}".format(i, str(e)))
        return data
