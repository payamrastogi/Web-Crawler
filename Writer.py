import logging
import hashlib
import os
from Logger import Logger
from urlparse import urlparse

""" Write content to file """
class Writer(object):

    def __init__(self, base_path, log_level):
        self.base_path = base_path
        self.logger = Logger.get_logger("Writer", log_level)

    """ create folder with name hash(url) and save the file with name index.html """
    def write(self, url, text):
        try:
            self.logger.debug("in write")
            parsed_uri = urlparse(url)
            net_loc = '{uri.netloc}'.format(uri=parsed_uri)
            path = '{uri.path}'.format(uri=parsed_uri)
            hashed =  hashlib.sha224(net_loc).hexdigest()
            dir = hashed + path
            if not os.path.isdir(dir):
                os.makedirs(dir)
            f = open(dir+"/index.html", 'w')
            f.write(str(text))
            f.close()
            return f.name
        except Exception as ex:
            self.logger.error("Exception:", exc_info=True)
        return None

            
""" to test """
def main():
    w = Writer("./", logging.DEBUG)
    w.write("test.txt", "this is test")

if __name__ == "__main__":
    main()
