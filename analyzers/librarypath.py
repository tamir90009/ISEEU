import os
from socket import socket
from analyzers.analyzer import Analyzer
from additionalscripts.datasend import datasend

class LibraryPathAnalyzer(Analyzer):

    @staticmethod
    def analyze(parsed_data, output_path):
        if parsed_data is None:
            return
        output_list = []
        for i in parsed_data:
            output_list.append({"path": i, "suspicious": True})

        host_name = socket.gethostname()
        LibraryPathAnalyzer.write_json(output_list, os.path.join(output_path, "%s_librarypath.json" % host_name))
        datasend(os.path.join(output_path, "%s_librarypath.json" % host_name), 'librarypath')
