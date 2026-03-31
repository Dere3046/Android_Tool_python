
__doc__ = '\nAn interface to html5lib that mimics the lxml.html interface.\n'
import sys
import string
from html5lib import HTMLParser as _HTMLParser
from html5lib.treebuilders.etree_lxml import TreeBuilder
from lxml import etree
from lxml.html import Element, XHTML_NAMESPACE, _contains_block_level_tag
# WARNING: Decompyle incomplete
