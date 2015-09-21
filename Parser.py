import urlparse
import re
import collections
import logging
from Fetcher import Fetcher
from Logger import Logger
from BeautifulSoup import BeautifulSoup
import urlparse
import unicodedata
from urllib import unquote
from Link import Link

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
                tag['href'] = self._clean(urlparse.urljoin(self._clean(url), self._clean(tag['href'])))
                if tag['href'] and "javascript" not in tag['href'].lower():
                    try :
                        extra_info = self._alpha_num_str(self._clean(tag['href']) + ' ' + str(self._clean(tag.contents)))
                    except:
                       extra_info = self._alpha_num_str(self._clean(tag['href']))

                    links.append(Link(self._clean(tag['href']),extra_info))
        return links

    def _clean(self, string):
        try:
            string = unicode(unquote(string), 'utf-8', 'replace')
            return unicodedata.normalize('NFC', string).encode('utf-8')
        except:
            return string

    def _alpha_num_str(self,string):
        try :
            return re.sub('[^a-zA-Z0-9\n ]', ' ', string)
        except:
            return string

def main():
    url = "http://www.sciencedirect.com/"
    parser = Parser("food", logging.DEBUG)
    fetcher = Fetcher(logging.DEBUG)
    text = fetcher.fetch(url)
    parser.parse(url,text)

if __name__ == "__main__":
    main()
