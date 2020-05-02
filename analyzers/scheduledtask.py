from analyzers.analyzer import Analyzer
import json
import socket


class ScheduledTaskAnalyzer(Analyzer):

    # this func save the parsed data of scheduled tasks and save it as json file
    @staticmethod
    def analyze(self, dst_path, scheduled_task_data):
        try:
            with open('{}/{}_scheduled_tasks.json'.format(dst_path, socket.gethostname()), 'w') as jf:
                json.dump(scheduled_task_data, jf)
        except Exception as e:
            raise Exception("problem in writing analytic data of scheduled_task_data - analyzer: {}".format(str(e)))
