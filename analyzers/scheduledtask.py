from analyzers.analyzer import Analyzer
import json
import socket
import os
from additionalscripts.datasend import datasend

DEST = '/tmp'


class ScheduledTaskAnalyzer(Analyzer):

    '''
    this func save the parsed data of scheduled tasks and save it as json file
    '''
    @staticmethod
    def analyze(scheduled_task_data, dst_path=DEST):
        try:
            with open(os.path.join(dst_path, '{}_scheduledtasks.json'.format(socket.gethostname())), 'w') as jf:
                for line in scheduled_task_data:
                    t=scheduled_task_data[line]['command']
                    if '/tmp' in scheduled_task_data[line]['command'] or '/run' in scheduled_task_data[line]['command']:
                        scheduled_task_data[line]['suspicious']=True
                    else:
                        scheduled_task_data[line]['suspicious'] = False
                    jf.write(json.dumps(scheduled_task_data[line]) + '\n')
            datasend(os.path.join(dst_path, '{}_scheduledtasks.json'.format(socket.gethostname())), 'scheduledtasks')
        except Exception as e:
            raise Exception("problem in writing analytic data of scheduled_task_data - analyzer: {}".format(str(e)))
