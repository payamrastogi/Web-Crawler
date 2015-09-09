from Logger import Logger

class Writer(object):

    def __init__(self, base_path, log_level):
        self.base_path = base_path
        self.logger = Logger.getLogger("Writer", log_level)

    def write(self, filename, text):
        f = open(base_path+filename, 'w')
        f.write(text)
        f.close()
