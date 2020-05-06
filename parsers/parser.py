class Parser(object):

    def parse_file(self, file_path):
        with open(file_path, "rb") as f:
            self.parse(f.readlines())

    def parse(self, data):
        raise NotImplemented