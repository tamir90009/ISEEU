from analyzers.analyzer import Analyzer
import json


class ScheduledTaskAnalyzer(Analyzer):

    # this func save the parsed data of scheduled tasks and save it as json file
    @staticmethod
    def analyze(self, dst_path, scheduled_task_data, analytic_folder_path):
        try:
            with open('{}/{}/scheduled_tasks.json'.format(dst_path, analytic_folder_path), 'w') as jf:
                json.dump(scheduled_task_data, jf)
        except Exception as e:
            raise Exception("problem in writing analytic data of scheduled_task_data - analyzer: {}".format(str(e)))
