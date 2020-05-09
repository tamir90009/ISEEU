from additionalscripts.offlineautomation import run_agent_on_machine
from taskmanager import TaskManager
import os



def main():
    task_manager = TaskManager()
    # task_manager.add_task("LibraryPath")
    # task_manager.add_task("LDPreload")
    # task_manager.execute_all_tasks("/tmp/output")
    # run_agent_on_machine("vm", "/tmp/output")


if __name__ == "__main__":
    main()
