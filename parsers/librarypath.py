from parsers.parser import Parser


class LibraryPathAnalyzer(Parser):

    def parse(self, data):
        if data[0] == 'empty':
            return None
        else:
            return data[0].split(":")
