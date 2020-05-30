import paramiko
import os

try:
    with open('delivery.conf','r') as conf:
        config = eval(conf.read())
except Exception as e:
    raise Exception("conf file not found " + e)


class MySFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        ''' Uploads the contents of the source directory to the target path. The
            target directory needs to exists. All subdirectories in source are
            created under target.
        '''
        try:
            for item in os.listdir(source):
                if os.path.isfile(os.path.join(source, item)):
                    self.put(os.path.join(source, item), '%s/%s' % (target, item))
                else:
                    self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                    self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))
        except:
            raise

    def mkdir(self, path, mode=511, ignore_existing=False):
        ''' Augments mkdir by adding an option to not fail if the folder exists  '''
        try:
            super(MySFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise



def datasend(localpath=config['local'],remotepath=config['remote']):

    # Connecting over Port and ip with data from config file
    transport = paramiko.Transport((config['ip'], int(config['port'])))
    transport.connect(username=config['user'], password=config['pass'])
    try:
        sftp = MySFTPClient.from_transport(transport)
        sftp.mkdir(remotepath, ignore_existing=True)
        sftp.put_dir(localpath, remotepath)
        sftp.close()
    except:
        sftp = transport.open_sftp_client()
        remote_file = remotepath + '/' + localpath.split("/")[-1]
        sftp.put(localpath,remote_file)
        sftp.close()


# Can sent Dir/ File
a = datasend("/home/test/HH/blop.txt", "/home/elk/Temp/New" )
