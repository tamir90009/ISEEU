from collectors.collector import Collector
import os
import subprocess


class LDPreloadCollector(Collector):
    @staticmethod
    def compil_syscall_detect(script_path, output_path):
        try:
            output, error = subprocess.Popen(["gcc", "-o", output_path, script_path])
            if error:
                raise OSError(error)
        except OSError:
            raise Exception("there was an error compiling" % script_path)

    @staticmethod
    def collect(dst_path):
        try:
            os.mkdir(dst_path)
        except Exception as e:
            raise e
        try:
            compiled_file = dst_path + "/syscall_detect"
            LDPreloadCollector.compilSyscallDetect("stuff/syscall_detect.c", compiled_file)
        except Exception as e:
            raise e
        try:
            output = subprocess.check_output(compiled_file, stderr=subprocess.STDOUT, timeout=10)
            output = output.decode('utf-8')
        except Exception as e:
            raise e
        with open(dst_path + "/check_result") as outFile:
            outFile.write(output)
