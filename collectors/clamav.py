import subprocess as sub
from collectors.collector import Collector
import json

class ClamAVCollector(Collector):

    @staticmethod
    def collect(dst_path):
        try:
            p = sub.Popen([r'clamscan -r /home'] ,stdout=sub.PIPE ,stderr=sub.PIPE ,stdin=sub.PIPE ,shell=True)
            out, err = p.communicate()
            if err:
                if "not found" in str(err):
                    raise Exception("Chip not installed " + str(err))
            if out:
                with open("{}".format(dst_path), "w") as fp:
                    for line in out.decode('utf-8').splitlines():
                        fp.write(line + '\n')
        except Exception as e:
            raise Exception("Cant run ClamScan " + str(e))
