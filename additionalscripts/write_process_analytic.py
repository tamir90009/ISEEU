import argparse
import json
import os


'''
this class writes analytics and a cli option to help the user with the writting one
'''

ANALYTICS_PATH = "analytices"

class AnalyticWriter(object):

    def __init__(self):
        self._analytic_name = ""
        self._comment = ""
        self._pid = ""
        self._ppid = ""
        self._pgid = ""
        self._psid = ""
        self._mem = 0
        self._cpu = 0
        self._user = ""
        self._tty = ""
        self._stat = ""
        self._start = ""
        self._time = ""
        self._cmdline = ""
        self._env = ""
        self._list_of_file_descript = []
        self._networking_unix = []
        self._networking_internet = []
        self._operator = ""


    '''
    collect the information from the user for a single analytic and put it in self
    '''
    def get_info_from_user(self,dest_path = ANALYTICS_PATH):
        parser = argparse.ArgumentParser(description="please enter value only to the \
        fields you want in the analytic in PYTHON REGEX , if your analytic include a check - if  one of the fields is empty please \
         put a "" (empty string) value to it,  for logical NOT please add '(NOT)' and then your regex expression")
        parser.add_argument('-w', '--comment',help="write a comment for your analytic that explain what it checkes and why is that suspicious", required=True)
        parser.add_argument('-N', '--name', help="write a name for the analytic", required=True)
        parser.add_argument('-p','--pid', help="write  a suspicious pid", required=False)
        parser.add_argument('-P', '--ppid', help="write  a suspicious parent process", required=False)
        parser.add_argument('-j', '--pgid', help="write  a suspicious process group id", required=False)
        parser.add_argument('-q', '--psid', help="write  a suspicious process session id", required=False)
        parser.add_argument('-a','--memory', help="write  a suspicious memory value", required=False)
        parser.add_argument('-c','--cpu', help="write  a suspicious cpu value", required=False)
        parser.add_argument('-u', '--user', help="write  a suspicious user name", required=False)
        parser.add_argument('-t', '--tty', help="write  a suspicious tty value", required=False)
        parser.add_argument('-s', '--stat', help="write  a suspicious process stat value", required=False)
        parser.add_argument('-k', '--start', help="write  a suspicious process start value", required=False)
        parser.add_argument('-m', '--time', help="write  a suspicious process time value", required=False)
        parser.add_argument('-l', '--cmdline', help="write  a suspicious process commandline ", required=False)
        parser.add_argument('-e', '--environ', help="write  a suspicious process environ value", required=False)
        parser.add_argument('-n', '--networking_internet', help="write  a suspicious process internet network value", required=False)
        parser.add_argument('-b', '--networking_unix', help="write  a suspicious process unix network value", required=False)
        parser.add_argument('-f', '--file_descriptor', help="write  a suspicious process file_descriptor value", required=False)
        parser.add_argument('-o', '--operator',default="AND", help="write  an operator that will be in the logic between the fields \
         - optional values are AND,OR the default is AND for multiple multiple fields and NONE for a single fields in the analytic")


        args = parser.parse_args()
        # print(args.network,"what")
        try:
            self._comment = args.comment
            self._analytic_name = args.name
            self._pid = args.pid
            self._ppid = args.ppid
            self._pgid = args.pgid
            self._psid = args.psid
            self._mem = args.memory
            self._cpu = args.cpu
            self._user = args.user
            self._tty = args.tty
            self._stat = args.stat
            self._start = args.start
            self._time = args.time
            self._cmdline = args.cmdline
            self._env = args.environ
            self._networking_unix = args.networking_unix
            self._networking_internet = args.networking_internet
            self._list_of_file_descript = args.file_descriptor
            self._operator = args.operator


        except Exception as e:
            print("problem in user input for an analytic ,func - get info from user :{}".format(e))

        try:
            self.write_analytic_json(dest_path)
        except Exception as es:
            print(es)

    '''
    this func will write the analytic the user want to add to a yml file for the program to parse 
    '''
    def write_analytic_json(self,dst_path = ANALYTICS_PATH):
        try:
            with open(os.path.join(dst_path,self._analytic_name),"w") as fp:
                to_json  = self.__dict__
                json.dump(to_json, fp, indent=4)
        except Exception as e:
            raise Exception("problem in dumping new analytic to file :{}.".format(str(e)))

