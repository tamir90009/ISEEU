import subprocess as sub

CKROOTKIT = 'CKR'

class CHKrootkit:

    def __init__(self):
        self.header = CKROOTKIT

    def chkrootkit_scan(self):
        try:
            p = sub.Popen(["chkrootkit"], stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE, shell=True)
            out, err = p.communicate()
            if err:
                if "not found" in str(err):
                    raise Exception("ckrootkit not installed")
            if out:
                self.parser(self.header, out)
        except Exception as e:
            raise Exception(e)