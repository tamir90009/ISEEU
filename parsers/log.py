from parsers.parser import Parser
import os

class LogParser(Parser):

    '''
    this func parse the auth.log and syslog data and add it to data dictionary with 'auth' as key
    and 'syslog' as key and return the dictionary
    '''
    @staticmethod
    def parse(dst_path):
        data = {'auth': LogParser.parse_log(dst_path, 'auth.log'), 'syslog': LogParser.parse_log(dst_path, 'syslog')}
        return data

    @staticmethod
    def parse_log(dst_path, log_name):
        parsed_log = {}
        count = 1
        try:
            with open(os.path.join(dst_path, log_name), "r") as current_file:
                log_lines = current_file.readlines()
        except Exception as e:
            raise Exception("problem in reading the log: {} - parser: {}".format(log_name, str(e)))
        try:
            for l in log_lines:
                attr = l.split(' ')
                time = ' '.join(attr[:3])
                subject = attr[4][:-1]
                message = ' '.join(attr[5:])[:-1]
                parsed_log[count] = {'log_time': time, 'log_subject': subject, 'log_message': message}
                count += 1
        except Exception as e:
            raise Exception("problem in parsing the data from the log: {} - parser: {}".format(log_name, str(e)))
        return parsed_log
