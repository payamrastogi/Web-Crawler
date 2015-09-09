import logging
from Logger import Logger

class Writer(object):

    def __init__(self, base_path, log_level):
        self.base_path = base_path
        self.logger = Logger.get_logger("Writer", log_level)

    def write(self, filename, text):
        self.logger.debug("in write")
        try:
            f = open(base_path+filename, 'w')
            f.write(text)
            f.close()
        except:
            self.logger.debug("some exception")

def main():
    w = Writer("./", logging.DEBUG)
    w.write("test.txt", "this is test")

if __name__ == "__main__":
    main()
