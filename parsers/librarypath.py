from parsers.parser import Parser


class LibraryPathParser(Parser):

    @staticmethod
    def parse(data_file_path):
        try:
            with open(data_file_path, "r") as f:
                data = f.readlines()
        except Exception as e:
            raise e
        if data[0] == 'empty':
            return None
        else:
            return data[0].split(":")
