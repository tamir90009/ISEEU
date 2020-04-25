from parsers.parser import Parser
import json

class AutoRunPathsParser(Parser):


    '''

    this func will read the autorun paths collector autoput in to a list and send it to the analyzer
    '''
    @staticmethod
    def parse(input_path):
        try:
            data = []
            with open("{}.json".format(input_path),'r') as fp:
                data = fp.readlines()
            paths = [x.strip() for x in data]
            return paths

        except Exception as e:
            raise Exception("problem in parse autorun paths  :{}".format(str(e)))


#pp=AutoRunPathsParser().parse('/tmp/autopaths')
