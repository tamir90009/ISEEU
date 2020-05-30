from parsers.parser import Parser
import json


class SystemInfoParser(Parser):

    '''
    this func  only print due to lack of analyzer and no need of parsing (already done in the tool
     that collects the data found
     it gets the information collected in the collector file  for input
     and return the info as an object
    '''

    @staticmethod
    def parse(input_path):
        try:
            with open("{}.json".format(input_path), 'r') as fp:
                return json.load(fp)

        except Exception as e:
            raise Exception("problem in parse process info :{}".format(str(e)))

#
# pp=SystemInfoParser().parse('/tmp/systeminfo')
