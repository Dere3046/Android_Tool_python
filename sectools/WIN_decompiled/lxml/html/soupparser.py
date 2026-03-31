
__doc__ = 'External interface to the BeautifulSoup HTML parser.\n'
__all__ = [
    'fromstring',
    'parse',
    'convert_tree']
import re
from lxml import etree, html
# WARNING: Decompyle incomplete
