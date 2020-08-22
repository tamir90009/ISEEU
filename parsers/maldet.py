from parsers.parser import Parser
import re

class MalDetParser(Parser):
    @staticmethod
    def parse(input_path):
        maldet_output = []
        with open(input_path, 'r') as output:
            for line in output.readlines():
                if "{hit}" in line:
                    event = line.split("malware hit ")
                    regex = re.compile('(?P<mal>.*) found for (?P<path>.*)')
                    founds = regex.search(event[1])
                    # print("mal: {0}, path:{1}".format(mal,path))
                    maldet_output.append({'mal': founds.groupdict()['mal'], 'path': founds.groupdict()['path'], 'status': 'found'})
            output.close()
            return maldet_output
