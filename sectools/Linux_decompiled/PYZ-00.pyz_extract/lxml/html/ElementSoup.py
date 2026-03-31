
'''Legacy interface to the BeautifulSoup HTML parser.
'''
__all__ = [
    'parse',
    'convert_tree']
from soupparser import convert_tree, parse as _parse

def parse(file, beautifulsoup, makeelement = (None, None)):
    root = _parse(file, beautifulsoup, makeelement, **('beautifulsoup', 'makeelement'))
    return root.getroot()

