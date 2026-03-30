
import functools
import operator
import itertools
from extern.jaraco.text import yield_lines
from extern.jaraco.functools import pass_none
from _importlib import metadata
from _itertools import ensure_unique
from extern.more_itertools import consume

def ensure_valid(ep):
    '''
    Exercise one of the dynamic properties to trigger
    the pattern match.
    '''
    ep.extras


def load_group(value, group):
    '''
    Given a value of an entry point or series of entry points,
    return each as an EntryPoint.
    '''
    lines = yield_lines(value)
    text = f'''[{group}]\n''' + '\n'.join(lines)
    return metadata.EntryPoints._from_text(text)


def by_group_and_name(ep):
    return (ep.group, ep.name)


def validate(eps = None):
    '''
    Ensure entry points are unique by group and name and validate each.
    '''
    consume(map(ensure_valid, ensure_unique(eps, by_group_and_name, **('key',))))
    return eps


def load(eps):
    '''
    Given a Distribution.entry_points, produce EntryPoints.
    '''
    groups = itertools.chain.from_iterable((lambda .0: for group, value in .0:
load_group(value, group))(eps.items()))
    return validate(metadata.EntryPoints(groups))

load = functools.singledispatch(load)

def _(eps):
    """
    >>> ep, = load('[console_scripts]\\nfoo=bar')
    >>> ep.group
    'console_scripts'
    >>> ep.name
    'foo'
    >>> ep.value
    'bar'
    """
    return validate(metadata.EntryPoints(metadata.EntryPoints._from_text(eps)))

_ = load.register(str)(_)
load.register(type(None), (lambda x: x))

def render(eps = None):
    by_group = operator.attrgetter('group')
    groups = itertools.groupby(sorted(eps, by_group, **('key',)), by_group)
    return '\n'.join((lambda .0: for group, items in .0:
f'''[{group}]\n{render_items(items)}\n''')(groups))

render = None(render)

def render_items(eps):
    return '\n'.join((lambda .0: for ep in .0:
f'''{ep.name} = {ep.value}''')(sorted(eps)))

