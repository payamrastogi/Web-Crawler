# Class to parse the top 10 results from BING. It extracts http links from the bing page.
from Tag import Tag
from HTMLParser import HTMLParser

class LinkExtractor(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.inlink = False
        self.link = ""
        self.data = []
        self.tags = []

    def handle_starttag(self, tag, attrs):
        #print "Start tag:", tag
        if tag.lower()=='a':
            for (key,value) in attrs:
                if key == 'href':
                    self.link = value
                    self.inlink = True
                    #print "     attr:", value

    def handle_endtag(self, tag):
        if tag.lower() == "a":
            self.inlink = False
            self.link=""
            #print "".join(self.data)

    def handle_data(self, data):
        if self.inlink:
            self.tags.append(Tag(self.link, data))

    def get_tags(self):
        return self.tags
    