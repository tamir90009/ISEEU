import paramiko

try:
    with open('delivery.conf','r') as conf:
        config = eval(conf.read())
except Exception as e:
    raise Exception("conf file not found " + e)


def datasend(localpath,remotepath):
    try:
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(config['ip'], username =config['user'], password =config['pass'],port=int(config['port']))
        except Exception as e:
            raise Exception("error with the ssh client... " + e)
        try:
            sftp = ssh_client.open_sftp()
            sftp.put(str(localpath), str(remotepath))
            sftp.close()
            ssh_client.close()
        except Exception as e:
            raise Exception("error with the sftp client... " + e)
    except Exception as e:
        raise Exception(e)


a = datasend("/home/test/Temp/hiddenfiles.txt", "/home/elk/Temp/hiddenfile.txt" )
