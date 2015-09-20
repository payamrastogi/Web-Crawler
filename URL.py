
""" 
	URL object 
	instance fields - priority, url
	to be used with priority queue 
"""
class URL(object):
    def __init__(self, priority, url):
        self.priority = priority
        self.url = url
        return
    """ to comapre priorities of two different URL object"""
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)