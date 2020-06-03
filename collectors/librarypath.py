from collectors.collector import Collector
import os


class LibraryPathCollector(Collector):

    @staticmethod
    def collect(dst_path):
        library_path_data = os.environ.get("LD_LIBRARY_PATH", "empty")
        with open(dst_path, "w") as outFile:
            outFile.write(library_path_data)
