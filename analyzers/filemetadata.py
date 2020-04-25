from analyzers.analyzer import Analyzer
import json


class FileMetaDataAnalyzer(Analyzer):

    # this func save the parsed meta data and save it as json file
    @staticmethod
    def analyze(self, dst_path, files_meta_data, analytic_folder_path):
        try:
            analyzed_data = attr_check(files_meta_data)
            for subject in analyzed_data.keys():
                with open('{}/{}/files_meta_data/{}.json'.format(dst_path, analytic_folder_path, subject), 'w') as jf:
                    json.dump(analyzed_data[subject], jf)
        except Exception as e:
            raise Exception("problem in writing analytic data of file_meta_data - analyzer :{}".format(str(e)))

def attr_check(data):
    logs = data
    for subject in data.keys():
        for ln in data[subject].keys():
            try:
                if ('a' in logs[ln]['attributes']) or ('d' in logs[ln]['attributes']) or ('i' in logs[ln]['attributes']) or ('u' in logs[ln]['attributes']):
                    logs[ln]['suspicious'] = True
            except Exception as e:
                raise Exception("problem in analyze attributes of file_meta_data - analyzer :{}".format(str(e)))
    return logs
