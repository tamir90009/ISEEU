from analyzers.analyzer import Analyzer
import socket

class LDPreloadAnalyzer(Analyzer):

    @staticmethod
    def analyze(parsed_data, output_path):
        output_dict = {}
        for i in parsed_data:
            output_dict[i] = {"suspicious": parsed_data[i]}
        host_name = socket.gethostname()
        LDPreloadAnalyzer.write_json(output_dict, output_path + "/%s_ldpreload" % host_name)
