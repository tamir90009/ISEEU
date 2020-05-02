from vboxcontroller import VBoxController
import os
from shutil import copyfile, copytree
import subprocess
from time import sleep


def insert_agent_to_vm(vm_name, agent_folder_path, mount_path=None, controller=None, path_in_machine="/tmp/agent"):
    try:
        if controller is None:
            controller = VBoxController()
        controller.mount_files_from_machine(vm_name, mount_path)
        if mount_path is None:
            mount_path = "/mnt/" + vm_name
        dst_path_by_host = mount_path + path_in_machine
        initd_file_name = "agent-automation"
        copytree(agent_folder_path, dst_path_by_host)
        initd_path = mount_path + "/etc/init.d"
        initd_full_path = initd_path + "/" + initd_file_name
        copyfile("additionalscripts/agent-automation", initd_full_path)
        subprocess.check_output(["chmod", "755", initd_full_path])
        subprocess.check_output(["chown", "root", initd_full_path])
        os.symlink(initd_path + "/" + initd_file_name, mount_path + "/etc/rc2.d/S01" + initd_file_name)
        os.symlink(initd_path + "/" + initd_file_name, mount_path + "/etc/rc3.d/S01" + initd_file_name)
        os.symlink(initd_path + "/" + initd_file_name, mount_path + "/etc/rc4.d/S01" + initd_file_name)
        os.symlink(initd_path + "/" + initd_file_name, mount_path + "/etc/rc5.d/S01" + initd_file_name)
        raise Exception("all good")
    except Exception as e:
        controller.umount_files_from_machine(vm_name, mount_path)
        print(str(e))

def run_agent_on_machine(vm_name, output_path, agent_folder_path, mount_path=None, controller=None, path_in_machine=None,
                       agent_main_file="main.py"):
    try:
        if controller is None:
            controller = VBoxController()
        controller.mount_files_from_machine(vm_name, mount_path)
        if mount_path is None:
            mount_path = "/mnt/" + vm_name
        insert_agent_to_vm(vm_name, agent_folder_path, controller=controller, agent_main_file=agent_main_file,
                           path_in_machine=path_in_machine)
        controller.start(vm_name)
        sleep(10)
        controller.mount_files_from_machine(vm_name, mount_path=mount_path, read_only=True)
        sleep(10)
        flag = True
        counter = 1
        while flag:
            try:
                if counter % 5 == 0:
                    controller.umount_files_from_machine(vm_name, mount_path)
                    sleep(2)
                    controller.mount_files_from_machine(vm_name, mount_path)
                open(mount_path + output_path + "finish")
                flag = False
            except:
                sleep(10)
                counter += 1

        #add the output agent path to be copy to the machine
        #copytree(agent_folder_path, dst_path_by_host)
        controller.stop(vm_name)
        raise Exception("all good")
    except Exception as e:
        controller.umount_files_from_machine(vm_name, mount_path)
        print(str(e))
