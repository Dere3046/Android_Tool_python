
__doc__ = 'The ``lxml.html`` tool set for HTML handling.\n'
from __future__ import absolute_import
__all__ = [
    'document_fromstring',
    'fragment_fromstring',
    'fragments_fromstring',
    'fromstring',
    'tostring',
    'Element',
    'defs',
    'open_in_browser',
    'submit_form',
    'find_rel_links',
    'find_class',
    'make_links_absolute',
    'resolve_base_href',
    'iterlinks',
    'rewrite_links',
    'parse']
import copy
import sys
import re
from functools import partial
# WARNING: Decompyle incomplete
