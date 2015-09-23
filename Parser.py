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
from LinkExtractor import LinkExtractor

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
        try:
            if text is not None:
                #soup = BeautifulSoup(text)
                linkExtractor = LinkExtractor()
                linkExtractor.feed(text)
                for tag in linkExtractor.get_tags():
                    original_href = tag.href
                    tag.href = self._clean(urlparse.urljoin(self._clean(url), self._clean(tag.href)))
                    if tag.href and "javascript" not in tag.href.lower():
                        try :
                            extra_info = self._alpha_num_str(self._clean(original_href) + ' ' + str(self._clean(tag.content)))
                        except:
                            extra_info = self._alpha_num_str(self._clean(original_href))
                        links.append(Link(self._clean(tag.href),extra_info))
        except:
            print "Content Parsing Error"
        return links

    """ To test Parser """

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
    #url = "http://www.coddicted.com"
    #parser = Parser("java", logging.DEBUG)
    #fetcher = Fetcher(logging.DEBUG)
    #text = fetcher.fetch(url)
    #print text
    #for link in parser.get_links(url, text):
    #    print link.url
    linkExtractor = LinkExtractor()
    linkExtractor.feed("<p>hello</p><p><a class='link' href='#main'><img src='/xyz'/></a><a href='#index'>welcome abcd efgh</a></p>")
    tags =  linkExtractor.get_tags()
    for tag in tags:
        print tag.href
        print tag.content
    #parser.parse(url,text)

if __name__ == "__main__":
    main()
