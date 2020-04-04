from collectors.collector import Collector
from additionalscripts.process_info import Process
from additionalscripts.all_processes import AllProcesses
import json

class ProcessInfoCollector(Collector):


    @staticmethod
    def collect(dst_path):
        try:
            with open(dst_path,"w") as fp:
                to_json={}
                all_process = AllProcesses()
                process_list = all_process.collect_all_info()
                for pid in process_list.keys():
                    to_json[pid] = process_list.get(pid).__dict__

                json.dump(to_json, fp, indent=4)


        except Exception as e:
            raise Exception("problem in collect process info :{}.".format(str(e)))

pp=ProcessInfoCollector.collect("/tmp/process_info.json")

