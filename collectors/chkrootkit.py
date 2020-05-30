import subprocess as sub
from collectors.collector import Collector


class CHKRootkitCollector(Collector):

    @staticmethod
    def collect(dst_path):
        try:
            p = sub.Popen(["chkrootkit"], stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE, shell=True)
            out, err = p.communicate()
            if err:
                if "not found" in str(err):
                    raise Exception("ckrootkit not installed " + err)
            if out:
                with open("{}.json".format(dst_path), "w") as fp:
                    fp.write('\n'.join(out.decode('utf-8')))
        except Exception as e:
            raise Exception("Cant run chkrootkit " + e)

