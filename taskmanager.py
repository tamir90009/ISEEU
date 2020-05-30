import importlib
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


class TaskManager(object):
    _tasks = []

    def add_task(self, task_name, last=False):
        """
        add task to to the task list
        :param task_name: Camel case task name example LibraryPath
               last: when to run the task at the beginning or at the end
        :return:
        """
        if task_name not in self._tasks:
            self._tasks.append([task_name, last])
        else:
            raise Exception("Task already in the task manager")

    @staticmethod
    def __execute_task(task_name, output_path=None):
        """
        execute a task, first look for his collector, then his parser and at the end his analyzer
        :param task_name: Camel case task name example LibraryPath
        :return:
        """
        to_datasender_path = output_path + "/to_datasender"
        os.makedirs(to_datasender_path, exist_ok=True)
        # collect
        try:
            task_collector_module = importlib.import_module("collectors." + task_name.lower())
        except ModuleNotFoundError:
            raise Exception("Couldn't find collector name %s" % task_name)
        try:
            task_collector = getattr(task_collector_module, task_name + "Collector")
        except AttributeError:
            raise Exception("Couldn't find %sCollector in module %s" % (task_name, task_name.lower()))
        try:
            task_collector.collect(output_path + "/" + task_name)
        except Exception as e:
            raise Exception("%s collector - %s" % (task_name, str(e)))

        # parse
        try:
            task_parser_module = importlib.import_module("parsers." + task_name.lower())
        except ModuleNotFoundError:
            raise Exception("Couldn't find parser name %s" % task_name)
        try:
            task_parser = getattr(task_parser_module, task_name + "Parser")
        except AttributeError:
            raise Exception("Couldn't find %sParser in module %s" % (task_name, task_name.lower()))
        try:
            parsed_data = task_parser.parse(output_path + "/" + task_name)
        except Exception as e:
            raise Exception("%s parser - %s" % (task_name, str(e)))
        # analyze
        try:
            task_analyzer_module = importlib.import_module("analyzers." + task_name.lower())
        except ModuleNotFoundError:
            raise Exception("Couldn't find analyzer name %s" % task_name)
        try:
            task_analyzer = getattr(task_analyzer_module, task_name + "Analyzer")
        except AttributeError:
            raise Exception("Couldn't find %sAnalyzer in module %s" % (task_name, task_name.lower()))
        try:
            task_analyzer.analyze(parsed_data, to_datasender_path)
        except Exception as e:
            raise Exception("%s analyzer - %s" % (task_name, str(e)))
        # senddata
        # try:
        #     task_data_sender_module = importlib.import_module("datasenders." + task_name.lower())
        # except ModuleNotFoundError:
        #     raise Exception("Couldn't find data sender name %s" % task_name)
        # try:
        #     task_data_sender = getattr(task_data_sender_module, task_name + "DataSender")
        # except AttributeError:
        #     raise Exception("Couldn't find %DataSender in module %s" % (task_name, task_name.lower()))
        # try:
        #     task_data_sender.sendData(to_datasender_path)
        # except Exception as e:
        #     raise e

        print("finish " + task_name)
        return True

    def execute_all_tasks(self, output_path, threads=3):
        """
        submit all the tasks to execute
        :param output_path: path to dump all the collected data
               threads: how many threads to run
        :return:
        """
        failed = []
        os.makedirs(output_path + "/to_datasender", exist_ok=True)
        results = {}
        later = []
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for task, last in self._tasks:
                if last:
                    later.append(task)
                results[task] = executor.submit(self.__execute_task, task, output_path)

            for task in results:
                try:
                    results[task].result()
                except KeyboardInterrupt:
                    exit()
                except Exception as e:
                    print(f"\033[91m" + task + ": " + str(e) + f"\033[0m")
                    failed.append(task)

            for task in later:
                    results[task] = executor.submit(self.__execute_task, task, output_path)

            for task in results:
                try:
                    results[task].result()
                except KeyboardInterrupt:
                    exit()
                except Exception as e:
                    print(f"\033[91m" + task + ": " + str(e) + f"\033[0m")
                    failed.append(task)

        print("finish all")
        if failed:
            print("failed with %s" % (",".join(failed)))
        with open(output_path + "/finish", "w") as f:
            f.write("finish")



