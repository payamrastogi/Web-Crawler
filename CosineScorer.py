import re
import logging
from math import log

class CosineScorer(object):
    def __init__(self, query, p_list, total_docs,log_level):
        self.query = query
        self.p_list = p_list
        self.total_docs = total_docs
        self.__setup_logging(log_level)

    def __setup_logging(self, level):
        logger = logging.getLogger("CosineScorer")
        hdlr = logging.FileHandler("./log/webcrawler.log")
        formatter = logging.Formatter("%(asctime)-15s %(levelname)s  %(module)s.%(funcName)s(): %(message)s")
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(level)
        self.logger = logger

    def get_score(self, query, p_list):
        tfidf_query = {}
        tfidf_document = {}
        scores = {}
        magnitude = {}
        searchTerms = re.findall("\w+", query.lower())
        pairs = collections.Counter(searchTerms)
        for term in searchTerms:
            tfidf_query[term] = (1 + log(pairs[term])) * log(self.total_docs/(len(p_list[term]) + 1)
            for list in p_list[term]:
                for key, value in list.iteritems():
                        tfidf_document[term][key] = (1 + log(value)) * log(self.total_docs/(len(p_list[term]) + 1)
                        if key in scores:
                            scores[key] = scores[key] + tfidf_query[term] * tfidf_document[term][key]
                            magnitude[key] = magnitude[key] + pow(tfidf_document[term][key],2)
                        else:
                            scores[key] =  tfidf_query[term] * tfidf_document[term][key]
                            magnitude[key] = pow(tfidf_document[term][key],2)
        #Normalize scores
        for key, value in scores.iteritems():
            scores[key] = value/sqrt(magnitude[key])
        return scores