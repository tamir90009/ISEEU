from parsers.parser import Parser


class LDPreloadParser(Parser):
    @staticmethod
    def parse(data_file_path):
        try:
            with open(data_file_path + "/check_result", "r") as f:
                data = f.readlines()
        except Exception as e:
            raise e
        results = {}
        if "/etc/ld.so.preload is not present" in data[0]:
            results["so"] = True
        else:
            results["so"] = False

        if "Memory maps are clean" in data[1]:
            results["memory"] = True
        else:
            results["memory"] = False

        return results
