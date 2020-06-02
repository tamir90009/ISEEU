from parsers.parser import Parser


class HiddenFilesParser(Parser):

    @staticmethod
    def parse(input_path):
        hidden_output = []
        with open(input_path,'r') as output:
            for line in output.readlines():
                #print(type(line.decode('utf-8')))
                try:
                    line = line.replace("\n", '')
                    hidden_output.append(line)
                except:
                    pass
        return hidden_output