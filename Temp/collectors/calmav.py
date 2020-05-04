import subprocess as sub
from collectors.collector import Collector

class AVScanCollector(Collector):

    @staticmethod
    def collect(dst_path):
        try:
            p = sub.Popen([r"clamscan -r /home/test/Downloads"] ,stdout=sub.PIPE ,stderr=sub.PIPE ,stdin=sub.PIPE ,shell=True)
            out, err = p.communicate()
            if err:
                if "not found" in str(err):
                    raise Exception("Chip not installed")
            if out:
                with open("{}.json".format(dst_path), "w") as fp:
                    fp.write('\n'.join(out.decode('utf-8')))
        except Exception as e:
            raise Exception("Cant run ClamScan")
