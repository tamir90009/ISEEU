from parsers.parser import Parser
import re

CHKROOTKITPAT1 = r'\S{2,}'
CHKROOTKITPAT2 = r'\s{1,}'
CHKROOTKITPAT3 = r'\S{1,}'


class CHKRootkitParser(Parser):

    @staticmethod
    def parse(input_path):
        try:
            chkroot_output = []
            with open(input_path,'r') as f:
                for line in f.readlines():
                    try:
                        # If starting with checking...
                        if str(line).startswith('Checking'):
                            full_status = ''
                            status = re.findall(CHKROOTKITPAT1, line)
                            check = status[1]
                            status = status[2:]
                            for i in status:
                                full_status += i + ' '
                            status = full_status[:-1]
                            chkroot_output.append({'check': check[1:-4], 'status': status})
                        # if start with searching...
                        elif str(line).startswith('Searching'):
                            search, status = str(line).split("...")
                            search = search[14:]
                            spaces = re.findall(CHKROOTKITPAT2, status)
                            number_of_spaces = len(spaces[0])
                            status = status[number_of_spaces:]
                            chkroot_output.append({'search': search, 'status': status})
                        # if start with ! get the process information:
                        elif str(line).startswith('!'):
                            process_details = re.findall(CHKROOTKITPAT3, line)[1:]
                            user = process_details[0]
                            pid = process_details[1]
                            tty = process_details[2]
                            cmd = process_details[3:]
                            chkroot_output.append({'user': user, 'pid': pid, 'cmd': cmd,'status': 'found'})
                    except:
                        continue
            f.close()
            return chkroot_output
        except Exception as e:
            raise Exception("Cant parse Chkrootkit " + str(e))
