from parsers.parser import Parser
import re

PATHPATTERN = r'(\/[A-z]{0,}\/{0,1}?){1,}'
STATUSPATTERN = r'm[A-Z]([A-z]){1,}(\s{0,}[A-z]{1,}){0,}' # need to remove the first letter [1:]


class RKHunterParser(Parser):

    @staticmethod
    def parse(input_path):
        rkhunter_output = []
        with open(input_path,'r') as avoutput:
            # Moving line by line and exporting the important
            for line in avoutput.readlines():
                try:
                    # Starting with checking:
                    if str(line[4:]).startswith('Checking'):
                        status = re.search(STATUSPATTERN, line).group()
                        UnwantedData = 23 + len(str(status))
                        check = line[4:-UnwantedData]
                        # print("check: {0} , status: {1}".format(check, status[1:]))
                        rkhunter_output.append({'check': check, 'status': status[1:]})
                    else:
                        file_path = re.search(PATHPATTERN, line)
                        if file_path:
                            path = file_path.group()
                        status = re.search(STATUSPATTERN, line)
                        if status:
                            clean_status = status.group()[1:]
                        if bool(file_path) == False and bool(status) == True:
                            rkhunter_output.append({'rootkitscan': line[4:-UnwantedData], 'status': clean_status})
                        elif bool(file_path) == True and bool(status) == True:
                            rkhunter_output.append({'path': path, 'status': clean_status})
                        else:
                            continue
                except Exception as e:
                    continue
            avoutput.close()
            return rkhunter_output