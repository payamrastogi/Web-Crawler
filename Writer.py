import logging
from Logger import Logger
from urlparse import urlparse

class Writer(object):

    def __init__(self, base_path, log_level):
        self.base_path = base_path
        self.logger = Logger.get_logger("Writer", log_level)

    def write(self, filename, text):
        self.logger.debug("in write")
        try:
            f = open(self.base_path+filename, 'w')
            f.write(text)
            f.close()
        except:
            self.logger.error("Exception:", exc_info=True)

    def writeToPath(self, url, text):
        self.logger.debug("in write")
        parsed_uri = urlparse('http://stackoverflow.com/questions/1234567/blah-blah-blah-blah')
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        try:
            f = open(domain+"index.html", 'w')
            f.write(text)
            print f
            f.close()
        except Exception as ex:
            self.logger.error("Exception:", exc_info=True)

def main():
    w = Writer("./", logging.DEBUG)
    w.write("test.txt", "this is test")

if __name__ == "__main__":
    main()
