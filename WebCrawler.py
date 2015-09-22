import Queue as Q
import logging
import time
import urllib
from Searcher import Searcher
from Fetcher import Fetcher
from Parser import Parser
from URL import URL
from Writer import Writer
from FindMatches import is_duplicate_content
from URLValidator import is_valid_url, is_valid_host
from CosineScorer import CosineScorer
from Indexer import Indexer
from sys import maxint
from Logger import Logger

""" 
    Main file
    user will be asked to provide search query
    and number of pages to be downloaded 
"""
class WebCrawler(object):


    def __init__(self):
        indexer = Indexer(logging.DEBUG)
        self.word_dict = indexer.get_normalized_fequency()
        self.query = raw_input("Search query: ")
        self.page_count = int(raw_input("No. of pages to download: "))
        self.log_level = logging.DEBUG
        self.priority_queue = Q.PriorityQueue()
        self.fetcher = Fetcher(self.log_level)
        self.parser = Parser(self.query, self.log_level)
        self.cosine = CosineScorer(self.word_dict, self.query, self.log_level)
        self.logger = Logger.get_logger("webcrawler", self.log_level)
        self.file_writer = Writer("./", logging.DEBUG)
        self.total_links_found = 0
        self.saved_content = 0.0
        self.rank = 1

    """ fetch top 10 results from google """
    def __get_google_results(self):
        print "Getting top 10 results from Google"
        search_start = time.time()
        searcher = Searcher(self.query, log_level=self.log_level)
        results = searcher.search()
        print "Results fetched in " + str(time.time()-search_start)+" seconds"
        return results

    """ creates priority queue and add urls (fetched from google) """
    def __seed(self, results):
        for result in results:
            if result["unescapedUrl"] is not None:
                url=urllib.unquote(result['unescapedUrl'])
                if is_valid_url(result['unescapedUrl']):
                    self.logger.debug(url)
                    self.total_links_found += 1
                    self.priority_queue.put(URL(maxint, result['unescapedUrl']))
            else:
                self.logger.debug("url is None")

    """ process priority queue """
    def __process_q(self):
        process_start = time.time()
        try:
            url = self.priority_queue.get()
            if is_valid_host(url.url):
                text = self.fetcher.fetch(url.url)
                if (text is not None) and (not is_duplicate_content(text, url.url)):
                    self.logger.debug("processing " + url.url)
                    score = self.cosine.get_score(text, url.url)
                    if score != 0:
                        self.logger.debug(url.url +" : "+str(url.priority)+"---"+ str(score))
                        self.saved_content += len(text)/1000
                        file_path = self.file_writer.write(url.url, text)
                        result_log_row = "Rank :"+ str(self.rank) +" URL :" + url.url + \
                                      " Score :" + str(url.priority) + \
                                      " Download Path :" + file_path
                        self.write_to_result_log(result_log_row)
                        self.rank += 1
                        for link in self.parser.get_links(url.url, text):
                            self.total_links_found += 1
                            if is_valid_url(link.url):
                                link_score = self.cosine.get_score(link.extra_info, url.url)
                                self.priority_queue.put(URL(score+link_score, link.url))
                    print "processed in " + str(time.time()-process_start)+ " seconds."
        except:
            self.logger.error("Exception:", exc_info=True)


    """ writes result to log """
    def write_to_result_log(self, line):
        logfile = open('result.log', 'a')
        logfile.write(line+'\n')
        logfile.close()

    def crawl(self):
        results = self.__get_google_results()
        self.__seed(results)
        while not self.priority_queue.empty() and self.rank <= self.page_count:
            self.__process_q()

def main():
    total_start = time.time()
    webCrawler = WebCrawler()
    webCrawler.crawl()

    stat_info = "\n\n\n Total Links Found :" + str(webCrawler.total_links_found) +\
                "\n Total Request Made :" + str(webCrawler.fetcher.total_request) +\
                "\n Total Request Failed :" + str(webCrawler.fetcher.failed_request + webCrawler.fetcher.robot_fail_request) +\
                "\n Total Request Failed Due to Robot :" + str(webCrawler.fetcher.robot_fail_request) +\
                "\n Saved Content Size :" + str(webCrawler.saved_content) + " KB" +\
                "\n Total Time :"+ str(time.time()-total_start)+ " seconds."
    webCrawler.write_to_result_log(stat_info)

if __name__ == "__main__":
    main()
