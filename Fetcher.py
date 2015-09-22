import logging
import robotparser
import urllib2
import time
import socket
import ssl
from Logger import Logger
from urlparse import urlparse
from URLValidator import runtime_igonre_host


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
                requests = urllib2.Request(url)
                requests.add_header("user-agent", "webcrawler")
                requests.add_header("contact-us", "pr1228@nyu.edu")
                requests.add_header("content-language", "en")
                response = urllib2.urlopen(requests, timeout=3.0)
                request_log_row += " Code: " + str(response.getcode())
                """if response.getcode() != 200:
                    self.failed_request += 1
                    self.logger.debug("Response status code is not 200")
                    self.write_to_request_log(request_log_row)
                    try:
                        parsed = urlparse(url)
                        if parsed is not None and parsed.hostname is not None:
                            runtime_igonre_host.add(parsed.hostname)
                    except:
                        return None
                    return None"""
                if response.getcode() == 200:
                    request_log_row += " Size: " + str(int(response.info().getheader("content-length") or 0)/1000.0) + \
                                       " KB Content-Type : " + response.info().getheader("Content-Type")
                    print request_log_row
                    self.logger.debug("Response status code: 200")
                    if int(response.info().getheader("content-length") or 0) == 0:
                        self.robot_fail_request += 1
                        parsed = urlparse(url)
                        if parsed is not None and parsed.hostname is not None:
                            runtime_igonre_host.add(parsed.hostname)
                        print "No Content From URL"
                        self.discared_url_log("No Content From URL : " + url)
                        self.write_to_request_log(request_log_row)
                        return None
                    elif response.info().getheader("Content-Type").startswith("text/"):
                        self.write_to_request_log(request_log_row)
                        return response.read()
                    else:
                        print url + " -- Invalid Content from the url"
                        self.logger.debug("Invalid Content from the url: " + url)
                        self.discared_url_log("Invalid Content: " + url)
                        self.write_to_request_log(request_log_row)
                        return None
            else:
                self.robot_fail_request += 1
                request_log_row += " Useragent is not allowed to fetch the url"
                self.logger.debug("Useragent is not allowed to fetch the url: " + url)
                self.write_to_request_log(request_log_row)
                self.discared_url_log("Useragent Not Allowed : " + url)
                parsed = urlparse(url)
                if parsed is not None and parsed.hostname is not None:
                    runtime_igonre_host.add(parsed.hostname)
                return None
        except socket.timeout:
            print url + " -- Timed out!"
            self.failed_request += 1
            self.discared_url_log("Timed out : " + url)
            self.write_to_request_log(request_log_row + " -- Time Out")
            try:
                parsed = urlparse(url)
                if parsed is not None and parsed.hostname is not None:
                    runtime_igonre_host.add(parsed.hostname)
            except:
                return None
            return None
        except ssl.SSLError:
            print url + " -- Timed out!"
            self.failed_request += 1
            self.discared_url_log("Timed out : " + url)
            self.write_to_request_log(request_log_row + " -- Time Out")
            try:
                parsed = urlparse(url)
                if parsed is not None and parsed.hostname is not None:
                    runtime_igonre_host.add(parsed.hostname)
            except:
                return None
            return None
        except urllib2.HTTPError, err:
            if err.code == 404:
                print url + " -- Page not found!"
                self.failed_request += 1
                self.discared_url_log("Page not found : " + url)
                self.write_to_request_log(request_log_row + " -- Page not found")
                return None
            elif err.code == 403:
                print url + " -- Access denied!"
                self.robot_fail_request += 1
                self.discared_url_log("Access denied : " + url)
                self.write_to_request_log(request_log_row + " -- Access denied")
                try:
                    parsed = urlparse(url)
                    if parsed is not None and parsed.hostname is not None:
                        runtime_igonre_host.add(parsed.hostname)
                except:
                    return None
            elif err.code == 401:
                print url + " -- Authentication Required!"
                self.robot_fail_request += 1
                self.discared_url_log("Authentication Required : " + url)
                self.write_to_request_log(request_log_row + " -- Authentication Required")
                try:
                    parsed = urlparse(url)
                    if parsed is not None and parsed.hostname is not None:
                        runtime_igonre_host.add(parsed.hostname)
                except:
                    return None
        except:
            self.failed_request += 1
            self.logger.error("Exception:", exc_info=True)
            self.logger.error("Unexpected error occurred")
            self.discared_url_log("Unexpected Error : " + url)
            self.write_to_request_log(request_log_row + " -- Unexpected Error")
            return None

    """
        check if user-agent is allowed or not
        return true if user-agent is allowed else return false
    """

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
            self.failed_request += 1
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

    """ writes discarded url to spam_url.log"""
    def discared_url_log(self, line):
        logfile = open('spam_url.log', 'a')
        logfile.write(line+'\n')
        logfile.close()

            
""" to test Fecther """
def main():
    fetcher = Fetcher(logging.DEBUG)
    url = "http://www.coddicted.com"
    fetcher.fetch(url)

if __name__ == "__main__":
    main()
