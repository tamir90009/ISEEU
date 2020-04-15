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
            with open("{}.json".format(input_path),'r') as fp:
                processlist = json.load(fp)

                return processlist
                #
                # for pid in processlist:
                #     print(processlist[pid]['_pid'],processlist[pid]['_ppid']
        except Exception as e:
            raise Exception("problem in parse process info :{}".format(str(e)))

#
# pp=ProcessInfoParser().parse('/tmp/process_info2.json')
