import io

from additionalscripts.process_info import Process
import subprocess

LSOF_COLUMNS = 11
NETSTAT_INTERNET_COLUMNS = 10
NETSTAT_UNIX_COLUMNS = 8
PS_COLUMNS = 10
TRACE_COMM_COLUMNS = 1

'''
this class represent a list of process and collects each process information from the os .
'''


class AllProcesses(object):

    def __init__(self):
        self._processDic = {}

    '''
    this func will enable and activate all collectors , put info in a single process object
    and print all sub objects of this list
    :return the whole object 
    '''

    def collect_all_info(self):
        self.ps_reader()
        self.ps_relations()
        self.netstat_reader()
        self.parse_pid_env()
        self.parse_lsof_command()
        return self.get_all_process()

    '''
    this func will print all processes info from the system
    [pid,user,cmdline,cpu,memeory,tty,stat,start,time,[internet_network],[unix_network],[file descriptors]]
    '''

    def print_object(self):
        try:
            for pid in self._processDic:
                self._processDic.get(pid).print_pid()
        except KeyError as error:
            raise KeyError(error)
        except Exception as e:
            raise Exception("problem while printing %s" % str(e))

    '''
       this part will parse 'ps -aux' command  out put to  10 coulmns 
       ["'USER", 'PID', '%CPU', '%MEM', 'VSZ', 'RSS', 'TTY', 'STAT', 'START', 'TIME', "COMMAND'"]
    '''

    def ps_reader(self):
        try:
            output = self.command_exec("ps -aux")
            for row in output:
                pid = int(row.split(None, PS_COLUMNS)[1])
                self._processDic.update({pid: Process(pid)})
                fields = len(row.split(None, PS_COLUMNS))
                if self._processDic.get(pid, None):
                    self._processDic.get(pid).set_user(row.split(None, fields)[0])
                    self._processDic.get(pid).set_cpu(row.split(None, fields)[PS_COLUMNS - 8])
                    self._processDic.get(pid).set_mem(row.split(None, fields)[PS_COLUMNS - 7])
                    self._processDic.get(pid).set_tty(row.split(None, fields)[PS_COLUMNS - 4])
                    self._processDic.get(pid).set_stat(row.split(None, fields)[PS_COLUMNS - 3])
                    self._processDic.get(pid).set_start(row.split(None, fields)[PS_COLUMNS - 2])
                    self._processDic.get(pid).set_time(row.split(None, fields)[PS_COLUMNS - 1])
                    self._processDic.get(pid).set_cmdline(" ".join(row.split(None, fields)[PS_COLUMNS:]))

        except KeyError as error:
            raise KeyError(error)

        except Exception as e:
            raise Exception("problem while ps_read %s" % (str(e)))


    '''
    this func will add each process the parent  process, process group id , and process session id
    '''
    def ps_relations(self):
        try:
            output = self.command_exec("ps -fj")
            for row in output:
                pid = int(row.split(None, PS_COLUMNS)[1])
                fields = len(row.split(None, PS_COLUMNS))
                if self._processDic.get(pid, None):
                    parent_cmdline = self._processDic.get(int(row.split(None, fields)[2])).get_cmdline()
                    self._processDic.get(pid).set_parent_cmdline(parent_cmdline)
                    self._processDic.get(pid).set_ppid(int(row.split(None, fields)[2]))
                    self._processDic.get(pid).set_pgid(int(row.split(None, fields)[3]))
                    self._processDic.get(pid).set_psid(int(row.split(None, fields)[4]))
        except Exception as e:
            raise Exception("problem while using process relation reader func %s" % (str(e)))


    '''
    this func parse the out put of 'netstat -nalp' command to
    first part - Active internet connection
    second part -Active UNIX domain sockets
    '''

    def netstat_reader(self):
        try:
            output = self.command_exec("netstat -napl")
            second_part_flag = 0
            for row in output[1:]:
                if "Active UNIX domain" in row or "Proto" in row:
                    second_part_flag = 1
                elif second_part_flag == 0:
                    self.netstat_active_domain(row)
                else:
                    self.netstat_unix_domain(row)
        except KeyError as error:
            raise error
        except TypeError as tp:
            raise tp
        except Exception as e:
            raise Exception("problem while using netstat reader func %s" % (str(e)))

    '''
    netsat secend part -Active UNIX domain sockets
    [Proto ,RefCnt Flags, Type , State , I-Node  ,PID/Program name , Path]
    
    '''

    def netstat_unix_domain(self, row):
        try:
            fields = len(row.split(None, NETSTAT_UNIX_COLUMNS))
            if "/" in row:
                if fields < NETSTAT_UNIX_COLUMNS:
                    pid = int((row.split(None, fields)[fields - 1]).split("/")[0])
                    if self._processDic.get(pid, None):
                        self._processDic.get(pid).set_networking_unix(row.split(None, fields)[:fields - 1])
                else:
                    pid = int((row.split(None, fields)[fields - 2]).split("/")[0])
                    if self._processDic.get(pid, None):
                        self._processDic.get(pid).set_networking_unix(row.split(None, fields)[:fields - 2])

        except KeyError as error:
            raise KeyError(error)
        except Exception as e:
            raise Exception("problem while using netat unix domain %s" % str(e),row)

    '''
    netstat first part parse - Active internet connection
    [Proto ,Recv-Q ,Send-Q ,Local Address ,Foreign Address , State ,PID/Program name]
    '''

    def netstat_active_domain(self, row):
        try:
            fields = len(row.split(None, NETSTAT_INTERNET_COLUMNS))
            if "/" in row:
                if "--type=" in row or ": r" in row:
                    pid = int((row.split(None, fields)[fields - 2]).split("/")[0])
                    if self._processDic.get(pid, None):
                        self._processDic.get(pid).set_networking_internet(row.split(None, fields)[:fields - 2])
                else:
                    pid = int((row.split(None, fields)[fields -1]).split("/")[0])
                    if self._processDic.get(pid, None):
                        self._processDic.get(pid).set_networking_internet(row.split(None, fields)[:fields - 1])

        except KeyError as error:
            raise error
        except Exception as e:
            raise Exception("problem in netstat active domains:{},in row:{}".format(str(e), row))

    '''
    this func parse the /proc/[pid]/env file for each process and add it to the process object
    '''

    def parse_pid_env(self):
        for pid in self._processDic.keys():
            if self.is_accessible("/proc/{}/environ".format(pid)):
                try:
                    f = open("/proc/{}/environ".format(pid), 'r')
                    pid_env = f.read()
                    if pid_env != "" and self._processDic.get(pid, None):
                        self._processDic.get(pid).set_env(pid_env)
                    if self._processDic.get(pid, None):
                        f.close()
                    else:
                        raise ValueError("None value in single process object")
                except IOError:
                    raise IOError.args

    '''
    this func will parse the information from the 'lsof -nPR' command to find all process file descriptors in use and 
    put it in the specific process object
    '''

    def parse_lsof_command(self):
        try:
            output = self.command_exec("lsof -nRP")
            for row in output[2:]:
                # ignore command warnings
                if 'lsof:' not in row and 'Output information may be incomplete.' not in row \
                        and not row.startswith('COMMAND'):
                    pid = ""
                    try:
                        pid = int(row.split(None, LSOF_COLUMNS)[1])
                    except Exception as e:
                        raise Exception("problem in parse lsof command - all_process  :{}".format(str(e)))
                    split_row = row.split(None, LSOF_COLUMNS)
                    split_row_len = len(split_row)
                    fd = [split_row[split_row_len - 6], split_row[split_row_len - 5], split_row[split_row_len - 4],
                          split_row[split_row_len - 3], split_row[split_row_len - 2], split_row[split_row_len - 1]]
                    if pid in self._processDic:
                        self._processDic.get(pid).set_list_of_file_descript(fd)
        except KeyError as error:
            raise error
        except Exception as e:
            raise Exception("problem in parse  lsof  command :{}".format(str(e)))



    '''
    get all pids 
    '''
    def get_pids(self):
        return self._processDic.keys()

    '''
    this func returns the all process list object
    '''
    def get_all_process(self):
        return self._processDic


    '''
    this func will execute os commands 
    '''
    @staticmethod
    def command_exec(command):
        try:
            parsed_command = command.split(" ")
            cmd = subprocess.check_output(parsed_command, stderr=subprocess.STDOUT, timeout=30)
            output_divided = cmd.decode('utf-8').splitlines()
            return output_divided[1:]
        except KeyError as error:
            raise error
        except subprocess.TimeoutExpired as e:
            print(str(e))
            return []
        except Exception as e:
            raise e

    """
    Check if the file or directory at `path` can
    be accessed by the program using `mode` open flags.
    """

    @staticmethod
    def is_accessible(path, mode='r'):
        try:
            with open(path, mode) as f:
                f.read()
        except IOError:
            return False
        return True
