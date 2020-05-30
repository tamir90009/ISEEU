import argparse
import json
import os
import re
from additionalscripts.offlineautomation import run_agent_on_machine
from vboxcontroller import VBoxController
from additionalscripts import offlineautomation
from taskmanager import TaskManager
from additionalscripts.write_process_analytic import AnalyticWriter

def argparse_func():
    parser = argparse.ArgumentParser(description='ISEEU main agent')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-esi', '--elastic_ip', help='elastic search ip:port')
    parser.add_argument('-esp', '--elastic_path', help='elastic path to throw data to', required=False)
    parser.add_argument('-esup', '--elastic_username_password', help='elastic search username:password', required=False)
    parser.add_argument('-op', '--output_path', help='output path', required=False)
    parser.add_argument('-tn', '--threads_number', help='max threads number to run the program', default=3, required=False)
    parser.add_argument('-ra', '--run_all', help='run all default tasks', action='store_true', required=False)
    parser.add_argument('-rs', '--run_specific', help='run specific tasks (use \',\' as delimeter)', required=False)
    group.add_argument('-ct', '--crontab', help='add to crontab', default=False)
    parser.add_argument('-ctf', '--crontab_flags', help='crontab flags (have to come with -ct before)', required=False)
    group.add_argument('-vm', '--vmname', help='vmname to run agent on')
    parser.add_argument('-i', '--image', help='HD image to run agent on', required=False)
    parser.add_argument('-in', '--image_name', help='name to name the vm', required=False)
    parser.add_argument('-ip', '--image_path', help='HD image to run agent on path', required=False)
    parser.add_argument('-ir', '--image_format', help='image format raw', action='store_true', required=False)
    parser.add_argument('-ios', '--image_os', help='image os', required=False)
    parser.add_argument('-im', '--image_ram', help='ram to give the machine', default=1024, required=False)
    parser.add_argument('-if', '--image_flags', help='flags to run the agent with at the machine', required=False)
    parser.add_argument('-iap', '--image_agent_path', help='path in the vm to copy the agent to', required=False)

    # analytics args
    group.add_argument('-na', '--new_analytic', help='add analytic', action='store_true', required=False)
    parser.add_argument('-w', '--comment',
                        help='write a comment for your analytic that explain what it checkes and why is that suspicious',
                        required=False)
    parser.add_argument('-N', '--name', help='write a name for the analytic', required=False)
    parser.add_argument('-p', '--pid', help='write  a suspicious pid', required=False)
    parser.add_argument('-P', '--ppid', help='write  a suspicious parent process', required=False)
    parser.add_argument('-j', '--pgid', help='write  a suspicious process group id', required=False)
    parser.add_argument('-q', '--psid', help='write  a suspicious process session id', required=False)
    parser.add_argument('-a', '--memory', help='write  a suspicious memory value', required=False)
    parser.add_argument('-c', '--cpu', help='write  a suspicious cpu value', required=False)
    parser.add_argument('-u', '--user', help='write  a suspicious user name', required=False)
    parser.add_argument('-t', '--tty', help='write  a suspicious tty value', required=False)
    parser.add_argument('-s', '--stat', help='write  a suspicious process stat value', required=False)
    parser.add_argument('-k', '--start', help='write  a suspicious process start value', required=False)
    parser.add_argument('-m', '--time', help='write  a suspicious process time value', required=False)
    parser.add_argument('-l', '--cmdline', help='write  a suspicious process commandline ', required=False)
    parser.add_argument('-e', '--environ', help='write  a suspicious process environ value', required=False)
    parser.add_argument('-n', '--networking_internet', help='write  a suspicious process internet network value',
                        required=False)
    parser.add_argument('-b', '--networking_unix', help='write  a suspicious process unix network value',
                        required=False)
    parser.add_argument('-f', '--file_descriptor', help='write  a suspicious process file_descriptor value',
                        required=False)
    parser.add_argument('-o', '--operator', default='AND', help='write  an operator that will be in the logic between the fields \
             - optional values are AND,OR the default is AND for multiple multiple fields and NONE for a single fields in the analytic')

    return parser.parse_args()


def on_machine(args):
    try:
        VBoxController.disk_image_to_machine(vmname=args.image_name, hard_drive_path=args.image_path,
                                             raw=args.image_format, os_type=args.image_os, memory=args.image_ram)
        pattern = re.compile('-o\s(?P<output_path>(\'.*\'|(\/|\w|\d|\s|\_|\-|\.)*))\s-')
        output_path = pattern.search(args.image_flags).group('output_path')
        run_agent_on_machine(vm_name=args.image_name, output_path=output_path, agent_folder_path=os.getcwd(),
                             agent_flags=args.image_flags, agent_main_file='agent.py',
                             path_in_machine=args.image_agent_path)
    except Exception as e:
        raise e

def main():
    args = argparse_func()
    if args.crontab:
        offlineautomation.add_to_cron(args.crontab_flags)
    # TODO: run on image

    if args.new_analytic:
        try:
            analytic_writer = AnalyticWriter()
            analytic_writer.get_info_from_user()
        except Exception as e:
            raise e

    if args.image:
        on_machine(args)
    else:
        task_manager = TaskManager()
        if args.run_all:
            tasks = ['FileMetaData', 'Log', 'ScheduledTask', 'BinaryList', 'LibraryPath', 'AutoRunPaths', 'ProcessInfo']
            for task in tasks:
                task_manager.add_task(task)
            task_manager.add_task('FileMetaData', True)

        if args.run_specific:
            for task in args.run_specific.replace(' ', '').split(','):
                task_manager.add_task(task)
            
        if args.elastic:
            if ':' in args.elastic:
                es_ip, es_port = args.elastic_ip.split(':')
            else:
                es_ip = args.elastic
                es_port = '9200'
            if not args.elastic_path:
                print("elastic path is missing")
                exit(1)
            remote_path = args.elastic_path
            if not args.elastic_username_password:
                print("elastic username and password is missing")
                exit(1)
            user_name, password = args.elastic_username_password.split(':')
            try:
                elastic_json = {'ip': es_ip, 'port': es_port,  'user': user_name, 'pass': password, 'remote': remote_path}
                with open('delivery.conf', 'w') as fp:
                    json.dump(elastic_json, fp)
            except Exception as e:
                raise e
            #print('dslkfjl')

        else:
            print('elastic info is missing')
            exit(1)

        if args.output_path:
            task_manager.execute_all_tasks(args.output_path, args.threads)

        else:
            print('output path is missing')
            exit(1)


if __name__ == '__main__':
    main()