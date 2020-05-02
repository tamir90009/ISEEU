from taskmanager import TaskManager


def main():
    task_manager = TaskManager()
    #task_manager.add_task("ProcessInfo")
    #task_manager.add_task("Log")
    task_manager.add_task("ScheduledTask")
    #task_manager.add_task("BinaryList")
    #task_manager.add_task("LibraryPath")
    #task_manager.add_task("LDPreload")
    task_manager.execute_all_tasks("/tmp/test9")

if __name__ == "__main__":
    main()