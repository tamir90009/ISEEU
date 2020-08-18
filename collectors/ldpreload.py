from collectors.collector import Collector
import os
import subprocess


class LDPreloadCollector(Collector):
    @staticmethod
    def compil_syscall_detect(script_path, output_path):
        try:
            cmd = subprocess.check_output(["gcc", "-o", output_path, script_path])

        except Exception as e:
            raise Exception("there was an error compiling" % script_path)

    @staticmethod
    def ld_check(dst_path, file_name):
        try:
            compiled_file = os.path.join(dst_path, file_name)
            LDPreloadCollector.compil_syscall_detect("additionalscripts/%s.c" % file_name, compiled_file)
        except Exception as e:
            raise e
        try:
            output = subprocess.check_output(compiled_file, shell=True,stderr=subprocess.STDOUT, timeout=10)
            output = output.decode('utf-8')
        except Exception as e:
            raise e
        return output

    @staticmethod
    def collect(dst_path):
        try:
            os.mkdir(dst_path)
        except Exception as e:
            raise e
        try:
            output = LDPreloadCollector.ld_check(dst_path, 'syscall_detect')
        except Exception as e:
            raise e
        with open(dst_path + "/check_result", "w") as outFile:
            outFile.write(output)

        try:
            output = LDPreloadCollector.ld_check(dst_path, 'detect')
        except Exception as e:
            raise e
        with open(dst_path + "/check_result_basic", "w") as outFile:
            outFile.write(output)
