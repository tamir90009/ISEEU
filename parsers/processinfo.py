from parsers.parser import Parser
import json

class ProcessInfoParser(Parser):


    '''
    this func  only print due to lack of analyzer and no need of parsing (already done in the tool
     that collects the data found in additional scripts)
    '''
    @staticmethod
    def parse(input_path):
        try:
            with open("{}.json".format(input_path), 'r') as fp:
                processlist = json.load(fp)

            return processlist
        except Exception as e:
            raise Exception("problem in parse process info :{}".format(str(e)))

