import urlparse
import re
import collections
import logging
from Fetcher import Fetcher
from Logger import Logger
from BeautifulSoup import BeautifulSoup

class Parser(object):
    def __init__(self, query, log_level):
        self.query = query
        self.logger = Logger.get_logger("Parser", log_level)

    def parse(self, text):
        links = self.__get_links(text)
        freqPairs = self.__get_frequency(self.query, text)
        #print links
        #print freqPairs

    def get_body(self, text):
         soup = BeautifulSoup(text)
         return soup.find('body').text

    def __get_frequency(self, query, text):
        freqPairs = {}
        if text is not None:
            words = re.findall('\w+', text.lower())
            pairs = collections.Counter(words)
            searchTerms = re.findall("\w+", query.lower())
            for term in searchTerms:
                freqPairs[term] = pairs[term]
        return freqPairs

    def get_links(self, url, text):
        links = []
        if text is not None:
            soup = BeautifulSoup(text)
            for tag in soup.findAll('a', href=True):
                #print(tag['href'])
                tag['href'] = urlparse.urljoin(url, tag['href']).encode('utf-8')
                links.append(tag['href'])
        return links

def main():
    url = "http://www.sciencedirect.com/"
    parser = Parser("food", logging.DEBUG)
    fetcher = Fetcher(logging.DEBUG)
    text = fetcher.fetch(url)
    parser.parse(url,text)

if __name__ == "__main__":
    main()
