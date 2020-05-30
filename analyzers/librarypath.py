from socket import socket
from analyzers.analyzer import Analyzer


class LibraryPathAnalyzer(Analyzer):

    @staticmethod
    def analyze(parsed_data, output_path):
        if parsed_data is None:
            return
        output_list = []
        for i in parsed_data:
            output_list.append({"path": i, "suspicious": True})

        host_name = socket.gethostname()
        LibraryPathAnalyzer.write_json(output_list, output_path + "/%s_librarypath" % host_name)
