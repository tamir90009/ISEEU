from parsers.parser import Parser

class HiddenFilesParser(Parser):

    @staticmethod
    def parse(input_path):
        hidden_output = []
        with open(input_path,'rb') as output:
            for line in output.readlines():
                try:
                    hidden_output.append(line)
                except:
                    continue
        output.close()
        return hidden_output