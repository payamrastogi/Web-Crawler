import re
from math import log
from math import sqrt
import logging
from Logger import Logger
import Queue as Q
import hashlib
import pickle
from Indexer import Indexer
import time
import collections

class CosineScorer(object):

    def __init__(self, word_dict, query, log_level):
        self.word_dict = word_dict
        #self.word_dict = pickle.load(open("wordfreq.pql", "rb"))
        self.query = query
        self.tfidf_query = {}
        self.searchTerms = re.findall("\w+", query.lower())
        pairs = collections.Counter(self.searchTerms)
        for term in self.searchTerms:
            self.tfidf_query[term] = (1 + log(pairs[term])) * self.word_dict[term]
        self.logger = Logger.get_logger("CosineScorer", log_level)

    def get_score(self, text, url):
        scores = 0.0
        tfidf_document = {}
        terms = re.findall("\w+", text.lower())
        pairs = collections.Counter(terms)
        print pairs["cat"]
        magnitude = 0.0
        for term in self.searchTerms:
            tfidf_document[term] = (1 + log(pairs[term])) * self.word_dict[term]
            scores = scores + self.tfidf_query[term] * tfidf_document[term]
            magnitude = magnitude + pow(tfidf_document[term],2)
        #Normalize scores
        scores = scores/sqrt(magnitude)
        return scores

def main():
    start = time.time()
    indexer = Indexer(logging.DEBUG)
    word_dict = indexer.get_normalized_fequency()
    cosine = CosineScorer(word_dict, "the cat and the dog", logging.DEBUG)
    score = cosine.get_score("the cat and the dog are best friends", "http://www.google.com")
    print score
    print str(time.time() - start) + " seconds"

if __name__=="__main__":
    main()
