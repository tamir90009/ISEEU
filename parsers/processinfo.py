from parsers.parser import Parser
import json

class ProcessInfoParser(Parser):


    '''
    this func curently only print due to lack of analyzer and no need of parseing (already done in the tool
     that collects the data found in additional scripts)

    '''
    @staticmethod
    def parse(input_path):
        try:
            with open(input_path,'r') as fp:
                processlist = json.load(fp)
                for pid in processlist:
                    print(processlist[pid]['_pid'],processlist[pid]['_mem'],processlist[pid]['_cpu'],
                          processlist[pid]['_user'],processlist[pid]['_tty'],processlist[pid]['_stat'],
                          processlist[pid]['_start'],processlist[pid]['_time'],processlist[pid]['_cmdline'],
                          processlist[pid]['_env'])
                    print(processlist[pid]['_list_of_file_descript'])
                    print(processlist[pid]['_networking_unix'])
                    print(processlist[pid]['_networking_internet'])

        except Exception as e:
            raise Exception("problem in parse process info :{}.".format(str(e)))


pp=ProcessInfoParser().parse('/tmp/process_info.json')
