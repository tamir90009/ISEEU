from crontab import CronTab

from additionalscripts.offlineautomation import run_agent_on_machine
from taskmanager import TaskManager
import os

def add_to_cron(args):
    try:
        username = os.getenv("USER")
        cron = CronTab(user=username)
        main_path = os.path.abspath(__file__)
        job = cron.new(command=main_path + " " + args)
        job.minute.on(0)
        job.hour.on(8)
        cron.write()
    except Exception as e:
        raise e

def main():
    task_manager = TaskManager()
    # task_manager.add_task("LibraryPath")
    # task_manager.add_task("LDPreload")
    # task_manager.execute_all_tasks("/tmp/output")
    # run_agent_on_machine("vm", "/tmp/output")


if __name__ == "__main__":
    main()
