import subprocess as sub

CLAMAV = 'CLA'

class AVScanCollector:

    def __init__(self):
        self.header = CLAMAV
    def avclam_scan(self):
        try:
            p = sub.Popen([r"clamscan -r /home"] ,stdout=sub.PIPE ,stderr=sub.PIPE ,stdin=sub.PIPE ,shell=True)
            out, err = p.communicate()
            if err:
                if "not found" in str(err):
                    raise Exception("Chip not installed")
            if out:
            #   print(out)
                self.parser(self.header, out)
        except:
            raise Exception("Error: Cant run ClamScan")