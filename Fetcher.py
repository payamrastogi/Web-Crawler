import requests
import logging
import robotparser
from Logger import Logger
from urlparse import urlparse

class Fetcher(object):
    def __init__(self, log_level):
        self.logger = Logger.get_logger("Fetcher", log_level)

    def fetch(self, url):
        try:
            if self.__can_fetch(url):
                headers = {"user-agent": "webcrawler", "contact-us":"pr1228@nyu.edu"}
                response = requests.get(url)
                if response.status_code != requests.codes.ok:
                    self.logger.debug("Response status code is not 200")
                    return None
                else:
                    self.logger.debug("Response status code: 200")
                    return response.content
            else:
                self.logger.debug("useragent is not allowed to fetch the url: " + url)
                return None
        except:
            self.logger.error("unexpected error occurred")

    def __can_fetch(self, url):
        try:
            base_url = self.__get_base_url(url)
            if base_url:
                rp = robotparser.RobotFileParser()
                #print base_url
                rp.set_url(base_url + "robots.txt")
                rp.read()
                return rp.can_fetch("*", url)
            else:
                return False
        except:
            self.logger.error("invalid url")
            return False

    def __get_base_url(self, url):
        try:
            parsed_uri = urlparse(url)
            base_url = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_uri)
            return base_url
        except:
            self.logger.error("cannot parse url: " + url)
            return None

def main():
    fetcher = Fetcher(logging.DEBUG)
    url = "http://www.animalplanet.com/pets/dogs/"
    #print fetcher.fetch(url)

if __name__ == "__main__":
    main()
