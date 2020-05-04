import os
import subprocess as sub
import string
import re
from analyzers import analyazer
import analyzers
analy = analyazer.Analyzer()
#global unfamiliar chars for hidden files search:
UNFAMILIARSTRINGS = string.punctuation + ' '
#Home Directory:
HOMEPATH = r"/home"
#Anti-Virus Headers:
CKROOTKIT = 'CKR'
MALDET = 'MAD'
CLAMAV = 'CLA'
RKHUNTER = 'RKH'
LYNIS = 'LYN'

#Regex patterns:
PATHPATTERN = r'(\/[A-z]{0,}\/{0,1}?){1,}'
STATUSPATTERN = r'm[A-Z]([A-z]){1,}(\s{0,}[A-z]{1,}){0,}' # need to remove the first letter [1:]

class ISEEUParser:
    def __init__(self):
        self.out = ''

    def parse(self,av,avoutput):
        try:
            #From bytes to string:
            avoutput = avoutput.decode('utf-8')
            #Checking from which AV the output came from and than send it to the right praser:
            if av == CKROOTKIT:
                chkroot_output = []

                for line in avoutput.splitlines():
                    try:
                        #If starting with checking...
                        if str(line).startswith('Checking'):
                            # print(line)
                            full_status = ''
                            status = re.findall(CHKROOTKITPAT1, line)
                            check = status[1]
                            status = status[2:]
                            for i in status:
                                full_status += i + ' '
                            status = full_status[:-1]
                            #print the check
                            #print("check: {0}, status: {1}".format(check[1:-4], status))
                            chkroot_output.append({'check':check[1:-4],'status':status})
                        #if start with searching...
                        elif str(line).startswith('Searching'):
                            search, status = str(line).split("...")
                            search = search[14:]
                            spaces = re.findall(CHKROOTKITPAT2, status)
                            number_of_spaces = len(spaces[0])
                            status = status[number_of_spaces:]

                            #print("search: {0}, status: {1}".format(search, status))
                            chkroot_output.append({'search': search, 'status': status})
                        #if start with ! get the process information:
                        elif str(line).startswith('!'):
                            process_details = re.findall('\S{1,}', line)[1:]
                            user = process_details[0]
                            pid = process_details[1]
                            tty = process_details[2]
                            cmd = process_details[3:]
                            #print("user: {0}, pid: {1}, cmd: {2}".format(user, pid, cmd))
                            chkroot_output.append({'user': user, 'pid': pid,'cmd':cmd})
                            # UnwantedData = 23 + len(str(status))
                            # print(line)
                            # print(status)
                            # check = line[4:-UnwantedData]
                            # print("check: {0} , status: {1}".format(check, status[1:]))
                        # print(line
                    except:
                        continue
                analy.analyzer(chkroot_output, av)
            elif av == MALDET:
                maldet_output = []
                for line in avoutput.splitlines():
                    if "{hit}" in line:
                        event= line.split("malware hit ")
                        mal = event[1].split(" ")[0]
                        path =  event[1].split(" ")[-1]
                        #print("mal: {0}, path:{1}".format(mal,path))
                        maldet_output({'mal':mal,'path':path})
                analy.analyzer(maldet_output, av)
            elif av == RKHUNTER:
                rkhunter_output = []
                #Moving line by line and exporting the important
                for line in avoutput.splitlines():
                    try:
                        #Starting
                        if str(line[4:]).startswith('Checking'):
                            status = re.search(STATUSPATTERN, line).group()
                            UnwantedData = 23 + len(str(status))
                            check = line[4:-UnwantedData]
                            #print("check: {0} , status: {1}".format(check, status[1:]))
                            rkhunter_output.append({'check':check,'status':status[1:]})

                        else:
                            file_path = re.search(PATHPATTERN, line)
                            if file_path:
                                path = file_path.group()

                            status = re.search(STATUSPATTERN, line)
                            if status:
                                clean_status = status.group()[1:]

                            if bool(file_path) == False and bool(status) == True:
                            #    print("[*]Rootkitscan: {0}, status: {1}".format(line[4:-UnwantedData], clean_status))
                                rkhunter_output.append({'rootkitscan':line[4:-UnwantedData] , 'status': clean_status})
                            elif bool(file_path) == True and bool(status) == True:
                             #   print("[*]Path: {0}, Status: {1}".format(path, clean_status))
                                rkhunter_output.append({'path': path, 'status': clean_status})
                            else:
                                continue

                                # print("[*]Line: {0}".format(line))

                            # print("\n")

                    except Exception as e:
                        print(e)
                analy.analyzer(rkhunter_output, av)

            elif av == CLAMAV:
                clamav_output = []
                for line in avoutput.splitlines():
                    try:

                        path, status = line.split(":")
                        if status:
                            status = status[1:]
                        path_exist = re.search(PATHPATTERN, line)
                        if bool(path_exist):
                            #print("path:{0},status:{1}".format(path, status))
                            clamav_output.append({'path':path,'status':status})

                    except:
                        continue
                analy.analyzer(clamav_output, av)




            else:
                raise Exception("Wrong id")
        except Exception as e:
            raise Exception(e)