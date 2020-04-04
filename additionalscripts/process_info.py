
'''

this class represents a dingle process object with full info collected
'''
class Process(object):

    def __init__(self, pid):
        self._pid = pid
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


    '''
    env param setter
    '''
    def set_env(self, env):
        self._env = env

    '''
    env param getter
    '''
    def get_env(self):
        return self._env

    '''
    mem param setter
    '''

    def set_mem(self, mem):
        self._mem = mem

    '''
    mem param getter
    '''

    def get_mem(self):
        return self._mem


    '''
    cpu param setter
    '''

    def set_cpu(self, cpu):
        self._cpu = cpu

    '''
    cpu param getter
    '''

    def get_cpu(self):
        return self._cpu


    '''
    user param setter
    '''

    def set_user(self, user):
        self._user = user

    '''
    user param getter
    '''

    def get_user(self):
        return self._user

    '''
    tty param setter
    '''

    def set_tty(self, tty):
        self._tty = tty

    '''
    tty param getter
    '''

    def get_tty(self):
        return self._tty
    '''
    stat param setter
    '''

    def set_stat(self, stat):
        self._stat = stat

    '''
    stat param getter
    '''

    def get_stat(self):
        return self._stat


    '''
    start param setter
    '''

    def set_start(self, start):
        self._start = start

    '''
    start param getter
    '''

    def get_start(self):
        return self._start

    '''
    time param setter
    '''

    def set_time(self, time):
        self._time = time

    '''
    time param getter
    '''

    def get_time(self):
        return self._time


    '''
    cmdline param setter
    '''

    def set_cmdline(self, cmdline):
        self._cmdline = cmdline

    '''
    cmdline param getter
    '''

    def get_cmdline(self):
        return self._cmdline

    '''
    list_of_file_descript param setter
    '''

    def set_list_of_file_descript(self, list_of_file_descript):
        self._list_of_file_descript.append(list_of_file_descript)

    '''
    list_of_file_descript param getter
    '''

    def get_list_of_file_descript(self):
        return self._list_of_file_descript


    '''
    networking_internet param setter
    '''

    def set_networking_internet(self, networking):
        self._networking_internet.append(networking)

    '''
    networking_internet param getter
    '''

    def get_networking_internet(self):
        return self._networking_internet

    '''
    networking_unix param setter
    '''

    def set_networking_unix(self, networking):
        self._networking_unix.append(networking)

    '''
    networking_unix param getter
    '''

    def get_networking_unix(self):
        return self._networking_unix
    '''
    networking param setter
    '''

    def set_networking(self, networking):
        self._networking = networking

    '''
    networking param getter
    '''

    def get_networking(self):
        return self._networking

    def get_pid(self):
        return self._pid

    def get_process(self):
        return self

    def print_pid(self):
        print(self.get_pid(), self.get_user(), self.get_cmdline(), self.get_cpu(), self.get_mem(), self.get_tty(),
              self.get_stat(), self.get_start(), self.get_time(), self.get_networking_internet(),
              self.get_networking_unix(), self.get_list_of_file_descript())

