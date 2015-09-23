import hashlib
import unicodedata
from urllib import unquote
from Logger import Logger
import logging

visited_content = set()
logger = Logger.get_logger("URLValidator", logging.DEBUG)

def txt_md5(txt):
    try:
        unicodetxt = unicode(unquote(txt), 'utf-8', 'replace')
        utftxt = unicodedata.normalize('NFC', unicodetxt).encode('utf-8')
        return hashlib.md5(utftxt).hexdigest()
    except:
        logger.error("Exception:", exc_info=True)
        return None

def is_duplicate_content(txt, url):
    txt_hash = txt_md5(txt)
    if txt_hash is None:
        return False
    if txt_hash in visited_content:
        print "Duplicate Content"
        discared_url_log("Duplicate Content : " + url)
        return True
    else:
        visited_content.add(txt_hash)
        return False
""" writes discarded url to spam_url.log"""
def discared_url_log(line):
    pass
    #logfile = open('spam_url.log', 'a')
    #logfile.write(line+'\n')
    #logfile.close()