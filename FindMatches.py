import hashlib
import unicodedata
from urllib import unquote

visited_content = set()

def txt_md5(txt):
    try:
        unicodetxt = unicode(unquote(txt), 'utf-8', 'replace')
        utftxt = unicodedata.normalize('NFC', unicodetxt).encode('utf-8')
        return hashlib.md5(utftxt).hexdigest()
    except:
        return None

def is_duplicate_content(txt):
    txt_hash = txt_md5(txt)
    if txt_hash is None:
        return False
    if txt_hash in visited_content:
        return True
    else:
        visited_content.add(txt_hash)
        return False
