import urlparse
import re
import collections
import logging
from Fetcher import Fetcher
from Logger import Logger
from BeautifulSoup import BeautifulSoup

class Parser(object):
    def __init__(self, url, query, log_level):
        self.url = url
        self.query = query
        self.logger = Logger.get_logger("Parser", log_level)

    def parse(self, text):
        links = self.__get_links(text)
        freqPairs = self.__get_frequency(self.query, text)
        #print links
        #print freqPairs

    def parseGetLinks(self, text):
        return self.__get_links(text)

    def parseGetFrequency(self, text):
        return self.__get_frequency(self.query, text)

    def __get_frequency(self, query, text):
        freqPairs = {}
        if text is not None:
            words = re.findall('\w+', text.lower())
            pairs = collections.Counter(words)
            searchTerms = re.findall("\w+", query.lower())
            for term in searchTerms:
                freqPairs[term] = pairs[term]
        return freqPairs

    def __get_links(self, text):
        links = []
        if text is not None:
            soup = BeautifulSoup(text)
            for tag in soup.findAll('a', href=True):
                #print(tag['href'])
                tag['href'] = urlparse.urljoin(self.url, tag['href']).encode('utf-8')
                links.append(tag['href'])
        return links

def main():
    url = "http://www.sciencedirect.com/"
    parser = Parser(url, "food", logging.DEBUG)
    fetcher = Fetcher(logging.DEBUG)
    text = fetcher.fetch(url)
    parser.parse(text)

if __name__ == "__main__":
    main()
