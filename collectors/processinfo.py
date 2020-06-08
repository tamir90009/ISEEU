from collectors.collector import Collector
from additionalscripts.all_processes import AllProcesses
import json

class ProcessInfoCollector(Collector):

    '''
    this function will collect all process information using additional script all_processes.py
    as an input it get an output path and returns nothing
    '''
    @staticmethod
    def collect(dst_path):
        try:
            to_json = {}
            all_process = AllProcesses()
            process_list = all_process.collect_all_info()
            for pid in process_list.keys():
                if pid:
                    to_json[pid] = process_list.get(pid).__dict__
            with open("{}.json".format(dst_path), "w") as fp:
                json.dump(to_json, fp, indent=4)


        except Exception as e:
            raise Exception("problem in collect process info :{}".format(str(e)))



