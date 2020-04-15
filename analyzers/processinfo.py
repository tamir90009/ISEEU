from analyzers.analyzer import Analyzer
from os import listdir
from os.path import isfile, join
import json
import re

ANALYTIC_PATH = "analytices"

class ProcessInfoAnalyzer(Analyzer):

    '''
    this func reads a each specific analytic from analytics path and check if the current process is suspicious by
    the logic of the analytic
    '''

    @staticmethod
    def analyze(process_data, analytic_folder_path = ANALYTIC_PATH):
        for pid in process_data:
            onlyfiles = [f for f in listdir(analytic_folder_path) if isfile(join(analytic_folder_path, f))]
            for file in onlyfiles:
                try:
                    with open("{}/{}".format(analytic_folder_path,file), 'r') as fp:
                        analytic_data = json.load(fp)
                        suspicious = False
                        if analytic_data["_operator"] == "OR":
                            suspicious = ProcessInfoAnalyzer.or_check(process_data[pid], analytic_data)
                        elif analytic_data["_operator"] == 'AND':
                            suspicious = ProcessInfoAnalyzer.and_check(process_data[pid], analytic_data)
                        #TODO:send to elastic eahc process object  + suspicious if its true



                except Exception as e:
                    raise Exception("problem in reading analytic  info - analyzer :{}".format(str(e)))
    '''
    this func will check all condition with operator "OR"
    '''
    @staticmethod
    def or_check(process_info,analytic_data):
        try:
            for key in analytic_data:
                if "_analytic_name" not in key and "_comment" not in key and "_operator" not in key:
                    if analytic_data[key] is not None:
                        proc_key = key
                        if not isinstance(process_info[key], str):
                            proc_key = "".join(str(process_info[key]))
                        if "(NOT)" in analytic_data[key]:
                            filtered_value = str(analytic_data[key]).strip("(NOT)")
                            match = re.match(str(filtered_value), proc_key)
                            if match is None:
                                return True
                        else:
                            match = re.match(analytic_data[key], proc_key)
                            if match is not None:
                                return True
            return False
        except Exception as e:
            raise Exception("problem in reading analytic OR operator info - analyzer :{}".format(str(e)))

    '''
    this func will check all the analytic with "AND" operator
    '''
    @staticmethod
    def and_check(process_info,analytic_data):
        try:
            for key in analytic_data:
                if ("_analytic_name" not in key) and ("_comment" not in key) and  ("_operator" not in key) :
                    if analytic_data[key] is not None:
                        proc_key = key
                        if not isinstance(process_info[key], str):
                            proc_key = "".join(str(process_info[key]))
                        if "(NOT)" in analytic_data[key]:
                            filtered_value = str(analytic_data[key]).strip("(NOT)")
                            match = re.match(str(filtered_value), proc_key)
                            if match is not None:
                                return False
                        else:

                            match = re.match(analytic_data[key], proc_key)
                            if match is None:
                                return False


            return True

        except Exception as e:
            raise Exception("problem in reading analytic  AND operator - analyzer :{}".format(str(e)))




#from additionalscripts.process_info import Process

# sp = Process(2)
# sp.set_user("root")
# sp.set_cmdline("ls --hide")
# sp.set_mem(0.4)
# sp.set_networking_internet("1.8.8.9")
# sp.set_networking_unix("1.8.8.1")
# pp=ProcessInfoAnalyzer(None).analyze(sp,"/tmp/analytics")


