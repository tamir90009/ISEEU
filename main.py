from taskmanager import TaskManager
from additionalscripts.datasend import send_folder_to_Sender



def main():
    task_manager = TaskManager()
    task_manager.add_task("FileMetaData")
    task_manager.add_task("Log")
    task_manager.add_task("ScheduledTask")
    task_manager.add_task("BinaryList")
    #task_manager.add_task("LibraryPath")
    task_manager.add_task("AutoRunPaths")
    task_manager.add_task("ProcessInfo")
    task_manager.add_task("SystemInfo")
    task_manager.execute_all_tasks("/tmp/test10")

    send_folder_to_Sender('/home/shachar/test10/to_datasender/')

if __name__ == "__main__":
    main()



