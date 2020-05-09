from collectors.collector import Collector
import shutil
import os


class LogCollector(Collector):

    # this func coping the log files to destination
    @staticmethod
    def collect(dst_path):
        try:
            os.mkdir(dst_path)
            shutil.copyfile('/var/log/auth.log', '{}/auth.log'.format(dst_path))
            shutil.copyfile('/var/log/syslog', '{}/syslog'.format(dst_path))
        except Exception as e:
            raise Exception("problem in coping the log files to destination - collector: {}".format(str(e)))


