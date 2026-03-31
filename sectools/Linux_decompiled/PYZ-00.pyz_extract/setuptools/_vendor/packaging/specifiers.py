
import abc
import functools
import itertools
import re
import warnings
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Pattern, Set, Tuple, TypeVar, Union
from utils import canonicalize_version
from version import LegacyVersion, Version, parse
ParsedVersion = Union[(Version, LegacyVersion)]
UnparsedVersion = Union[(Version, LegacyVersion, str)]
VersionTypeVar = TypeVar('VersionTypeVar', UnparsedVersion, **('bound',))
CallableOperator = Callable[([
    ParsedVersion,
    str], bool)]

class InvalidSpecifier(ValueError):
    '''
    An invalid specifier was found, users should refer to PEP 440.
    '''
    pass

BaseSpecifier = <NODE:27>((lambda : 
def __str__(self = None):
'''
        Returns the str representation of this Specifier like object. This
        should be representative of the Specifier itself.
        '''
pass__str__ = None(__str__)
def __hash__(self = None):
'''
        Returns a hash value for this Specifier like object.
        '''
pass__hash__ = None(__hash__)
def __eq__(self = None, other = None):
'''
        Returns a boolean representing whether or not the two Specifier like
        objects are equal.
        '''
pass__eq__ = None(__eq__)
def __ne__(self = None, other = None):
'''
        Returns a boolean representing whether or not the two Specifier like
        objects are not equal.
        '''
pass__ne__ = None(__ne__)
def prereleases(self = None):
'''
        Returns whether or not pre-releases as a whole are allowed by this
        specifier.
        '''
passprereleases = None(prereleases)
def prereleases(self = None, value = None):
'''
        Sets whether or not pre-releases as a whole are allowed by this
        specifier.
        '''
passprereleases = None(prereleases)
def contains(self = None, item = None, prereleases = abc.abstractmethod):
'''
        Determines if the given item is contained within this specifier.
        '''
passcontains = None(contains)
def filter(self = None, iterable = None, prereleases = abc.abstractmethod):
'''
        Takes an iterable of items and filters them so that only items which
        are contained within this specifier are allowed in it.
        '''
passfilter = None(filter)), 'BaseSpecifier', abc.ABCMeta, **('metaclass',))

class _IndividualSpecifier(BaseSpecifier):
    _regex: Pattern[str] = { }
    
    def __init__(self = None, spec = None, prereleases = None):
        match = self._regex.search(spec)
        if not match:
            raise InvalidSpecifier(f'''Invalid specifier: \'{spec}\'''')
        self._spec = (None.group('operator').strip(), match.group('version').strip())
        self._prereleases = prereleases

    
    def __repr__(self = None):
        pre = f''', prereleases={self.prereleases!r}''' if self._prereleases is not None else ''
        return '<{}({!r}{})>'.format(self.__class__.__name__, str(self), pre)

    
    def __str__(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def _canonical_spec(self = None):
        return (self._spec[0], canonicalize_version(self._spec[1]))

    _canonical_spec = None(_canonical_spec)
    
    def __hash__(self = None):
        return hash(self._canonical_spec)

    
    def __eq__(self = None, other = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __ne__(self = None, other = None):
        pass
    # WARNING: Decompyle incomplete

    
    def _get_operator(self = None, op = None):
        operator_callable = getattr(self, f'''_compare_{self._operators[op]}''')
        return operator_callable

    
    def _coerce_version(self = None, version = None):
        if not isinstance(version, (LegacyVersion, Version)):
            version = parse(version)
        return version

    
    def operator(self = None):
        return self._spec[0]

    operator = None(operator)
    
    def version(self = None):
        return self._spec[1]

    version = None(version)
    
    def prereleases(self = None):
        return self._prereleases

    prereleases = None(prereleases)
    
    def prereleases(self = None, value = None):
        self._prereleases = value

    prereleases = None(prereleases)
    
    def __contains__(self = None, item = None):
        return self.contains(item)

    
    def contains(self = None, item = None, prereleases = None):
        if prereleases is None:
            prereleases = self.prereleases
        normalized_item = self._coerce_version(item)
        if not normalized_item.is_prerelease and prereleases:
            return False
        operator_callable = None._get_operator(self.operator)
        return operator_callable(normalized_item, self.version)

    
    def filter(self = None, iterable = None, prereleases = None):
        yielded = False
        found_prereleases = []
        kw = {
            'prereleases': prereleases if prereleases is not None else True }
    # WARNING: Decompyle incomplete



class LegacySpecifier(_IndividualSpecifier):
    _regex_str = '\n        (?P<operator>(==|!=|<=|>=|<|>))\n        \\s*\n        (?P<version>\n            [^,;\\s)]* # Since this is a "legacy" specifier, and the version\n                      # string can be just about anything, we match everything\n                      # except for whitespace, a semi-colon for marker support,\n                      # a closing paren since versions can be enclosed in\n                      # them, and a comma since it\'s a version separator.\n        )\n        '
    _regex = re.compile('^\\s*' + _regex_str + '\\s*$', re.VERBOSE | re.IGNORECASE)
    _operators = {
        '==': 'equal',
        '!=': 'not_equal',
        '<=': 'less_than_equal',
        '>=': 'greater_than_equal',
        '<': 'less_than',
        '>': 'greater_than' }
    
    def __init__(self = None, spec = None, prereleases = None):
        super().__init__(spec, prereleases)
        warnings.warn('Creating a LegacyVersion has been deprecated and will be removed in the next major release', DeprecationWarning)

    
    def _coerce_version(self = None, version = None):
        if not isinstance(version, LegacyVersion):
            version = LegacyVersion(str(version))
        return version

    
    def _compare_equal(self = None, prospective = None, spec = None):
        return prospective == self._coerce_version(spec)

    
    def _compare_not_equal(self = None, prospective = None, spec = None):
        return prospective != self._coerce_version(spec)

    
    def _compare_less_than_equal(self = None, prospective = None, spec = None):
        return prospective <= self._coerce_version(spec)

    
    def _compare_greater_than_equal(self = None, prospective = None, spec = None):
        return prospective >= self._coerce_version(spec)

    
    def _compare_less_than(self = None, prospective = None, spec = None):
        return prospective < self._coerce_version(spec)

    
    def _compare_greater_than(self = None, prospective = None, spec = None):
        return prospective > self._coerce_version(spec)

    __classcell__ = None


def _require_version_compare(fn = None):
    
    def wrapped(self = None, prospective = None, spec = None):
        if not isinstance(prospective, Version):
            return False
        return None(self, prospective, spec)

    wrapped = None(wrapped)
    return wrapped


class Specifier(_IndividualSpecifier):
    _regex_str = "\n        (?P<operator>(~=|==|!=|<=|>=|<|>|===))\n        (?P<version>\n            (?:\n                # The identity operators allow for an escape hatch that will\n                # do an exact string match of the version you wish to install.\n                # This will not be parsed by PEP 440 and we cannot determine\n                # any semantic meaning from it. This operator is discouraged\n                # but included entirely as an escape hatch.\n                (?<====)  # Only match for the identity operator\n                \\s*\n                [^\\s]*    # We just match everything, except for whitespace\n                          # since we are only testing for strict identity.\n            )\n            |\n            (?:\n                # The (non)equality operators allow for wild card and local\n                # versions to be specified so we have to define these two\n                # operators separately to enable that.\n                (?<===|!=)            # Only match for equals and not equals\n\n                \\s*\n                v?\n                (?:[0-9]+!)?          # epoch\n                [0-9]+(?:\\.[0-9]+)*   # release\n                (?:                   # pre release\n                    [-_\\.]?\n                    (a|b|c|rc|alpha|beta|pre|preview)\n                    [-_\\.]?\n                    [0-9]*\n                )?\n                (?:                   # post release\n                    (?:-[0-9]+)|(?:[-_\\.]?(post|rev|r)[-_\\.]?[0-9]*)\n                )?\n\n                # You cannot use a wild card and a dev or local version\n                # together so group them with a | and make them optional.\n                (?:\n                    (?:[-_\\.]?dev[-_\\.]?[0-9]*)?         # dev release\n                    (?:\\+[a-z0-9]+(?:[-_\\.][a-z0-9]+)*)? # local\n                    |\n                    \\.\\*  # Wild card syntax of .*\n                )?\n            )\n            |\n            (?:\n                # The compatible operator requires at least two digits in the\n                # release segment.\n                (?<=~=)               # Only match for the compatible operator\n\n                \\s*\n                v?\n                (?:[0-9]+!)?          # epoch\n                [0-9]+(?:\\.[0-9]+)+   # release  (We have a + instead of a *)\n                (?:                   # pre release\n                    [-_\\.]?\n                    (a|b|c|rc|alpha|beta|pre|preview)\n                    [-_\\.]?\n                    [0-9]*\n                )?\n                (?:                                   # post release\n                    (?:-[0-9]+)|(?:[-_\\.]?(post|rev|r)[-_\\.]?[0-9]*)\n                )?\n                (?:[-_\\.]?dev[-_\\.]?[0-9]*)?          # dev release\n            )\n            |\n            (?:\n                # All other operators only allow a sub set of what the\n                # (non)equality operators do. Specifically they do not allow\n                # local versions to be specified nor do they allow the prefix\n                # matching wild cards.\n                (?<!==|!=|~=)         # We have special cases for these\n                                      # operators so we want to make sure they\n                                      # don't match here.\n\n                \\s*\n                v?\n                (?:[0-9]+!)?          # epoch\n                [0-9]+(?:\\.[0-9]+)*   # release\n                (?:                   # pre release\n                    [-_\\.]?\n                    (a|b|c|rc|alpha|beta|pre|preview)\n                    [-_\\.]?\n                    [0-9]*\n                )?\n                (?:                                   # post release\n                    (?:-[0-9]+)|(?:[-_\\.]?(post|rev|r)[-_\\.]?[0-9]*)\n                )?\n                (?:[-_\\.]?dev[-_\\.]?[0-9]*)?          # dev release\n            )\n        )\n        "
    _regex = re.compile('^\\s*' + _regex_str + '\\s*$', re.VERBOSE | re.IGNORECASE)
    _operators = {
        '~=': 'compatible',
        '==': 'equal',
        '!=': 'not_equal',
        '<=': 'less_than_equal',
        '>=': 'greater_than_equal',
        '<': 'less_than',
        '>': 'greater_than',
        '===': 'arbitrary' }
    
    def _compare_compatible(self = None, prospective = None, spec = _require_version_compare):
        prefix = '.'.join(list(itertools.takewhile(_is_not_suffix, _version_split(spec)))[:-1])
        prefix += '.*'
        if self._get_operator('>=')(prospective, spec):
            pass
        return self._get_operator('==')(prospective, prefix)

    _compare_compatible = None(_compare_compatible)
    
    def _compare_equal(self = None, prospective = None, spec = _require_version_compare):
        if spec.endswith('.*'):
            prospective = Version(prospective.public)
            split_spec = _version_split(spec[:-2])
            split_prospective = _version_split(str(prospective))
            shortened_prospective = split_prospective[:len(split_spec)]
            (padded_spec, padded_prospective) = _pad_version(split_spec, shortened_prospective)
            return padded_prospective == padded_spec
        spec_version = None(spec)
        if not spec_version.local:
            prospective = Version(prospective.public)
        return prospective == spec_version

    _compare_equal = None(_compare_equal)
    
    def _compare_not_equal(self = None, prospective = None, spec = _require_version_compare):
        return not self._compare_equal(prospective, spec)

    _compare_not_equal = None(_compare_not_equal)
    
    def _compare_less_than_equal(self = None, prospective = None, spec = _require_version_compare):
        return Version(prospective.public) <= Version(spec)

    _compare_less_than_equal = None(_compare_less_than_equal)
    
    def _compare_greater_than_equal(self = None, prospective = None, spec = _require_version_compare):
        return Version(prospective.public) >= Version(spec)

    _compare_greater_than_equal = None(_compare_greater_than_equal)
    
    def _compare_less_than(self = None, prospective = None, spec_str = _require_version_compare):
        spec = Version(spec_str)
        if not prospective < spec:
            return False
        if None.is_prerelease and prospective.is_prerelease and Version(prospective.base_version) == Version(spec.base_version):
            return False

    _compare_less_than = None(_compare_less_than)
    
    def _compare_greater_than(self = None, prospective = None, spec_str = _require_version_compare):
        spec = Version(spec_str)
        if not prospective > spec:
            return False
        if None.is_postrelease and prospective.is_postrelease and Version(prospective.base_version) == Version(spec.base_version):
            return False
        if None.local is not None and Version(prospective.base_version) == Version(spec.base_version):
            return False

    _compare_greater_than = None(_compare_greater_than)
    
    def _compare_arbitrary(self = None, prospective = None, spec = None):
        return str(prospective).lower() == str(spec).lower()

    
    def prereleases(self = None):
        if self._prereleases is not None:
            return self._prereleases
        (operator, version) = None._spec
        if operator in ('==', '>=', '<=', '~=', '==='):
            if operator == '==' and version.endswith('.*'):
                version = version[:-2]
            if parse(version).is_prerelease:
                return True
            return None

    prereleases = None(prereleases)
    
    def prereleases(self = None, value = None):
        self._prereleases = value

    prereleases = None(prereleases)

_prefix_regex = re.compile('^([0-9]+)((?:a|b|c|rc)[0-9]+)$')

def _version_split(version = None):
    result = []
    for item in version.split('.'):
        match = _prefix_regex.search(item)
        if match:
            result.extend(match.groups())
            continue
        result.append(item)
    return result


def _is_not_suffix(segment = None):
    return not None((lambda .0 = None: for prefix in .0:
segment.startswith(prefix))(('dev', 'a', 'b', 'rc', 'post')))


def _pad_version(left = None, right = None):
    left_split = []
    right_split = []
    left_split.append(list(itertools.takewhile((lambda x: x.isdigit()), left)))
    right_split.append(list(itertools.takewhile((lambda x: x.isdigit()), right)))
    left_split.append(left[len(left_split[0]):])
    right_split.append(right[len(right_split[0]):])
    left_split.insert(1, [
        '0'] * max(0, len(right_split[0]) - len(left_split[0])))
    right_split.insert(1, [
        '0'] * max(0, len(left_split[0]) - len(right_split[0])))
# WARNING: Decompyle incomplete


class SpecifierSet(BaseSpecifier):
    
    def __init__(self = None, specifiers = None, prereleases = None):
        split_specifiers = (lambda .0: [ s.strip() for s in .0 if s.strip() ])(specifiers.split(','))
        parsed = set()
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        pre = f''', prereleases={self.prereleases!r}''' if self._prereleases is not None else ''
        return '<SpecifierSet({!r}{})>'.format(str(self), pre)

    
    def __str__(self = None):
        return ','.join(sorted((lambda .0: for s in .0:
str(s))(self._specs)))

    
    def __hash__(self = None):
        return hash(self._specs)

    
    def __and__(self = None, other = None):
        if isinstance(other, str):
            other = SpecifierSet(other)
        elif not isinstance(other, SpecifierSet):
            return NotImplemented
        specifier = SpecifierSet()
        specifier._specs = frozenset(self._specs | other._specs)
        if self._prereleases is None and other._prereleases is not None:
            specifier._prereleases = other._prereleases
            return specifier
        if None._prereleases is not None and other._prereleases is None:
            specifier._prereleases = self._prereleases
            return specifier
        if None._prereleases == other._prereleases:
            specifier._prereleases = self._prereleases
            return specifier
        raise None('Cannot combine SpecifierSets with True and False prerelease overrides.')

    
    def __eq__(self = None, other = None):
        if isinstance(other, (str, _IndividualSpecifier)):
            other = SpecifierSet(str(other))
        elif not isinstance(other, SpecifierSet):
            return NotImplemented
        return self._specs == other._specs

    
    def __ne__(self = None, other = None):
        if isinstance(other, (str, _IndividualSpecifier)):
            other = SpecifierSet(str(other))
        elif not isinstance(other, SpecifierSet):
            return NotImplemented
        return self._specs != other._specs

    
    def __len__(self = None):
        return len(self._specs)

    
    def __iter__(self = None):
        return iter(self._specs)

    
    def prereleases(self = None):
        if self._prereleases is not None:
            return self._prereleases
        if not None._specs:
            return None
        return None((lambda .0: for s in .0:
s.prereleases)(self._specs))

    prereleases = None(prereleases)
    
    def prereleases(self = None, value = None):
        self._prereleases = value

    prereleases = None(prereleases)
    
    def __contains__(self = None, item = None):
        return self.contains(item)

    
    def contains(self = None, item = None, prereleases = None):
        if not isinstance(item, (LegacyVersion, Version)):
            item = parse(item)
        if prereleases is None:
            prereleases = self.prereleases
        if prereleases and item.is_prerelease:
            return False
        return None((lambda .0 = None: for s in .0:
s.contains(item, prereleases, **('prereleases',)))(self._specs))

    
    def filter(self = None, iterable = None, prereleases = None):
        if prereleases is None:
            prereleases = self.prereleases
        if self._specs:
            for spec in self._specs:
                iterable = spec.filter(iterable, bool(prereleases), **('prereleases',))
            return iterable
        filtered = None
        found_prereleases = []
        for item in iterable:
            if not isinstance(item, (LegacyVersion, Version)):
                parsed_version = parse(item)
            else:
                parsed_version = item
            if isinstance(parsed_version, LegacyVersion):
                continue
            if not parsed_version.is_prerelease and prereleases:
                if not filtered:
                    found_prereleases.append(item)
                continue
            filtered.append(item)
        if filtered and found_prereleases and prereleases is None:
            return found_prereleases


