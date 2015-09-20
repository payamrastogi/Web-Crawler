class URL(object):
    def __init__(self, priority, url):
        self.priority = priority
        self.url = url
        return

    def __cmp__(self, other):
        return cmp(other.priority, self.priority)