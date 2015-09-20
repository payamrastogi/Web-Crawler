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
from URLValidator import is_valid_url
from CosineScorer import CosineScorer
from Indexer import Indexer
from sys import maxint
from Logger import Logger

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

    def __get_google_results(self):
        print "Getting top 10 results from Google"
        search_start = time.time()
        searcher = Searcher(self.query, log_level=self.log_level)
        results = searcher.search()
        print "Results fetched in " + str(time.time()-search_start)+" seconds"
        return results

    def __seed(self, results):
        for result in results:
            if result["unescapedUrl"] is not None:
                #self.logger.debug(result["url"])
                url=urllib.unquote(result['unescapedUrl'])
                self.logger.debug(url)
                self.priority_queue.put(URL(maxint, result['unescapedUrl']))
            else:
                self.logger.debug("url is None")

    def __process_q(self):
        process_start = time.time()
        temp = ""
        try:
            url = self.priority_queue.get()
            print "processing " + url.url
            temp = url.url
            text = self.fetcher.fetch(url.url)
            body = self.parser.get_body(str(text))
            ##if (body is None) or (not is_duplicate_content(body)):
            ##    pass
            score = self.cosine.get_score(body, url.url)
            self.logger.debug(url.url +" : "+str(url.priority)+"---"+ str(score))
            #file_writer.write(url.url, text)
            self.page_count -= 1
            if self.page_count <= 0:
                return
            if text is not None:
                for link in self.parser.get_links(url.url, text):
                    #normalUrl=url_normalize.url_normalize(link)
                    #if is_valid_url(normalUrl):   # If the current url is already crawled discard
                    self.priority_queue.put(URL(score, link))
            print "processed in " + str(time.time()-process_start)+ " seconds."
        except:
            print "processed in " + str(time.time()-process_start)+ " seconds."
            self.logger.error("Exception:", exc_info=True)
            
            
    def crawl(self):
        results = self.__get_google_results()
        self.__seed(results)
        while not self.priority_queue.empty():
            self.__process_q()

def main():
    webCrawler = WebCrawler()
    webCrawler.crawl()

if __name__ == "__main__":
    main()
