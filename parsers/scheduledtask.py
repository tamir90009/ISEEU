from parsers.parser import Parser
#from collectors.filemetadata import FileMetadataCollector
import glob
import pretty_cron
import re
import os


class ScheduledTaskParser(Parser):

    # this func parse the crontab files that in the destination, write the parsed data to dictionary and return it
    @staticmethod
    def parse(dst_path):
        files = []
        data = []
        cron_tabs = {}
        for file in glob.glob(r'{}/crontabs/*'.format(dst_path)):
            try:
                user = file.split('/')[-1]
                with open(file) as current_file:
                    crontab_list = current_file.readlines()
                for i in crontab_list:
                    if i[:1] == '#':
                        pass
                    elif i == '\n':
                        pass
                    else:
                        data.append(i)
            except Exception as e:
                raise Exception("problem in geting data from crontab file of:{} - parser: {}".format(file, str(e)))
            # split the data to sections and merge the data that have connection
            try:
                count = 1
                for i in data:
                    if '\t' in i:
                        tmp_line = i.split(' ')
                        line = []
                        for tl in tmp_line:
                            if '\t' in tl:
                                line += tl.split('\t')
                            else:
                                line.append(tl)
                    else:
                        line = i.split(' ')
                    time = ' '.join(line[:5])
                    command = ' '.join((line[5:]))[:-1]
                    cron_tabs['{}{}'.format(user, count)] = {'user': user, 'execution_time_origin_form': time,
                                                             'execution_time': pretty_cron.prettify_cron(time),
                                                             'command': command}
                    files += re.findall("/[^\s\t]+", command)
                    count += 1
            except Exception as e:
                raise Exception("problem in parcing the data from crontab file of:{} - parser: {}".format(file, str(e)))
        #FileMetadataCollector.collect(dst_path, files, 'scheduled_tasks')
        dst_path_meta_data = "{}/MetaData".format("/".join(dst_path.split('/')[:-1]))
        os.makedirs(dst_path_meta_data, exist_ok=True)
        for f in files:
            with open('{}/ScheduledTasks.txt'.format(dst_path_meta_data), "a+") as meta_data_file:
                meta_data_file.write('{}\n'.format(f))
        return cron_tabs
