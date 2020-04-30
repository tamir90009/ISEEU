from parsers.parser import Parser

class BinaryListParser(Parser):

    '''

    this func will read the binary paths collector autoput in to a list and send it to the analyzer
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
            raise Exception("problem in parse binarylist paths  :{}".format(str(e)))


#pp=AutoRunPathsParser().parse('/tmp/binarylist')
