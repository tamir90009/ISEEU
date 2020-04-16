import subprocess as sub

MALDET = 'MAD'


class MalDetScan:

    def __init__(self):
        self.header = MALDET

    def maldet_scan(self):
        try:
            p = sub.Popen(["maldet -a /home --log"], stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE, shell=True)
            out, err = p.communicate()
            if err:
                if "not found" in str(err):
                    raise Exception("maldet not installed")

            if out:
                self.parser(self.header, out)
        except Exception as e:
            raise Exception(e)