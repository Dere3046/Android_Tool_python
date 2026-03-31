
import railroad
import pyparsing
from pkg_resources import resource_filename
from typing import List, Optional, NamedTuple, Generic, TypeVar, Dict, Callable, Set, Iterable
from jinja2 import Template
from io import StringIO
import inspect
with open(resource_filename(__name__, 'template.jinja2'), 'utf-8', **('encoding',)) as fp:
    template = Template(fp.read())
    None(None, None, None)
# WARNING: Decompyle incomplete
