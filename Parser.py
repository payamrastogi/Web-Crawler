import urlparse
import re
import collections
import logging
from Fetcher import Fetcher
from BeautifulSoup import BeautifulSoup

class Parser(object):
    def __init__(self, url, query, log_level):
        self.url = url
        self.query = query
        self.__setup_logging(log_level)

    def __setup_logging(self, level):
        logger = logging.getLogger("Parser")
        hdlr = logging.FileHandler("./log/webcrawler.log")
        formatter = logging.Formatter("%(asctime)-15s %(levelname)s  %(module)s.%(funcName)s(): %(message)s")
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(level)
        self.logger = logger

    def parse(self, text):
        links = self.__get_links(text)
        freqPairs = self.__get_frequency(self.query, text)
        print links
        print freqPairs

    def __get_frequency(self, query, text):
        freqPairs = {}
        words = re.findall('\w+', text.lower())
        pairs = collections.Counter(words)
        searchTerms = re.findall("\w+", query.lower())
        for term in searchTerms:
            freqPairs[term] = pairs[term]
        return freqPairs

    def __get_links(self, text):
        links = []
        soup = BeautifulSoup(text)
        for tag in soup.findAll('a', href=True):
            tag['href'] = urlparse.urljoin(self.url, tag['href'])
            links.append(tag['href'])
        return links

def main():
    url = "http://www.animalplanet.com/pets/dogs/"
    parser = Parser(url, "dog cats", logging.DEBUG)
    fetcher = Fetcher(logging.DEBUG)
    text = fetcher.fetch(url)
    parser.parse(text)

if __name__ == "__main__":
    main()
