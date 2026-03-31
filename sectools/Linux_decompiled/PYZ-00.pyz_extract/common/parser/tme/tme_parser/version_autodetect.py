
from functools import wraps
from typing import Dict, cast
from common.data.data import comma_separated_string
from common.parser.tme.tme_parser.defines import TagList, SharedState
from common.parser.tme.tme_parser.exceptions import ProtocolParsingError, ProtocolVersionError, ProtocolError

def parser_autodetect(tme_grammar_versions = None, parser_number = None):
    '''
    In the case of the tag exception, looks up the correct parser version for that tag.
    As a second stage, anticipates the version exception to adjust the correct parser version.
    '''
    
    def wrapper(func = None):
        
        def wrapped(*args, **kwargs):
            pass
        # WARNING: Decompyle incomplete

        wrapped = None(wrapped)
        return wrapped

    return wrapper

