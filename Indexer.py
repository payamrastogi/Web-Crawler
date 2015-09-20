import logging
from Logger import Logger
from math import log
import time
import hashlib
import pickle

file_path="./wordfreq.txt"
total_words = 1229245740
class Indexer(object):

    def __init__(self, log_level):
        self.logger = Logger.get_logger("Indexer", log_level)

    def get_normalized_fequency(self):
        print "initializing word dictionary..."
        try:
            index = {}
            f = open(file_path, "r")
            if f is not None:
                for line in f:
                    i = line.split("\t")
                    index[i[0]] = log(total_words/int(i[1]))
                #pickle.dump(index, open("./wordfreq.pql", "wb"))
                return index
            else:
                print "error"
        except Exception:
            self.logger.error("Exception:", exc_info=True)
            return None

def main():
    start = time.time()
    indexer = Indexer(log_level=logging.DEBUG)
    index = indexer.get_normalized_fequency()
    if index is not None:
        print index["the"]
    else:
        print "Error occured!!"
    print str(time.time() - start) + " seconds"

if __name__ == "__main__":
    main()
