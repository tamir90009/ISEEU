from collectors.collector import Collector
import shutil
import os

class ScheduledTaskCollector(Collector):
    '''
    this func coping crontab's folder to destination
    '''
    @staticmethod
    def collect(dst_path):
        try:
            if os.path.exists('{}/crontabs'.format(dst_path)):
                shutil.rmtree('{}/crontabs'.format(dst_path))
            shutil.copytree('/var/spool/cron/crontabs', '{}/crontabs'.format(dst_path))
        except Exception as e:
            raise Exception("problem in coping the crontabs dictionary to destination - collector: {}".format(str(e)))
