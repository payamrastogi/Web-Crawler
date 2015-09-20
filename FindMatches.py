import hashlib

visited_content = set()

def txt_md5(txt):
    return hashlib.md5(txt).hexdigest()

def is_duplicate_content(txt):
    txt_hash = txt_md5(txt.encode('utf8'))
    if txt_hash in visited_content:
        return False
    else:
        visited_content.add(txt_hash)
        return True
