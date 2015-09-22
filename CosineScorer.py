import re
import time
import collections
import logging
import hashlib
import Queue as Q
from math import log
from math import sqrt
from Logger import Logger
from Indexer import Indexer

""" 
To Calculate the cosine score for a document(html page) 
Modification to original Cosine Similarity Score 
instead of using  (|Corpus| / df(t,q)), where |Corpus| is the total number of documents 
and df(t,q) is the number of documents in which term t appears, we have used (total_frequency/frequency_of_term)
where total_frequency is the total number of words appear in Wikipedia (English) pages and frequency_of_term is 
the frequency of term in those pages
total_frequency is 1229245740
"""
class CosineScorer(object):

    """
        @params word_dic A dictionary containing words and their normalized frequency
        @params query Search query
    """
    def __init__(self, word_dict, query, log_level):
        self.word_dict = word_dict
        self.query = query
        self.tfidf_query = {} #term frequency inverse document frequency, here query is the document
        self.searchTerms = re.findall("\w+", query.lower())
        pairs = collections.Counter(self.searchTerms)
        for term in self.searchTerms:
            if term in pairs.keys() and term in self.word_dict.keys():
                self.tfidf_query[term] = (1 + log(pairs[term])) * self.word_dict[term]
            else:
                self.tfidf_query[term] = 0
        self.logger = Logger.get_logger("CosineScorer", log_level)

    """
        Return the document score
    """
    def get_score(self, text):
        scores = 0.0
        if text is None:
            return scores
        tfidf_document = {}
        terms = re.findall("\w+", text.lower())
        #pairs_start = time.time()
        pairs = collections.Counter(terms)
        #print "pairs_counted in: " + str(time.time()-pairs_start)+ " seconds."
        magnitude = 0.0
        for_cosine_start = time.time()
        for term in self.searchTerms:
            #dict_start = time.time()
            if term in pairs and term in self.word_dict:
                #print "dict compared in: " + str(time.time()-dict_start)+ " seconds."
                #cal_start = time.time()
                tfidf_document[term] = (1 + log(pairs[term])) * self.word_dict[term]
                scores = scores + self.tfidf_query[term] * tfidf_document[term]
                magnitude = magnitude + pow(tfidf_document[term],2)
                #print "calculated in: " + str(time.time()-cal_start)+ " seconds."
        #print "for_cosine in: " + str(time.time()-for_cosine_start)+ " seconds."
        #Normalize scores
        if magnitude != 0:
            scores = scores/sqrt(magnitude)
        return scores

    def get_link_score(self, text):
        scores = 0.0
        if text is None:
            return scores
        terms = re.findall("\w+", text.lower())
        pairs = collections.Counter(terms)
        for term in self.searchTerms:
            if term in pairs:
                scores = scores + pairs[term]
        return scores


""" to test CosineScorer """
def main():
    start = time.time()
    indexer = Indexer(logging.DEBUG)
    word_dict = indexer.get_normalized_fequency()
    cosine = CosineScorer(word_dict, "the cat and the dog jkhgdh", logging.DEBUG)
    score = cosine.get_score("httpwwwvimncompressnickseriessam uSam jkhgdh ampcat", "http://www.google.com")
    print score
    print str(time.time() - start) + " seconds"

if __name__=="__main__":
    main()