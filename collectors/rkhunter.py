import subprocess as sub
from collectors.collector import Collector


class RKHunterCollector(Collector):

    @staticmethod
    def collect(dst_path):
        try:
            p = sub.Popen(["rkhunter -c"], stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE, shell=True)
            out, err = p.communicate()
            if err:
                if "not found" in str(err):
                    raise Exception("rkhunter not installed " + err)
            if out:
                with open("{}".format(dst_path), "w") as fp:
                    for line in out.decode('utf-8').splitlines():
                        fp.write(line + '\n')
        except Exception as e:
            raise Exception("cant run rkhunter " + str(e))

