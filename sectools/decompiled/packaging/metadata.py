
from __future__ import annotations
import email.feedparser as email
import email.header as email
import email.message as email
import email.parser as email
import email.policy as email
import pathlib
import sys
import typing
from typing import Any, Callable, Generic, Literal, TypedDict, cast
from  import licenses, requirements, specifiers, utils
from  import version as version_module
from licenses import NormalizedLicenseExpression
T = typing.TypeVar('T')
if sys.version_info >= (3, 11):
    ExceptionGroup = ExceptionGroup
else:
    
    class ExceptionGroup(Exception):
        exceptions: 'list[Exception]' = 'A minimal implementation of :external:exc:`ExceptionGroup` from Python 3.11.\n\n        If :external:exc:`ExceptionGroup` is already defined by Python itself,\n        that version is used instead.\n        '
        
        def __init__(self = None, message = None, exceptions = None):
            self.message = message
            self.exceptions = exceptions

        
        def __repr__(self = None):
            return f'''{self.__class__.__name__}({self.message!r}, {self.exceptions!r})'''



class InvalidMetadata(ValueError):
    field: 'str' = 'A metadata field contains invalid data.'
    
    def __init__(self = None, field = None, message = None):
        self.field = field
        super().__init__(message)

    __classcell__ = None

RawMetadata = <NODE:27>((lambda : license_files: 'list[str]' = 'A dictionary of raw core metadata.\n\n    Each field in core metadata maps to a key of this dictionary (when data is\n    provided). The key is lower-case and underscores are used instead of dashes\n    compared to the equivalent core metadata field. Any core metadata field that\n    can be specified multiple times or can hold multiple values in a single\n    field have a key with a plural name. See :class:`Metadata` whose attributes\n    match the keys of this dictionary.\n\n    Core metadata fields that can be specified multiple times are stored as a\n    list or dict depending on which is appropriate for the field. Any fields\n    which hold multiple values in a single field are stored as a list.\n\n    '), 'RawMetadata', TypedDict, False, **('total',))
_STRING_FIELDS = {
    'author_email',
    'description_content_type',
    'requires_python',
    'description',
    'maintainer',
    'metadata_version',
    'maintainer_email',
    'summary',
    'author',
    'home_page',
    'version',
    'name',
    'license_expression',
    'download_url',
    'license'}
_LIST_FIELDS = {
    'platforms',
    'obsoletes',
    'dynamic',
    'classifiers',
    'license_files',
    'provides_extra',
    'supported_platforms',
    'obsoletes_dist',
    'provides',
    'requires_external',
    'requires_dist',
    'requires',
    'provides_dist'}
_DICT_FIELDS = {
    'project_urls'}

def _parse_keywords(data = None):
    '''Split a string of comma-separated keywords into a list of keywords.'''
    return (lambda .0: [ k.strip() for k in .0 ])(data.split(','))


def _parse_project_urls(data = None):
    '''Parse a list of label/URL string pairings separated by a comma.'''
    urls = { }
    for pair in data:
        parts = (lambda .0: [ p.strip() for p in .0 ])(pair.split(',', 1))
        parts.extend([
            ''] * max(0, 2 - len(parts)))
        (label, url) = parts
        if label in urls:
            raise KeyError('duplicate labels in project urls')
        urls[label] = None
    return urls


def _get_payload(msg = None, source = None):
    '''Get the body of the message.'''
    pass
# WARNING: Decompyle incomplete

# WARNING: Decompyle incomplete
