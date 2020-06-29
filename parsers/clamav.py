from parsers.parser import Parser
import re

PATHPATTERN = r'(\/[A-z]{0,}\/{0,1}?){1,}'

class ClamAVParser(Parser):

    @staticmethod
    def parse(input_path):
        clamav_output = []
        with open(input_path, 'r') as avoutput:
            for line in avoutput.readlines():
                try:
                    path, status = line.split(":")
                    if status:
                        status = status[1:]
                    path_exist = re.search(PATHPATTERN, line)
                    if path_exist:
                        clamav_output.append({'path': path, 'status': status[:-1]})
                except:
                    continue
        avoutput.close()
        return clamav_output
