import subprocess as sub

RKHUNTER = 'RKH'

class RKHunter:

    def __init__(self):
        self.header = RKHUNTER

    def rkhunter_scan(self):
        try:
            p = sub.Popen(["rkhunter -c"], stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE, shell=True)
            out, err = p.communicate()
            if err:
                if "not found" in str(err):
                    raise Exception("rkhunter not installed")
            if out:
                self.parser(self.header, out)
        except Exception as e:
            raise Exception(e)