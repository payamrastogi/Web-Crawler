import requests
import logging
import robotparser
import urllib2
from Logger import Logger
from urlparse import urlparse
from URLValidator import runtime_igonre_host
import time

""" To fetch urls """

class Fetcher(object):
    def __init__(self, log_level):
        self.logger = Logger.get_logger("Fetcher", log_level)
        self.total_request = 0
        self.failed_request = 0
        self.robot_fail_request = 0

    """
        Return response else return None  
    """

    def fetch(self, url):
        self.total_request += 1;
        request_log_row = url+" Time: " + str(time.asctime(time.localtime(time.time())))
        try:
            if self.__can_fetch(url):
                headers = {"user-agent": "webcrawler", "contact-us":"pr1228@nyu.edu"}
                response = requests.get(url)
                request_log_row += " Code: " + str(response.status_code)
                if response.status_code != requests.codes.ok:
                    self.failed_request += 1
                    self.logger.debug("Response status code is not 200")
                    self.write_to_request_log(request_log_row)
                    return None
                else:
                    request_log_row += " Size: " + str(int(response.headers['content-length'])/1000.0) + " KB Content-Type : " + response.headers['content-type']
                    self.write_to_request_log(request_log_row)
                    self.logger.debug("Response status code: 200")
                    if response.headers['content-type'].startswith("text/html"):
                        return response.content
                    else:
                        self.logger.debug("Invalid Content from the url: " + url)
                        return None
            else:
                parsed = urlparse(url)
                if parsed is not None and parsed.hostname is not None:
                    runtime_igonre_host.add(parsed.hostname)
                self.robot_fail_request += 1
                request_log_row += " Useragent is not allowed to fetch the url"
                self.logger.debug("Useragent is not allowed to fetch the url: " + url)
                self.write_to_request_log(request_log_row)
                return None
        except:
            self.logger.error("Unexpected error occurred")

    """
        check if user-agent is allowed or not
        return true if user-agent is allowed else return false
    """

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

    """
        Return base_url i.e http://<hostname>/<path> else return None
        parameters are omitted from the url
    """
    def __get_base_url(self, url):
        try:
            parsed_uri = urlparse(url)
            base_url = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_uri)
            return base_url
        except:
            self.logger.error("cannot parse url: " + url)
            return None

    def write_to_request_log(self, line):
        logfile = open('request.log', 'a')
        logfile.write(line+'\n')
        logfile.close()

            
""" to test Fecther """
def main():
    fetcher = Fetcher(logging.DEBUG)
    url = "http://www.animalplanet.com/pets/dogs/"
    print fetcher.fetch(url)

if __name__ == "__main__":
    main()
