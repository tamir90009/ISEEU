import grp
import platform
import pwd
from collectors.collector import Collector
import subprocess
import json

class SystemInfoCollector(Collector):

    '''

    this func will collect system information
    as an input it will get a  destination path for the out put
    dosent return any thing
    it will write the collected data to the path 
    '''
    @staticmethod
    def collect(dst_path):
        try:
            data = {}
            system_arch = platform.architecture()[0]
            data['architecture'] = system_arch
            system_host_name = platform.node()
            data['host_name'] = system_host_name
            kernel_version = platform.uname()[2]
            data['kernel_version'] = kernel_version
            data['distribution'] = SystemInfoCollector.get_distribution()
            data['users'] = []
            for p in pwd.getpwall():
                data['users'].append({
                    'user_name': p[0],
                    'user_id':p[2],
                    'user_groups':grp.getgrgid(p[3])[0]})
            groups = grp.getgrall()
            data['groups'] = []
            for group in groups:
                data['groups'].append({
                    'group_id' : group[2],
                    'group_name' : group [0]
                })

            with open("{}.json".format(dst_path), 'w') as outfile:
                json.dump(data, outfile)
        except Exception as e:
            print("problem in system info collector - collect :".format(str(e)))


    '''
    this func will extract the os distribution
    it takes no input
    and return the os distribution 
    '''
    @staticmethod
    def get_distribution():
        try:
            cmd = subprocess.check_output(["lsb_release", "-a"], stderr=subprocess.STDOUT, timeout=10)
            output_divided = cmd.decode('utf-8').splitlines()
            system_dist = str(output_divided[2]).split("\t")[1:]
            return system_dist
        except subprocess.CalledProcessError as e:
            raise Exception(e.output)
        except Exception as m:
            raise Exception("problem in system info collector - collect subprocess :{}  ".format(str(m)))


pp = SystemInfoCollector()
pp.collect("/tmp/systeminfo")