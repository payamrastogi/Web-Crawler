import requests
import logging
import robotparser
from urlparse import urlparse

class Fetcher(object):
    def __init__(self, log_level):
        self.__setup_logging(log_level)

    def __setup_logging(self, level):
        logger = logging.getLogger("Fetcher")
        hdlr = logging.FileHandler("./log/webcrawler.log")
        formatter = logging.Formatter("%(asctime)-15s %(levelname)s  %(module)s.%(funcName)s(): %(message)s")
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(level)
        self.logger = logger

    def fetch(self, url):
        try:
            if self.__can_fetch(url):
                response = requests.get(url)
                if response.status_code != requests.codes.ok:
                    self.logger.debug("Response status code is not 200")
                    return None
                else:
                    self.logger.debug("Response status code: 200")
                    return response.content
            else:
                self.logger.debug("Useragent is not allowed to fetch the url: " + url)
                return None
        except:
            self.logger.error("Unexpected error occurred")

    def __can_fetch(self, url):
        try:
            base_url = self.__get_base_url(url)
            if base_url:
                rp = robotparser.RobotFileParser()
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
    print fetcher.fetch(url)

if __name__ == "__main__":
    main()
