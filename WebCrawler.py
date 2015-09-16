import logging
from Searcher import Searcher
from Fetcher import Fetcher
from Parser import Parser
from URL import URL
from Writer import Writer
import Queue as Q

def main():
    query = "food"
    log_level = logging.DEBUG
    s = Searcher(query, log_level=log_level)
    search_results = s.search()
    fetcher = Fetcher(logging.DEBUG)
    prio_queue = Q.PriorityQueue()
    link_set = set()
    file_writer = Writer("./", logging.DEBUG)

    for result in search_results["responseData"]["results"]:
        if result["url"] is not None:
            prio_queue.put(URL(1, result["url"]))

    while not prio_queue.empty():
        url = prio_queue.get()
        link_set.add(url.url)
        text = fetcher.fetch(url.url)
        file_writer.write(url.url, text)
        print(str(url.priority) + "<---->" + url.url)
        if text is not None:
            parser = Parser(url.url, query, logging.DEBUG)
            for link in parser.parseGetLinks(text):
                if url.priority < 1 and link not in link_set:
                    prio_queue.put(URL(url.priority + 1, link))


if __name__ == "__main__":
    main()
