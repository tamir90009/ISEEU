import importlib
import os


class TaskManager(object):
    _tasks = []

    def add_task(self, task_name):
        """
        :param task_name: Camal case task name example LibraryPath
        :return:
        """
        if task_name not in self._tasks:
            self._tasks.append(task_name)
        else:
            raise Exception("Task already in the task manager")

    @staticmethod
    def __execute_task(task_name, output_path):
        # collect
        try:
            task_collector_module = importlib.import_module("collectors." + task_name.lower())
        except ModuleNotFoundError:
            raise Exception("Couldn't find collector name %s" % (task_name))
        try:
            task_collector = getattr(task_collector_module, task_name + "Collector")
        except AttributeError:
            raise Exception("Couldn't find %sCollector in module %s" % (task_name, task_name.lower()))
        try:
            collect(output_path + "\\" + task_name)
        except Exception as e:
            raise e

        # parse
        try:
            task_parser_module = importlib.import_module("parsers." + task_name.lower())
        except ModuleNotFoundError:
            raise Exception("Couldn't find parser name %s" % (task_name))
        try:
            task_parser = getattr(task_parser_module, task_name + "Parser")
        except AttributeError:
            raise Exception("Couldn't find %sParser in module %s" % (task_name, task_name.lower()))
        try:
            parsed_data = task_parser.parse(output_path + "\\" + task_name)
        except Exception as e:
            raise e
        # analyze
        try:
            task_analyzer_module = importlib.import_module("analyzers." + task_name.lower())
        except ModuleNotFoundError:
            raise Exception("Couldn't find analyzer name %s" % (task_name))
        try:
            task_analyzer = getattr(task_analyzer_module, task_name + "Analyzer")
        except AttributeError:
            raise Exception("Couldn't find %sAnalyzer in module %s" % (task_name, task_name.lower()))
        try:
            analyzed_data = task_analyzer.analyze(parsed_data)
        except Exception as e:
            raise e
        # senddata
        # todo:add send data


        print("finish " + task_name)
        return True

    def execute_all_tasks(self, output_path):

        failed = []
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        for task in self._tasks:
            try:
                self.__execute_task(task,output_path)
            except KeyboardInterrupt:
                exit()
            except Exception as e:
                print(f"\033[91m"+ task + ": " + str(e) + f"\033[0m")
                failed.append(task)

        print("finish all")
        if failed:
            print("failed with %s" % (",".join(failed)))
