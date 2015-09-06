import re
import collections
words = re.findall('\w+', "This is new line".lower())
c = collections.Counter(words)
print c["this"]
