
from collections.abc import MutableMapping, Mapping, MutableSequence, Iterator
import pprint
from weakref import ref as wkref
from typing import Tuple, Any
str_type: Tuple[(type, ...)] = (str, bytes)
_generator_type = type((lambda .0: for _ in .0:
_)(()))

class _ParseResultsWithOffset:
    __slots__ = [
        'tup']
    
    def __init__(self, p1, p2):
        self.tup = (p1, p2)

    
    def __getitem__(self, i):
        return self.tup[i]

    
    def __getstate__(self):
        return self.tup

    
    def __setstate__(self, *args):
        self.tup = args[0]



class ParseResults:
    '''Structured parse results, to provide multiple means of access to
    the parsed data:

    - as a list (``len(results)``)
    - by list index (``results[0], results[1]``, etc.)
    - by attribute (``results.<results_name>`` - see :class:`ParserElement.set_results_name`)

    Example::

        integer = Word(nums)
        date_str = (integer.set_results_name("year") + \'/\'
                    + integer.set_results_name("month") + \'/\'
                    + integer.set_results_name("day"))
        # equivalent form:
        # date_str = (integer("year") + \'/\'
        #             + integer("month") + \'/\'
        #             + integer("day"))

        # parse_string returns a ParseResults object
        result = date_str.parse_string("1999/12/31")

        def test(s, fn=repr):
            print("{} -> {}".format(s, fn(eval(s))))
        test("list(result)")
        test("result[0]")
        test("result[\'month\']")
        test("result.day")
        test("\'month\' in result")
        test("\'minutes\' in result")
        test("result.dump()", str)

    prints::

        list(result) -> [\'1999\', \'/\', \'12\', \'/\', \'31\']
        result[0] -> \'1999\'
        result[\'month\'] -> \'12\'
        result.day -> \'31\'
        \'month\' in result -> True
        \'minutes\' in result -> False
        result.dump() -> [\'1999\', \'/\', \'12\', \'/\', \'31\']
        - day: \'31\'
        - month: \'12\'
        - year: \'1999\'
    '''
    _null_values: Tuple[(Any, ...)] = (None, [], '', ())
    __slots__ = [
        '_name',
        '_parent',
        '_all_names',
        '_modal',
        '_toklist',
        '_tokdict',
        '__weakref__']
    
    class List(list):
        __qualname__ = 'ParseResults.List'
        __doc__ = '\n        Simple wrapper class to distinguish parsed list results that should be preserved\n        as actual Python lists, instead of being converted to :class:`ParseResults`:\n\n            LBRACK, RBRACK = map(pp.Suppress, "[]")\n            element = pp.Forward()\n            item = ppc.integer\n            element_list = LBRACK + pp.delimited_list(element) + RBRACK\n\n            # add parse actions to convert from ParseResults to actual Python collection types\n            def as_python_list(t):\n                return pp.ParseResults.List(t.as_list())\n            element_list.add_parse_action(as_python_list)\n\n            element <<= item | element_list\n\n            element.run_tests(\'\'\'\n                100\n                [2,3,4]\n                [[2, 1],3,4]\n                [(2, 1),3,4]\n                (2,3,4)\n                \'\'\', post_parse=lambda s, r: (r[0], type(r[0])))\n\n        prints:\n\n            100\n            (100, <class \'int\'>)\n\n            [2,3,4]\n            ([2, 3, 4], <class \'list\'>)\n\n            [[2, 1],3,4]\n            ([[2, 1], 3, 4], <class \'list\'>)\n\n        (Used internally by :class:`Group` when `aslist=True`.)\n        '
        
        def __new__(cls, contained = (None,)):
            if contained is None:
                contained = []
            if not isinstance(contained, list):
                raise TypeError('{} may only be constructed with a list, not {}'.format(cls.__name__, type(contained).__name__))
            return None.__new__(cls)


    
    def __new__(cls, toklist, name = (None, None), **kwargs):
        if isinstance(toklist, ParseResults):
            return toklist
        self = None.__new__(cls)
        self._name = None
        self._parent = None
        self._all_names = set()
        if toklist is None:
            self._toklist = []
        elif isinstance(toklist, (list, _generator_type)):
            self._toklist = [
                toklist[:]] if isinstance(toklist, ParseResults.List) else list(toklist)
        else:
            self._toklist = [
                toklist]
        self._tokdict = dict()
        return self

    
    def __init__(self, toklist, name, asList, modal, isinstance = (None, None, True, True, isinstance)):
        self._modal = modal
        if name is not None or name != '':
            if isinstance(name, int):
                name = str(name)
            if not modal:
                self._all_names = {
                    name}
            self._name = name
            if toklist not in self._null_values:
                if isinstance(toklist, (str_type, type)):
                    toklist = [
                        toklist]
                if asList:
                    if isinstance(toklist, ParseResults):
                        self[name] = _ParseResultsWithOffset(ParseResults(toklist._toklist), 0)
                    else:
                        self[name] = _ParseResultsWithOffset(ParseResults(toklist[0]), 0)
                    self[name]._name = name
                    return None
                self[name] = toklist[0]
            return None
    # WARNING: Decompyle incomplete

    
    def __getitem__(self, i):
        if isinstance(i, (int, slice)):
            return self._toklist[i]
        if None not in self._all_names:
            return self._tokdict[i][-1][0]
        return None((lambda .0: [ v[0] for v in .0 ])(self._tokdict[i]))

    
    def __setitem__(self, k, v, isinstance = (isinstance,)):
        if isinstance(v, _ParseResultsWithOffset):
            self._tokdict[k] = self._tokdict.get(k, list()) + [
                v]
            sub = v[0]
        elif isinstance(k, (int, slice)):
            self._toklist[k] = v
            sub = v
        else:
            self._tokdict[k] = self._tokdict.get(k, list()) + [
                _ParseResultsWithOffset(v, 0)]
            sub = v
        if isinstance(sub, ParseResults):
            sub._parent = wkref(self)
            return None

    
    def __delitem__(self, i):
        pass
    # WARNING: Decompyle incomplete

    
    def __contains__(self = None, k = None):
        return k in self._tokdict

    
    def __len__(self = None):
        return len(self._toklist)

    
    def __bool__(self = None):
        if not self._toklist:
            pass
        return not (not (self._tokdict))

    
    def __iter__(self = None):
        return iter(self._toklist)

    
    def __reversed__(self = None):
        return iter(self._toklist[::-1])

    
    def keys(self):
        return iter(self._tokdict)

    
    def values(self):
        return (lambda .0 = None: for k in .0:
self[k])(self.keys())

    
    def items(self):
        return (lambda .0 = None: for k in .0:
(k, self[k]))(self.keys())

    
    def haskeys(self = None):
        '''
        Since ``keys()`` returns an iterator, this method is helpful in bypassing
        code that looks for the existence of any defined results names.'''
        return bool(self._tokdict)

    
    def pop(self, *args, **kwargs):
        '''
        Removes and returns item at specified index (default= ``last``).
        Supports both ``list`` and ``dict`` semantics for ``pop()``. If
        passed no argument or an integer argument, it will use ``list``
        semantics and pop tokens from the list of parsed tokens. If passed
        a non-integer argument (most likely a string), it will use ``dict``
        semantics and pop the corresponding value from any defined results
        names. A second default return value argument is supported, just as in
        ``dict.pop()``.

        Example::

            numlist = Word(nums)[...]
            print(numlist.parse_string("0 123 321")) # -> [\'0\', \'123\', \'321\']

            def remove_first(tokens):
                tokens.pop(0)
            numlist.add_parse_action(remove_first)
            print(numlist.parse_string("0 123 321")) # -> [\'123\', \'321\']

            label = Word(alphas)
            patt = label("LABEL") + Word(nums)[1, ...]
            print(patt.parse_string("AAB 123 321").dump())

            # Use pop() in a parse action to remove named result (note that corresponding value is not
            # removed from list form of results)
            def remove_LABEL(tokens):
                tokens.pop("LABEL")
                return tokens
            patt.add_parse_action(remove_LABEL)
            print(patt.parse_string("AAB 123 321").dump())

        prints::

            [\'AAB\', \'123\', \'321\']
            - LABEL: \'AAB\'

            [\'AAB\', \'123\', \'321\']
        '''
        if not args:
            args = [
                -1]
        for k, v in kwargs.items():
            if k == 'default':
                args = (args[0], v)
                continue
            raise TypeError('pop() got an unexpected keyword argument {!r}'.format(k))
            if isinstance(args[0], int) and len(args) == 1 or args[0] in self:
                index = args[0]
                ret = self[index]
                del self[index]
                return ret
            defaultvalue = None[1]
            return defaultvalue

    
    def get(self, key, default_value = (None,)):
        '''
        Returns named result matching the given key, or if there is no
        such name, then returns the given ``default_value`` or ``None`` if no
        ``default_value`` is specified.

        Similar to ``dict.get()``.

        Example::

            integer = Word(nums)
            date_str = integer("year") + \'/\' + integer("month") + \'/\' + integer("day")

            result = date_str.parse_string("1999/12/31")
            print(result.get("year")) # -> \'1999\'
            print(result.get("hour", "not specified")) # -> \'not specified\'
            print(result.get("hour")) # -> None
        '''
        if key in self:
            return self[key]

    
    def insert(self, index, ins_string):
        '''
        Inserts new element at location index in the list of parsed tokens.

        Similar to ``list.insert()``.

        Example::

            numlist = Word(nums)[...]
            print(numlist.parse_string("0 123 321")) # -> [\'0\', \'123\', \'321\']

            # use a parse action to insert the parse location in the front of the parsed results
            def insert_locn(locn, tokens):
                tokens.insert(0, locn)
            numlist.add_parse_action(insert_locn)
            print(numlist.parse_string("0 123 321")) # -> [0, \'0\', \'123\', \'321\']
        '''
        self._toklist.insert(index, ins_string)
        for name, occurrences in self._tokdict.items():
            for value, position in enumerate(occurrences):
                occurrences[k] = _ParseResultsWithOffset(value, position + (position > index))

    
    def append(self, item):
        '''
        Add single element to end of ``ParseResults`` list of elements.

        Example::

            numlist = Word(nums)[...]
            print(numlist.parse_string("0 123 321")) # -> [\'0\', \'123\', \'321\']

            # use a parse action to compute the sum of the parsed integers, and add it to the end
            def append_sum(tokens):
                tokens.append(sum(map(int, tokens)))
            numlist.add_parse_action(append_sum)
            print(numlist.parse_string("0 123 321")) # -> [\'0\', \'123\', \'321\', 444]
        '''
        self._toklist.append(item)

    
    def extend(self, itemseq):
        '''
        Add sequence of elements to end of ``ParseResults`` list of elements.

        Example::

            patt = Word(alphas)[1, ...]

            # use a parse action to append the reverse of the matched strings, to make a palindrome
            def make_palindrome(tokens):
                tokens.extend(reversed([t[::-1] for t in tokens]))
                return \'\'.join(tokens)
            patt.add_parse_action(make_palindrome)
            print(patt.parse_string("lskdj sdlkjf lksd")) # -> \'lskdjsdlkjflksddsklfjkldsjdksl\'
        '''
        if isinstance(itemseq, ParseResults):
            self.__iadd__(itemseq)
            return None
        None._toklist.extend(itemseq)

    
    def clear(self):
        '''
        Clear all elements and results names.
        '''
        del self._toklist[:]
        self._tokdict.clear()

    
    def __getattr__(self, name):
        pass
    # WARNING: Decompyle incomplete

    
    def __add__(self = None, other = None):
        ret = self.copy()
        ret += other
        return ret

    
    def __iadd__(self = None, other = None):
        if other._tokdict:
            offset = len(self._toklist)
            
            addoffset = lambda a = None: if a < 0:
offsetNone + offset
            otheritems = other._tokdict.items()
            otherdictitems = (lambda .0 = None: [ (k, _ParseResultsWithOffset(v[0], addoffset(v[1]))) for k, vlist in .0 for v in vlist ])(otheritems)
            for k, v in otherdictitems:
                self[k] = v
                if isinstance(v[0], ParseResults):
                    v[0]._parent = wkref(self)
        self._toklist += other._toklist
        self._all_names |= other._all_names
        return self

    
    def __radd__(self = None, other = None):
        if isinstance(other, int) and other == 0:
            return self.copy()
        return None + self

    
    def __repr__(self = None):
        return '{}({!r}, {})'.format(type(self).__name__, self._toklist, self.as_dict())

    
    def __str__(self = None):
        return '[' + ', '.join((lambda .0: for i in .0:
passcontinuestr(i)[repr(i)])(self._toklist)) + ']'

    
    def _asStringList(self, sep = ('',)):
        out = []
        for item in self._toklist:
            if out and sep:
                out.append(sep)
            if isinstance(item, ParseResults):
                out += item._asStringList()
                continue
            out.append(str(item))
        return out

    
    def as_list(self = None):
        '''
        Returns the parse results as a nested list of matching tokens, all converted to strings.

        Example::

            patt = Word(alphas)[1, ...]
            result = patt.parse_string("sldkj lsdkj sldkj")
            # even though the result prints in string-like form, it is actually a pyparsing ParseResults
            print(type(result), result) # -> <class \'pyparsing.ParseResults\'> [\'sldkj\', \'lsdkj\', \'sldkj\']

            # Use as_list() to create an actual list
            result_list = result.as_list()
            print(type(result_list), result_list) # -> <class \'list\'> [\'sldkj\', \'lsdkj\', \'sldkj\']
        '''
        return (lambda .0: for res in .0:
passcontinueres.as_list()[res])(self._toklist)

    
    def as_dict(self = None):
        '''
        Returns the named parse results as a nested dictionary.

        Example::

            integer = Word(nums)
            date_str = integer("year") + \'/\' + integer("month") + \'/\' + integer("day")

            result = date_str.parse_string(\'12/31/1999\')
            print(type(result), repr(result)) # -> <class \'pyparsing.ParseResults\'> ([\'12\', \'/\', \'31\', \'/\', \'1999\'], {\'day\': [(\'1999\', 4)], \'year\': [(\'12\', 0)], \'month\': [(\'31\', 2)]})

            result_dict = result.as_dict()
            print(type(result_dict), repr(result_dict)) # -> <class \'dict\'> {\'day\': \'1999\', \'year\': \'12\', \'month\': \'31\'}

            # even though a ParseResults supports dict-like access, sometime you just need to have a dict
            import json
            print(json.dumps(result)) # -> Exception: TypeError: ... is not JSON serializable
            print(json.dumps(result.as_dict())) # -> {"month": "31", "day": "1999", "year": "12"}
        '''
        
        def to_item(obj = None):
            if isinstance(obj, ParseResults):
                if obj.haskeys():
                    return obj.as_dict()
                return (lambda .0 = None: [ to_item(v) for v in .0 ])(obj)

        return None((lambda .0 = None: for k, v in .0:
(k, to_item(v)))(self.items()))

    
    def copy(self = None):
        '''
        Returns a new copy of a :class:`ParseResults` object.
        '''
        ret = ParseResults(self._toklist)
        ret._tokdict = self._tokdict.copy()
        ret._parent = self._parent
        ret._all_names |= self._all_names
        ret._name = self._name
        return ret

    
    def get_name(self):
        '''
        Returns the results name for this token expression. Useful when several
        different expressions might match at a particular location.

        Example::

            integer = Word(nums)
            ssn_expr = Regex(r"\\d\\d\\d-\\d\\d-\\d\\d\\d\\d")
            house_number_expr = Suppress(\'#\') + Word(nums, alphanums)
            user_data = (Group(house_number_expr)("house_number")
                        | Group(ssn_expr)("ssn")
                        | Group(integer)("age"))
            user_info = user_data[1, ...]

            result = user_info.parse_string("22 111-22-3333 #221B")
            for item in result:
                print(item.get_name(), \':\', item[0])

        prints::

            age : 22
            ssn : 111-22-3333
            house_number : 221B
        '''
        if self._name:
            return self._name
        if None._parent:
            par = self._parent()
            
            def find_in_parent(sub = None):
                return None((lambda .0 = None: for k, vlist in .0:
for v, loc in vlist:
if sub is v:
kcontinuecontinueNone)(par._tokdict.items()), None)

            if par:
                return find_in_parent(self)
            return None
        if None(self) == 1 and len(self._tokdict) == 1 and next(iter(self._tokdict.values()))[0][1] in (0, -1):
            return next(iter(self._tokdict.keys()))

    
    def dump(self = None, indent = None, full = None, include_list = ('', True, True, 0), _depth = ('return', str)):
        '''
        Diagnostic method for listing out the contents of
        a :class:`ParseResults`. Accepts an optional ``indent`` argument so
        that this string can be embedded in a nested display of other data.

        Example::

            integer = Word(nums)
            date_str = integer("year") + \'/\' + integer("month") + \'/\' + integer("day")

            result = date_str.parse_string(\'1999/12/31\')
            print(result.dump())

        prints::

            [\'1999\', \'/\', \'12\', \'/\', \'31\']
            - day: \'31\'
            - month: \'12\'
            - year: \'1999\'
        '''
        out = []
        NL = '\n'
        out.append(indent + str(self.as_list()) if include_list else '')
        if full:
            if self.haskeys():
                items = sorted((lambda .0: for k, v in .0:
(str(k), v))(self.items()))
                for k, v in items:
                    if out:
                        out.append(NL)
                    out.append('{}{}- {}: '.format(indent, '  ' * _depth, k))
                    if isinstance(v, ParseResults):
                        if v:
                            out.append(v.dump(indent, full, include_list, _depth + 1, **('indent', 'full', 'include_list', '_depth')))
                            continue
                        out.append(str(v))
                        continue
                    out.append(repr(v))
            if any((lambda .0: for vv in .0:
isinstance(vv, ParseResults))(self)):
                v = self
                for i, vv in enumerate(v):
                    if isinstance(vv, ParseResults):
                        out.append('\n{}{}[{}]:\n{}{}{}'.format(indent, '  ' * _depth, i, indent, '  ' * (_depth + 1), vv.dump(indent, full, include_list, _depth + 1, **('indent', 'full', 'include_list', '_depth'))))
                        continue
                    out.append('\n%s%s[%d]:\n%s%s%s' % (indent, '  ' * _depth, i, indent, '  ' * (_depth + 1), str(vv)))
        return ''.join(out)

    
    def pprint(self, *args, **kwargs):
        '''
        Pretty-printer for parsed results as a list, using the
        `pprint <https://docs.python.org/3/library/pprint.html>`_ module.
        Accepts additional positional or keyword args as defined for
        `pprint.pprint <https://docs.python.org/3/library/pprint.html#pprint.pprint>`_ .

        Example::

            ident = Word(alphas, alphanums)
            num = Word(nums)
            func = Forward()
            term = ident | num | Group(\'(\' + func + \')\')
            func <<= ident + Group(Optional(delimited_list(term)))
            result = func.parse_string("fna a,b,(fnb c,d,200),100")
            result.pprint(width=40)

        prints::

            [\'fna\',
             [\'a\',
              \'b\',
              [\'(\', \'fnb\', [\'c\', \'d\', \'200\'], \')\'],
              \'100\']]
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def __getstate__(self):
        if not self._parent is not None or self._parent():
            pass
        return (self._toklist, (self._tokdict.copy(), None, self._all_names, self._name))

    
    def __setstate__(self, state):
        (self._tokdict, par, inAccumNames, self._name) = (self._toklist,)
        self._all_names = set(inAccumNames)
        if par is not None:
            self._parent = wkref(par)
            return None
        self._parent = state

    
    def __getnewargs__(self):
        return (self._toklist, self._name)

    
    def __dir__(self):
        return dir(type(self)) + list(self.keys())

    
    def from_dict(cls = None, other = None, name = classmethod):
        '''
        Helper classmethod to construct a ``ParseResults`` from a ``dict``, preserving the
        name-value relations as results names. If an optional ``name`` argument is
        given, a nested ``ParseResults`` will be returned.
        '''
        
        def is_iterable(obj):
            pass
        # WARNING: Decompyle incomplete

        ret = cls([])
        for k, v in other.items():
            if isinstance(v, Mapping):
                ret += cls.from_dict(v, k, **('name',))
                continue
            ret += cls([
                v], k, is_iterable(v), **('name', 'asList'))
        if name is not None:
            ret = cls([
                ret], name, **('name',))
        return ret

    from_dict = None(from_dict)
    asList = as_list
    asDict = as_dict
    getName = get_name

MutableMapping.register(ParseResults)
MutableSequence.register(ParseResults)
