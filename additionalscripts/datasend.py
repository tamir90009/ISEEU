import paramiko
import os
import json
import os

def configs():
    try:
        with open('additionalscripts/delivery.conf', 'r') as conf:
            config = json.load(conf)
            return config
    except Exception as e:
        raise Exception("conf file not found " + e)


class MySFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        ''' Uploads the contents of the source directory to the target path. The
            target directory needs to exists. All subdirectories in source are
            created under target.
        '''
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), '%s/%s' % (target, item))
            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        ''' Augments mkdir by adding an option to not fail if the folder exists  '''
        try:
            super(MySFTPClient, self).mkdir(path, mode)
        except Exception as e:
            pass


def datasend(localpath, task_name):

    try:
        # Connecting over Port and ip with data from config file
        conf = configs()
        transport = paramiko.Transport((conf['ip'], int(conf['port'])))
        transport.connect(username=conf['user'], password=conf['pass'])
        sftp = MySFTPClient.from_transport(transport)
        remote_path = os.path.join(conf["remote"], task_name)
        # Directory transport:
        if os.path.isdir(localpath):
            try:
                sftp.mkdir(remote_path, ignore_existing=True)
                sftp.put_dir(localpath, remote_path)
            except Exception as e:
                raise Exception("error while sending a dir " + e)
            sftp.close()
        # File transport
        elif os.path.isfile(localpath):
            #sftp = transport.open_sftp_client()
            try:
                remote_file = os.path.join(remote_path, os.path.basename(localpath))
                sftp.mkdir(remote_path, ignore_existing=True)
                sftp.put(localpath, remote_file)
            except Exception as e:
                raise Exception("error while sending file " + e)
            sftp.close()
        else:
            raise Exception("file not found")
    except Exception as e:
        raise Exception("Error with setting transport " + e)



