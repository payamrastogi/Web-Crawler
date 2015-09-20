from urlparse import urlparse
from os.path import splitext

seen_urls = set()

def is_unique(website):
    # Strip of the last bit
    parsed = urlparse(website)
    if parsed is None or parsed.hostname:
        return False
    url = parsed.hostname + str(parsed.path)
    if url in seen_urls:
        return False
    seen_urls.add(url)
    return True

def get_ext(url):
    """Return the filename extension from url, or ''."""
    parsed = urlparse(url)
    if parsed is None:
        return None
    root, ext = splitext(parsed.path)
    return ext

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
        '.css', '.pdf', '.doc', '.exe', '.bin', '.rss', '.zip', '.rar',
    ]
    ext = get_ext(url)

    if ext in IGNORED_EXTENSIONS:
        return False
    return True

def is_valid_url(url):
    return is_unique(url) and is_valid_extention(url)

