from urlparse import urlparse
from os.path import splitext
import unicodedata
from urllib import unquote
from Logger import Logger
import logging

seen_urls = set()
runtime_igonre_host = set()
logger = Logger.get_logger("URLValidator", logging.DEBUG)

def is_unique(url):
    # Strip of the last bit
    original_url = url
    try:
        parsed = urlparse(url)
        if parsed is None or parsed.hostname is None:
            return False
        url = parsed.hostname + str(parsed.path)
        if url in seen_urls:
            discared_url_log("Duplicate URL : " + original_url)
            return False
        seen_urls.add(url)
        return True
    except:
        logger.error("Exception:", exc_info=True)
        return True

def get_ext(url):
    """Return the filename extension from url, or ''."""
    try:
        parsed = urlparse(url)
        if parsed is None:
            return None
        root, ext = splitext(parsed.path)
        return ext
    except:
        logger.error("Exception:", exc_info=True)
        return None

def is_valid_extention(url):
    IGNORED_EXTENSIONS = [
        # images
        '.mng', '.pct', '.bmp', '.gif', '.jpg', '.jpeg', '.png', '.pst', '.psp', '.tif',
        '.tiff', '.ai', '.drw', '.dxf', '.eps', '.ps', '.svg',

        # audio
        '.mp3', '.wma', '.ogg', '.wav', '.ra', '.aac', '.mid', '.au', '.aiff',

        # video
        '.3gp', '.asf', '.asx', '.avi', '.mov', '.mp4', '.mpg', '.qt', '.rm', '.swf', '.wmv',
        '.m4a',

        # other
        '.css', '.pdf', '.doc', '.exe', '.bin', '.rss', '.zip', '.rar', '.docx', '.xls', '.xlsx',
        '.js', '.ppt', '.pptx',
    ]
    ext = get_ext(url)

    if ext in IGNORED_EXTENSIONS:
        discared_url_log("Invalid URL Ext. : " + url)
        return False
    return True

def is_valid_host(url):
    IGNORED_HOSTS = [
        'www.youtube.com', 'www.dailymotion.com', 'www.netflix.com', 'www.yelp.com', 'www.grubhub.com',
        'www.mediawiki.org', 'www.twitter.com' , 'www.tv.com', 'www.facebook.com', 'www.wikipedia.org'
        'www.en.wikipedia.org',
    ]
    try:
        parsed = urlparse(url)
        if parsed is None or parsed.hostname is None:
            discared_url_log("Black Listed Host : " + url)
            return False
        if parsed.hostname in IGNORED_HOSTS or parsed.hostname in runtime_igonre_host:
            discared_url_log("Black Listed Host : " + url)
            return False
        return True
    except:
        logger.error("Exception:", exc_info=True)
        return True

def is_valid_url(url):
    return is_unique(url) and is_valid_extention(url) and is_valid_host(url)

""" writes discarded url to spam_url.log"""
def discared_url_log(line):
    logfile = open('spam_url.log', 'a')
    logfile.write(line+'\n')
    logfile.close()

