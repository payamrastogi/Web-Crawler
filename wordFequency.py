import re
import collections
words = re.findall('\w+', open('./test.txt').read().lower())
print collections.Counter(words)
