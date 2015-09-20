import logging
import requests
import json
import argparse
from Logger import Logger

search_url = "http://ajax.googleapis.com/ajax/services/search/web"
class Searcher(object):

    def __init__(self, query, log_level):
        self.query = query;
        self.rsz = 8 #results per page - 4/8
        self.filter = 1; #turn on duplicate content filter
        self.safe = "off" #safe browsing - active/moderate/off
        self.hl = "en" #Defaults to en
        self.logger = Logger.get_logger("Searcher", log_level)

    def __search(self):
        try:
            args = {"q" : self.query, "v" : 3.0, "start" : 0, "safe" : self.safe, "filter" : self.filter, "hl" : self.hl, "rsz":self.rsz}
            response = requests.get(search_url, params=args) #json format
            if response.status_code != requests.codes.ok:
                self.logger.debug("Response status code is not 200")
                return None
            else:
                result = json.loads(response.content.decode('utf-8'))
                if result.has_key("responseData") and result["responseData"].has_key("results"):
                    return result["responseData"].get("results")
                else :
                    self.logger.error("responseData or results key not found")
                    return None
        except ValueError as e:
            self.logger.error("ValueError" + e)
        except KeyError as e:
            self.logger.error("KeyError" + e)
        except:
            self.logger.error("Unexpected Error occurred")

    def search(self):
        results = self.__search()
        if not results:
            self.logger.info("no results found")
            return
        #for result in results["responseData"]["results"]:
        #   print "-"+result["titleNoFormatting"]
        return results

def main():
    parser = argparse.ArgumentParser(description="A simple Google search module for Python")
    parser.add_argument("query", nargs="*", default=None)
    args = parser.parse_args()
    query = " ".join(args.query)
    log_level = logging.DEBUG
    if not query:
        parser.print_help()
        exit()
    s = Searcher(query, log_level=log_level)
    s.search()

if __name__ == "__main__":
    main()
