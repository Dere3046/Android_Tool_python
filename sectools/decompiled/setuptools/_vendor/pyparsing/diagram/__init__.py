
import railroad
import pyparsing
import typing
from typing import List, NamedTuple, Generic, TypeVar, Dict, Callable, Set, Iterable
from jinja2 import Template
from io import StringIO
import inspect
jinja2_template_source = '<!DOCTYPE html>\n<html>\n<head>\n    {% if not head %}\n        <style type="text/css">\n            .railroad-heading {\n                font-family: monospace;\n            }\n        </style>\n    {% else %}\n        {{ head | safe }}\n    {% endif %}\n</head>\n<body>\n{{ body | safe }}\n{% for diagram in diagrams %}\n    <div class="railroad-group">\n        <h1 class="railroad-heading">{{ diagram.title }}</h1>\n        <div class="railroad-description">{{ diagram.text }}</div>\n        <div class="railroad-svg">\n            {{ diagram.svg }}\n        </div>\n    </div>\n{% endfor %}\n</body>\n</html>\n'
template = Template(jinja2_template_source)
NamedDiagram = NamedTuple('NamedDiagram', [
    ('name', str),
    ('diagram', typing.Optional[railroad.DiagramItem]),
    ('index', int)])
T = TypeVar('T')

class EachItem(railroad.Group):
    '''
    Custom railroad item to compose a:
    - Group containing a
      - OneOrMore containing a
        - Choice of the elements in the Each
    with the group label indicating that all must be matched
    '''
    all_label = '[ALL]'
    
    def __init__(self = None, *items):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None


class AnnotatedItem(railroad.Group):
    '''
    Simple subclass of Group that creates an annotation label
    '''
    
    def __init__(self = None, label = None, item = None):
        super().__init__(item, '[{}]'.format(label) if label else label, **('item', 'label'))

    __classcell__ = None


def EditablePartial():
    '''EditablePartial'''
    __doc__ = "\n    Acts like a functools.partial, but can be edited. In other words, it represents a type that hasn't yet been\n    constructed.\n    "
    
    def __init__(self = None, func = None, args = None, kwargs = ('func', Callable[(..., T)], 'args', list, 'kwargs', dict)):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    
    def from_call(cls = None, func = None, *args, **kwargs):
        '''
        If you call this function in the same way that you would call the constructor, it will store the arguments
        as you expect. For example EditablePartial.from_call(Fraction, 1, 3)() == Fraction(1, 3)
        '''
        return EditablePartial(func, list(args), kwargs, **('func', 'args', 'kwargs'))

    from_call = None(from_call)
    
    def name(self):
        return self.kwargs['name']

    name = property(name)
    
    def __call__(self = None):
        '''
        Evaluate the partial and return the result
        '''
        args = self.args.copy()
        kwargs = self.kwargs.copy()
        arg_spec = inspect.getfullargspec(self.func)
        if arg_spec.varargs in self.kwargs:
            args += kwargs.pop(arg_spec.varargs)
    # WARNING: Decompyle incomplete


EditablePartial = <NODE:27>(EditablePartial, 'EditablePartial', Generic[T])

def railroad_to_html(diagrams = None, **kwargs):
    '''
    Given a list of NamedDiagram, produce a single HTML string that visualises those diagrams
    :params kwargs: kwargs to be passed in to the template
    '''
    data = []
    for diagram in diagrams:
        if diagram.diagram is None:
            continue
        io = StringIO()
        diagram.diagram.writeSvg(io.write)
        title = diagram.name
        if diagram.index == 0:
            title += ' (root)'
        data.append({
            'title': title,
            'text': '',
            'svg': io.getvalue() })
# WARNING: Decompyle incomplete


def resolve_partial(partial = None):
    '''
    Recursively resolves a collection of Partials into whatever type they are
    '''
    if isinstance(partial, EditablePartial):
        partial.args = resolve_partial(partial.args)
        partial.kwargs = resolve_partial(partial.kwargs)
        return partial()
    if None(partial, list):
        return (lambda .0: [ resolve_partial(x) for x in .0 ])(partial)
    if None(partial, dict):
        return (lambda .0: pass# WARNING: Decompyle incomplete
)(partial.items())


def to_railroad(element = None, diagram_kwargs = None, vertical = None, show_results_names = (None, 3, False, False), show_groups = ('element', pyparsing.ParserElement, 'diagram_kwargs', typing.Optional[dict], 'vertical', int, 'show_results_names', bool, 'show_groups', bool, 'return', List[NamedDiagram])):
    '''
    Convert a pyparsing element tree into a list of diagrams. This is the recommended entrypoint to diagram
    creation if you want to access the Railroad tree before it is converted to HTML
    :param element: base element of the parser being diagrammed
    :param diagram_kwargs: kwargs to pass to the Diagram() constructor
    :param vertical: (optional) - int - limit at which number of alternatives should be
       shown vertically instead of horizontally
    :param show_results_names - bool to indicate whether results name annotations should be
       included in the diagram
    :param show_groups - bool to indicate whether groups should be highlighted with an unlabeled
       surrounding box
    '''
    if not diagram_kwargs:
        pass
    lookup = ConverterState({ }, **('diagram_kwargs',))
    _to_diagram_element(element, lookup, None, vertical, show_results_names, show_groups, **('lookup', 'parent', 'vertical', 'show_results_names', 'show_groups'))
    root_id = id(element)
    if root_id in lookup:
        if not element.customName:
            lookup[root_id].name = ''
        lookup[root_id].mark_for_extraction(root_id, lookup, True, **('force',))
    diags = list(lookup.diagrams.values())
    if len(diags) > 1:
        seen = set()
        deduped_diags = []
        for d in diags:
            if d.name == '...':
                continue
            if d.name is not None and d.name not in seen:
                seen.add(d.name)
                deduped_diags.append(d)
        resolved = (lambda .0: [ resolve_partial(partial) for partial in .0 ])(deduped_diags)
    else:
        resolved = (lambda .0: [ resolve_partial(partial) for partial in .0 ])(diags)
    return sorted(resolved, (lambda diag: diag.index), **('key',))


def _should_vertical(specification = None, exprs = None):
    '''
    Returns true if we should return a vertical list of elements
    '''
    if specification is None:
        return False
    return None(_visible_exprs(exprs)) >= specification


class ElementState:
    '''
    State recorded for an individual pyparsing Element
    '''
    
    def __init__(self, element, converted = None, parent = None, number = None, name = (None, None), parent_index = ('element', pyparsing.ParserElement, 'converted', EditablePartial, 'parent', EditablePartial, 'number', int, 'name', str, 'parent_index', typing.Optional[int])):
        self.element = element
        self.name = name
        self.converted = converted
        self.parent = parent
        self.number = number
        self.parent_index = parent_index
        self.extract = False
        self.complete = False

    
    def mark_for_extraction(self = None, el_id = None, state = None, name = (None, False), force = ('el_id', int, 'state', 'ConverterState', 'name', str, 'force', bool)):
        """
        Called when this instance has been seen twice, and thus should eventually be extracted into a sub-diagram
        :param el_id: id of the element
        :param state: element/diagram state tracker
        :param name: name to use for this element's text
        :param force: If true, force extraction now, regardless of the state of this. Only useful for extracting the
        root element when we know we're finished
        """
        self.extract = True
        if not self.name:
            if name:
                self.name = name
            elif self.element.customName:
                self.name = self.element.customName
            else:
                self.name = ''
        if force or self.complete or _worth_extracting(self.element):
            state.extract_into_diagram(el_id)
            return None
        return None



class ConverterState:
    '''
    Stores some state that persists between recursions into the element tree
    '''
    
    def __init__(self = None, diagram_kwargs = None):
        self._element_diagram_states = { }
        self.diagrams = { }
        self.unnamed_index = 1
        self.index = 0
        if not diagram_kwargs:
            pass
        self.diagram_kwargs = { }
        self.extracted_diagram_names = set()

    
    def __setitem__(self = None, key = None, value = None):
        self._element_diagram_states[key] = value

    
    def __getitem__(self = None, key = None):
        return self._element_diagram_states[key]

    
    def __delitem__(self = None, key = None):
        del self._element_diagram_states[key]

    
    def __contains__(self = None, key = None):
        return key in self._element_diagram_states

    
    def generate_unnamed(self = None):
        '''
        Generate a number used in the name of an otherwise unnamed diagram
        '''
        self.unnamed_index += 1
        return self.unnamed_index

    
    def generate_index(self = None):
        '''
        Generate a number used to index a diagram
        '''
        self.index += 1
        return self.index

    
    def extract_into_diagram(self = None, el_id = None):
        '''
        Used when we encounter the same token twice in the same tree. When this
        happens, we replace all instances of that token with a terminal, and
        create a new subdiagram for the token
        '''
        position = self[el_id]
        if position.parent:
            ret = EditablePartial.from_call(railroad.NonTerminal, position.name, **('text',))
            if 'item' in position.parent.kwargs:
                position.parent.kwargs['item'] = ret
            elif 'items' in position.parent.kwargs:
                position.parent.kwargs['items'][position.parent_index] = ret
        if position.converted.func == railroad.Group:
            content = position.converted.kwargs['item']
        else:
            content = position.converted
    # WARNING: Decompyle incomplete



def _worth_extracting(element = None):
    '''
    Returns true if this element is worth having its own sub-diagram. Simply, if any of its children
    themselves have children, then its complex enough to extract
    '''
    children = element.recurse()
    return any((lambda .0: for child in .0:
child.recurse())(children))


def _apply_diagram_item_enhancements(fn):
    '''
    decorator to ensure enhancements to a diagram item (such as results name annotations)
    get applied on return from _to_diagram_element (we do this since there are several
    returns in _to_diagram_element)
    '''
    
    def _inner(element = None, parent = None, lookup = None, vertical = None, index = None, name_hint = None, show_results_names = None, show_groups = None):
        ret = fn(element, parent, lookup, vertical, index, name_hint, show_results_names, show_groups)
        if show_results_names and ret is not None:
            element_results_name = element.resultsName
            if element_results_name:
                element_results_name += '' if element.modalResults else '*'
                ret = EditablePartial.from_call(railroad.Group, ret, element_results_name, **('item', 'label'))
        return ret

    return _inner


def _visible_exprs(exprs = None):
    non_diagramming_exprs = (pyparsing.ParseElementEnhance, pyparsing.PositionToken, pyparsing.And._ErrorStop)
    return (lambda .0 = None: [ e for e in .0 if isinstance(e, non_diagramming_exprs) ])(exprs)


def _to_diagram_element(element, parent, lookup, vertical = None, index = None, name_hint = _apply_diagram_item_enhancements, show_results_names = (None, None, 0, None, False, False), show_groups = ('element', pyparsing.ParserElement, 'parent', typing.Optional[EditablePartial], 'lookup', ConverterState, 'vertical', int, 'index', int, 'name_hint', str, 'show_results_names', bool, 'show_groups', bool, 'return', typing.Optional[EditablePartial])):
    """
    Recursively converts a PyParsing Element to a railroad Element
    :param lookup: The shared converter state that keeps track of useful things
    :param index: The index of this element within the parent
    :param parent: The parent of this element in the output tree
    :param vertical: Controls at what point we make a list of elements vertical. If this is an integer (the default),
    it sets the threshold of the number of items before we go vertical. If True, always go vertical, if False, never
    do so
    :param name_hint: If provided, this will override the generated name
    :param show_results_names: bool flag indicating whether to add annotations for results names
    :returns: The converted version of the input element, but as a Partial that hasn't yet been constructed
    :param show_groups: bool flag indicating whether to show groups using bounding box
    """
    exprs = element.recurse()
    if not name_hint and element.customName:
        pass
    name = element.__class__.__name__
    el_id = id(element)
    element_results_name = element.resultsName
    if element.customName and isinstance(element, (pyparsing.Located,)) and exprs:
        if not exprs[0].customName:
            propagated_name = name
        else:
            propagated_name = None
        return _to_diagram_element(element.expr, parent, lookup, vertical, index, propagated_name, show_results_names, show_groups, **('parent', 'lookup', 'vertical', 'index', 'name_hint', 'show_results_names', 'show_groups'))
    if None(element):
        if el_id in lookup:
            looked_up = lookup[el_id]
            looked_up.mark_for_extraction(el_id, lookup, name_hint, **('name',))
            ret = EditablePartial.from_call(railroad.NonTerminal, looked_up.name, **('text',))
            return ret
        if None in lookup.diagrams:
            ret = EditablePartial.from_call(railroad.NonTerminal, lookup.diagrams[el_id].kwargs['name'], **('text',))
            return ret
        if None(element, pyparsing.And):
            if not exprs:
                return None
            if None(set((lambda .0: for e in .0:
(e.name, e.resultsName))(exprs))) == 1:
                ret = EditablePartial.from_call(railroad.OneOrMore, '', str(len(exprs)), **('item', 'repeat'))
            elif _should_vertical(vertical, exprs):
                ret = EditablePartial.from_call(railroad.Stack, [], **('items',))
            else:
                ret = EditablePartial.from_call(railroad.Sequence, [], **('items',))
        elif isinstance(element, (pyparsing.Or, pyparsing.MatchFirst)):
            if not exprs:
                return None
            if None(vertical, exprs):
                ret = EditablePartial.from_call(railroad.Choice, 0, [], **('items',))
            else:
                ret = EditablePartial.from_call(railroad.HorizontalChoice, [], **('items',))
        elif isinstance(element, pyparsing.Each):
            if not exprs:
                return None
            ret = None.from_call(EachItem, [], **('items',))
        elif isinstance(element, pyparsing.NotAny):
            ret = EditablePartial.from_call(AnnotatedItem, 'NOT', '', **('label', 'item'))
        elif isinstance(element, pyparsing.FollowedBy):
            ret = EditablePartial.from_call(AnnotatedItem, 'LOOKAHEAD', '', **('label', 'item'))
        elif isinstance(element, pyparsing.PrecededBy):
            ret = EditablePartial.from_call(AnnotatedItem, 'LOOKBEHIND', '', **('label', 'item'))
        elif isinstance(element, pyparsing.Group):
            if show_groups:
                ret = EditablePartial.from_call(AnnotatedItem, '', '', **('label', 'item'))
            else:
                ret = EditablePartial.from_call(railroad.Group, '', '', **('label', 'item'))
        elif isinstance(element, pyparsing.TokenConverter):
            ret = EditablePartial.from_call(AnnotatedItem, type(element).__name__.lower(), '', **('label', 'item'))
        elif isinstance(element, pyparsing.Opt):
            ret = EditablePartial.from_call(railroad.Optional, '', **('item',))
        elif isinstance(element, pyparsing.OneOrMore):
            ret = EditablePartial.from_call(railroad.OneOrMore, '', **('item',))
        elif isinstance(element, pyparsing.ZeroOrMore):
            ret = EditablePartial.from_call(railroad.ZeroOrMore, '', **('item',))
        elif isinstance(element, pyparsing.Group):
            ret = EditablePartial.from_call(railroad.Group, None, element_results_name, **('item', 'label'))
        elif not isinstance(element, pyparsing.Empty) and element.customName:
            ret = None
        elif len(exprs) > 1:
            ret = EditablePartial.from_call(railroad.Sequence, [], **('items',))
        elif not len(exprs) > 0 and element_results_name:
            ret = EditablePartial.from_call(railroad.Group, '', name, **('item', 'label'))
        else:
            terminal = EditablePartial.from_call(railroad.Terminal, element.defaultName)
            ret = terminal
    if ret is None:
        return None
    lookup[el_id] = None(element, ret, parent, index, lookup.generate_index(), **('element', 'converted', 'parent', 'parent_index', 'number'))
    if element.customName:
        lookup[el_id].mark_for_extraction(el_id, lookup, element.customName)
    i = 0
    for expr in exprs:
        if 'items' in ret.kwargs:
            ret.kwargs['items'].insert(i, None)
        item = _to_diagram_element(expr, ret, lookup, vertical, i, show_results_names, show_groups, **('parent', 'lookup', 'vertical', 'index', 'show_results_names', 'show_groups'))
        if item is not None:
            if 'item' in ret.kwargs:
                ret.kwargs['item'] = item
                continue
            if 'items' in ret.kwargs:
                ret.kwargs['items'][i] = item
                i += 1
            continue
        if 'items' in ret.kwargs:
            del ret.kwargs['items'][i]
    if ret:
        if ('items' in ret.kwargs or len(ret.kwargs['items']) == 0 or 'item' in ret.kwargs) and ret.kwargs['item'] is None:
            ret = EditablePartial.from_call(railroad.Terminal, name)
    if el_id in lookup:
        lookup[el_id].complete = True
    if el_id in lookup and lookup[el_id].extract and lookup[el_id].complete:
        lookup.extract_into_diagram(el_id)
        if ret is not None:
            ret = EditablePartial.from_call(railroad.NonTerminal, lookup.diagrams[el_id].kwargs['name'], **('text',))
    return ret

_to_diagram_element = None(_to_diagram_element)
