from analyzers.analyzer import Analyzer


class LibraryPathAnalyzer(Analyzer):

    @staticmethod
    def analyze(parsed_data, output_path):
        if parsed_data is None:
            return
        output_dict = {}
        for i in parsed_data:
            output_dict[i] = {"suspicious": True}

        LibraryPathAnalyzer.write_json(output_dict, output_path + "/librarypath")
