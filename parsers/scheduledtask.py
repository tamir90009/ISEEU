from parsers.parser import Parser
from collectors.filemetadata import FileMetadataCollector
import glob
import pretty_cron
import re


class ScheduledTaskParser(Parser):

    # this func parse the crontab files that in the destination, write the parsed data to dictionary and return it
    @staticmethod
    def parse(self, dst_path):
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
                        for l in tmp_line:
                            if '\t' in l:
                                line += l.split('\t')
                            else:
                                line.append(l)
                    else:
                        line = i.split(' ')
                    time = ' '.join(line[:5])
                    command = ' '.join((line[5:]))[:-1]

                    #cron_tabs[i] = (json.dumps({'user': user, 'execution_time_origin_form': time,
                    #                            'execution_time': pretty_cron.prettify_cron(time),
                    #                           'command': command}))
                    cron_tabs['{}{}'.format(user, count)] = {'user': user, 'execution_time_origin_form': time,
                                                'execution_time': pretty_cron.prettify_cron(time),
                                              'command': command}
                    files += re.findall("/[^\s\t]+", command)
                    count += 1
            except Exception as e:
                raise Exception("problem in parcing the data from crontab file of:{} - parser: {}".format(file, str(e)))
        FileMetadataCollector.collect(files, 'scheduled_tasks')
        return cron_tabs
