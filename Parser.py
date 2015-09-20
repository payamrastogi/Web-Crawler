import urlparse
import re
import collections
import logging
from Fetcher import Fetcher
from Logger import Logger
from BeautifulSoup import BeautifulSoup

""" Parse the HTML text """
class Parser(object):
    def __init__(self, query, log_level):
        self.query = query
        self.logger = Logger.get_logger("Parser", log_level)

    """ Return links and freqPairs<search_term, freq> """
    def parse(self, text):
        links = self.get_links(text)
        freqPairs = self.get_frequency(self.query, text)
        #print links
        #print freqPairs

    """ Return the content of the <body> tag """
    def get_body(self, text):
         soup = BeautifulSoup(text)
         return soup.find('body').text

    """ Return the freqPairs<search_term, frequency_of_search_term_in_text> """
    def get_frequency(self, query, text):
        freqPairs = {}
        if text is not None:
            words = re.findall('\w+', text.lower())
            pairs = collections.Counter(words)
            searchTerms = re.findall("\w+", query.lower())
            for term in searchTerms:
                freqPairs[term] = pairs[term]
        return freqPairs

    """" Return the links in the text """
    def get_links(self, url, text):
        links = []
        if text is not None:
            soup = BeautifulSoup(text)
            for tag in soup.findAll('a', href=True):
                #print(tag['href'])
                tag['href'] = urlparse.urljoin(url, tag['href']).encode('utf-8')
                links.append(tag['href'])
        return links

""" To test Parser """
def main():
    url = "http://www.sciencedirect.com/"
    parser = Parser("food", logging.DEBUG)
    fetcher = Fetcher(logging.DEBUG)
    text = fetcher.fetch(url)
    parser.parse(url,text)

if __name__ == "__main__":
    main()
