from parsers.parser import Parser
import re

PATHPATTERN = r'(\/[A-z]{0,}\/{0,1}?){1,}'


class AVScanParser(Parser):

    @staticmethod
    def parse(input_path):
        clamav_output = []
        with open(input_path, 'rb') as avoutput:
            for line in avoutput.readlines():
                try:
                    path, status = line.split(":")
                    if status:
                        status = status[1:]
                    path_exist = re.search(PATHPATTERN, line)
                    if bool(path_exist):
                        clamav_output.append({'path': path, 'status': status})
                except:
                    continue
        avoutput.close()
        return clamav_output
