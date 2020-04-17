from taskmanager import TaskManager
from vboxcontroller import VBoxController
import os
from shutil import copyfile, copytree

def insert_agent_to_vm(vm_name, agent_folder_path, mount_path=None, controller=None, path_in_machine="/tmp/agent",
                       agent_main_file="main.py", agent_arguments=None):
    try:
        if controller is None:
            controller = VBoxController()
        controller.mount_files_from_machine(vm_name, mount_path)
        if mount_path is None:
            mount_path = "/mnt/" + vm_name
            dst_path_by_host = mount_path + path_in_machine
        else:
            dst_path_by_host = mount_path + path_in_machine
        # os.makedirs(dst_path_by_host, exist_ok=True)
        copytree(agent_folder_path, dst_path_by_host)
        crontab_path = mount_path + "/var/spool/cron/crontabs"
        os.makedirs(crontab_path, exist_ok=True)
        with open(crontab_path + "/root", "a+") as cronfile:
            # cronjob = "@reboot sudo python3 " + path_in_machine + "/" + agent_main_file + " " + agent_arguments + "\n"
            cronjob = "@reboot mkdir /test\n"
            cronfile.write(cronjob)

        raise Exception("all good")

    except Exception as e:
        controller.umount_files_from_machine(vm_name, mount_path)
        print(str(e))

def main():
    # task_manager = TaskManager()
    # task_manager.add_task("LibraryPath")
    # task_manager.add_task("LDPreload")
    # task_manager.execute_all_tasks("/tmp/output")
    insert_agent_to_vm("vm", "/home/test/Desktop/test")


if __name__ == "__main__":
    main()
