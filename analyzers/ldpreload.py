import os
from analyzers.analyzer import Analyzer
import socket
from additionalscripts.datasend import datasend

class LDPreloadAnalyzer(Analyzer):

    @staticmethod
    def analyze(parsed_data, output_path):
        output_list = []
        for i in parsed_data:
            if not i:
                output_list.append({'file': i, "suspicious": True})
        host_name = socket.gethostname()
        LDPreloadAnalyzer.write_json(output_list, os.path.join(output_path, "%s_ldpreload.json" % host_name))
        datasend(os.path.join(output_path, "%s_ldpreload.json" % host_name), 'ldpreload')
