from taskmanager import TaskManager


def main():
    task_manager = TaskManager()
    task_manager.add_task("LibraryPath")
    task_manager.execute_all_tasks("fsdjhg")

if __name__ == "__main__":
    main()