
class Analyzer(object):
    def __init__(self, whitelist):
        if isinstance(whitelist,str):
            self.import_whitelist_from_file(whitelist)
        else:
            self.import_whitelist_data(whitelist)

    def Analyze(self, data):
        raise NotImplemented

    def import_whitelist_data(self, whitelist_data):
        self.whitelist_data = whitelist_data

    def import_whitelist_from_file(self, whitelist_path):
        with open(whitelist_path,"r") as f:
            self.import_whitelist_data(f.readlines())

    def remove_known_behavior(self, analyzed_data):
        #todo: maybe can be written here
        raise NotImplemented