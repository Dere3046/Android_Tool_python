
__doc__ = '\nGeneral functions for HTML manipulation.\n'
import re as _re
from html.entities import html5 as _html5
__all__ = [
    'escape',
    'unescape']

def escape(s, quote = (True,)):
    '''
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (\') characters are also
    translated.
    '''
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    if quote:
        s = s.replace('"', '&quot;')
        s = s.replace("'", '&#x27;')
    return s

# WARNING: Decompyle incomplete
