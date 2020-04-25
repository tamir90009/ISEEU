from parsers.parser import Parser


class LogParser(Parser):

    # this func parse the auth.log and syslog data and add it to data dictionary with 'auth' as key
    # and 'syslog' as key and return the dictionary
    @staticmethod
    def parse(self, dst_path):
        data = {'auth': parse_log(dst_path, 'auth.log'), 'syslog': parse_log(dst_path, 'syslog')}
        return data


def parse_log(dst_path, log_name):
    parsed_log = {}
    count = 1
    try:
        with open('{}/{}'.format(dst_path, log_name)) as current_file:
            log_lines = current_file.readlines()
    except Exception as e:
        raise Exception("problem in reading the log: {} - parser: {}".format(log_name, str(e)))
    try:
        for l in log_lines:
            attr = l.split(' ')
            time = ' '.join(attr[:3])
            subject = attr[4][:-1]
            message = ' '.join(attr[5:])[:-1]
            parsed_log[count] = {'time': time, 'subject': subject, 'message': message}
            count += 1
    except Exception as e:
        raise Exception("problem in parsing the data from the log: {} - parser: {}".format(log_name, str(e)))
    return parsed_log
