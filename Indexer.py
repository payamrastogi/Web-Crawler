import logging
import time
import hashlib
from Logger import Logger
from math import log

""" http://d241g0t0c5miix.cloudfront.net/data/wikipedia_wordfreq.txt.gz """
""" To create a dictionary containing word and its normalized frequency """
file_path="./wordfreq.txt"
total_words = 1229245740
class Indexer(object):

    def __init__(self, log_level):
        self.logger = Logger.get_logger("Indexer", log_level)

    """ 
        Return a dictionary containing word and its normalized frequency
        Normalized frequency is calculated as:
        log(tota_words/freqeuncy_of_term)
        where total_words is the total_words in wikipedia pages (English) 
        and frequency_of_term is the frequency of term in those wikipedia pages
    """
    def get_normalized_fequency(self):
        print "Initializing word dictionary..."
        start = time.time()
        try:
            index = {}
            f = open(file_path, "r")
            if f is not None:
                for line in f:
                    i = line.split("\t")
                    index[i[0]] = log(total_words/int(i[1]))
                print "Initialized in " + str(time.time()-start) +" seconds."
                return index
        except Exception:
            self.logger.error("Exception:", exc_info=True)
            return None

""" to test Indexer"""
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
