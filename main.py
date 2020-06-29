from taskmanager import TaskManager


def main():
    task_manager = TaskManager()
    #task_manager.add_task("FileMetaData")
    #task_manager.add_task("Log")
    #task_manager.add_task("ScheduledTask")
    #task_manager.add_task("BinaryList")
    #task_manager.add_task("LibraryPath")
    #task_manager.add_task("AutoRunPaths")
    #task_manager.add_task("ProcessInfo")
    task_manager.add_task("CHKRootkit")
    task_manager.add_task(("HiddenFiles"))
    task_manager.add_task(("RKHunter"))
    #task_manager.add_task("MalDet")
    #task_manager.add_task("ClamAV")
    #task_manager.add_task("SystemInfo")
    task_manager.execute_all_tasks("/tmp/test3")

if __name__ == "__main__":
    main()



