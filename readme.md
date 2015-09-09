#### To-Do
- posting list
- multi-threading
- priority queue based scores dict
- test CosineScorer
- hashing logic for documents
- file writer
- dict to maintain filename, hash-value, path

#### Ranking and Retrieving Details
- Fetch links for top-10 results from Google for a query.
- Fetch first link from search results and update term frequency for document for all the terms and calculate score for this document and store it in priority queue (prioirity queue data structure will contain following fields - doc_score, doc_hashcode, term frequency for each term in query, doc_url, downloaded_path??) and mark them visited and fetch all the links from this page and add them in the queue.
- Fetch second link from search results and update term frequency for document for all the terms and calculate the score for this document and mark them visited
- so on until all the search term links are downloaded and scored.
- Now fetch all the link.

#### components
 - robotparser - https://docs.python.org/2/library/robotparser.html
 - urlib2 - https://docs.python.org/2/library/urllib2.html
 - HTMLParser - https://docs.python.org/2/library/htmlparser.html
 - Google Web Search api (deprecated) - http://ajax.googleapis.com/ajax/services/search/web?q=dog&v=3.0&rsz=8&start=0
 - pygoogle - http://pygoogle.googlecode.com/svn/trunk/pygoogle.py
 - Threading
    * http://www.tutorialspoint.com/python/python_multithreading.htm
    * http://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python
 - TF-IDF (see example) - https://en.wikipedia.org/wiki/Tf%E2%80%93idf
 - Cosine scoring
    * http://www.ics.uci.edu/~djp3/classes/2008_09_26_CS221/Lectures/Lecture26.pdf
    * http://nlp.stanford.edu/IR-book/html/htmledition/efficient-scoring-and-ranking-1.html
 - collections.Counter - https://docs.python.org/2/library/collections.html
 - hashlib - https://docs.python.org/2/library/hashlib.html#module-hashlib
 - &lt;Key, Value&gt; where value is list
    * http://stackoverflow.com/questions/960733/python-creating-a-dictionary-of-lists
    * https://docs.python.org/2/library/collections.html
 - requests - http://docs.python-requests.org/en/latest/user/quickstart/
 - urlparse
    * http://stackoverflow.com/questions/9626535/get-domain-name-from-url   
    * https://docs.python.org/2/library/urlparse.html
 - Unicode strings to regular strings - http://stackoverflow.com/questions/4855645/how-to-turn-unicode-strings-into-regular-strings
 - Priority Queue - http://www.bogotobogo.com/python/python_PriorityQueue_heapq_Data_Structure.php
 - static method - http://stackoverflow.com/questions/735975/static-methods-in-python
