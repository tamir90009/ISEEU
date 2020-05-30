from analyzers.analyzer import Analyzer
import socket

class LDPreloadAnalyzer(Analyzer):

    @staticmethod
    def analyze(parsed_data, output_path):
        output_list = []
        for i in parsed_data:
            output_list.append({'file': i, "suspicious": True})
        host_name = socket.gethostname()
        LDPreloadAnalyzer.write_json(output_list, output_path + "/%s_ldpreload" % host_name)
