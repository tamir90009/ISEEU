from collectors.collector import Collector
import shutil


class ScheduledTaskCollector(Collector):

    # this func coping crontab's folder to destination
    @staticmethod
    def collect(dst_path):
        try:
            shutil.copytree('/var/spool/cron/crontabs', '{}/crontabs'.format(dst_path))
        except Exception as e:
            raise Exception("problem in coping the crontabs dictionary to destination - collector: {}".format(str(e)))