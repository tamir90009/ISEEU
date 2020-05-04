from parsers.parser import Parser


class MalDetParser(Parser):
    @staticmethod
    def parse(input_path):
        maldet_output = []
        with open(input_path, 'rb') as output:
            for line in output.readlines():
                if "{hit}" in line:
                    event = line.split("malware hit ")
                    mal = event[1].split(" ")[0]
                    path = event[1].split(" ")[-1]
                    # print("mal: {0}, path:{1}".format(mal,path))
                    maldet_output.append({'mal': mal, 'path': path, 'status': 'found'})
            output.close()
            return maldet_output
