
from __future__ import annotations
from contextlib import suppress
from copy import deepcopy
from functools import cache, reduce
from json import dumps, loads
from operator import getitem, itemgetter
from typing import Any, Iterator, cast
from common.data.data import comma_separated_string
from common.parser.tme.tme_parser.defines import SharedState, Tag, TagList
from common.parser.tme.tme_parser.exceptions import ProtocolError, ProtocolVersionError
from common.parser.tme.tme_parser.grammar import TMEGrammarException, TME_GRAMMAR_VERSIONS
from common.parser.tme.tme_parser.tag_parsers import ConstrainedMapObject, MapObject
from common.parser.tme.tme_parser.version_autodetect import parser_autodetect

class TME:
    '''The TME format parser.
    Used for TME Debug Policy and Debug Entitlement.

    TME is similar to JSON/CBOR formats, however, simplified and with more specialized tags
    (rather than generic string key-value pairs).
    The TME uses specialized parsers to process individual tags. These are derived from the
    base_parser that are not to be changed in the future versions (otherwise, that is a new grammar/format).

    USAGE NOTE: When interested in a particular field(s) from the parsed TME object use items interface -
    i.e., tme["Entitlement"]["InterestingPart"]["etc."]. That will trigger a KeyError if the item you\'re querying is
    missing.
    On the other hand, when creating a new TME object, that may be convenient to use attribute interface instead.
    That will allow default creation of non-existent TME sub-items and their assignment.
    For example, tme.Entitlement.MissingPart.NewItem = "SHA256".
    '''
    _attribute_lock = False
    
    def __init__(self, data = None, tme_grammar_versions = None, version = None, tme_tag_id = (None, None, None, None, False), populate_required_only = ('data', 'memoryview | int | bytes | bytearray | dict | str | TME | None', 'tme_grammar_versions', 'dict[int, TagList] | None', 'version', 'int | None', 'tme_tag_id', 'int | None', 'populate_required_only', 'bool', 'return', 'None')):
        '''The TME object accepts both binary data and JSON text as a constructor input. It makes an assumption of
        the input based on argument type - byte array or string.

        Note: The parser object keeps provided data as python object. Use .pack() to reconstruct to binary.
        Otherwise, use str(TME object) for printable JSON.
        Use .normalize() to verify the TME object without packing/ unpacking.
        '''
        self.structure = { }
        if not tme_grammar_versions:
            pass
        self._tme_grammar_versions = TME_GRAMMAR_VERSIONS
        self.version = version
    # WARNING: Decompyle incomplete

    
    def unpack(self = None, data = None):
        '''Unpacks the data (get JSON representation).'''
        self._unpack(data)

    
    def _unpack(self = None, data = None, ignore_tme_structure = None, resolve_enums = (False, True)):
        '''Extended version that allows additional flags. Unpacks the data (get JSON representation).'''
        
        def _unpack(state = None):
            ret = MapObject(data, state, True, **('data', 'state', 'is_root_object')).get_json()
            return (ret, cast(int, state.last_tried_tme_version))

        _unpack = None(_unpack)
        (structure, version) = _unpack(SharedState(ignore_tme_structure, resolve_enums, **('ignore_tme_structure', 'resolve_enums')), **('state',))
        self._attribute_lock = False
        self.structure = structure
        self.version = version
        self._attribute_lock = True
        return self

    
    def normalize(self = None, resolve_enums = None):
        '''
        Reformat the TME representation.
        Runs internal parsers normalization that will check for TME errors. Calls for JSON normalization,
        therefore useful for "expanding" tags (i.e., converts int values to enums, etc.).
        '''
        self._unpack(self.structure, resolve_enums, **('resolve_enums',))
        return self

    
    def pack(self = None):
        '''
        Extended version that allows additional flags.
        Packs the data (get byte array representation).
        Always does version autodetection unless it (the version grammar) restricted by the
        constructor - version argument.
        '''
        return self._pack(self._tme_grammar_versions, SharedState())

    
    def _force_pack(self = None, version = None):
        """Don't use this function! Pack TME object even if that violates TME spec."""
        return self._pack({
            version: self._tme_grammar_versions[version] }, SharedState(True, **('ignore_tme_structure',)))

    
    def _pack(self = None, tme_grammar_versions = None, state = None):
        '''
        Extended version that allows additional flags and control. Low level function, use pack() instead.
        Packs the data (get byte array representation).
        Always does version autodetection unless it (the version grammar) restricted by the
        constructor - version argument.
        '''
        
        def _pack(state = None):
            ret = MapObject(self.structure, state, True, **('data', 'state', 'is_root_object')).get_byte_array()
            self._attribute_lock = False
            self.version = state.last_tried_tme_version
            self._attribute_lock = True
            return ret

        _pack = None(_pack)
        return _pack(state, **('state',))

    
    def is_type(cls = None, data = None):
        pass
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def __repr__(self = None):
        return dumps(self.structure, 4, **('indent',))

    
    def __getitem__(self, key):
        return self.structure[key]

    
    def set_item(self = None, json_pointer = None, value = None):
        '''Convenience function. Assigns an item using JSON pointer string.'''
        pointers = json_pointer.lstrip('/').split('/')
        tmp = reduce(getattr, pointers[:-1], self)
        setattr(tmp, pointers[-1], value)

    
    def get_item(self = None, json_pointer = None):
        '''
        Convenience function. Returns an item using JSON pointer string. JSON pointer string cannot follow paths inside
        of list items.
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def is_item(self = None, json_pointer = None):
        '''Convenience function. Returns true if JSON pointer string points to an existing item.'''
        member_list = json_pointer.lstrip('/').split('/')
    # WARNING: Decompyle incomplete

    
    def find(self = None, tag_name = None):
        """
        Recursively finds JSON path and value by the tag name.
        The None value for the tag_name is a special case allowing listing all the TME object's JSON paths (all leaves).
        """
        
        def finder(obj = None, what = None, path = None):
            for k, v in obj.items():
                if not (k == what or what is None) and isinstance(v, dict):
                    yield (path + f'''/{k}''', v)
                if isinstance(v, dict):
                    yield from finder(v, what, path + f'''/{k}''')
                    continue
                if isinstance(v, list):
                    for element in v:
                        if isinstance(element, dict):
                            yield from finder(element, what, path + f'''/{k}''')

        return finder(self.structure, tag_name)

    
    def get_items_under_path(self = None, path = None):
        path = path.strip('/')
        for current_path, value in self.find(None):
            current_path = current_path.strip('/')
            if current_path.startswith(path):
                current_path = current_path[len(path):]
                if isinstance(value, list):
                    for item in value:
                        yield (current_path, item)
                    continue
                yield (current_path, value)

    
    def __getattr__(self = None, name = None):
        '''
        Enable attribute access for TME structure.
        Fully re-route unknown TME attribute accesses to TME structure.

        Allow default dict like access to attributes.
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def __setattr__(self = None, name = None, value = None):
        '''Fully re-route TME attribute accesses to TME structure.'''
        if self._attribute_lock and '_attribute_lock' != name:
            self.structure[name] = value
            return None
        None().__setattr__(name, value)

    
    def from_tag_id(cls = None, tme_tag_id = None, tme_grammar_versions = classmethod, populate_required_only = (False,)):
        """
        The alternative constructor that generates the structure for a tag id.
        Creates all required fields and fills them with default values.

        If the class doesn't have a specific grammar version selected, it uses the latest (max).
        """
        custom_map_object_type = type('custom_map_object', (ConstrainedMapObject,), {
            'REQUIRED_TAGS': {
                tme_tag_id: 'root' },
            'ALLOWED_TAGS': {
                tme_tag_id: 'root' } })
        version = max(tme_grammar_versions.keys())
        state = SharedState(tme_grammar_versions[version], populate_required_only, **('tag_list', 'populate_required_only'))
        custom_map_object = custom_map_object_type(None, state, **('state',))
        return cls(custom_map_object.get_json(), tme_grammar_versions, version, **('data', 'tme_grammar_versions', 'version'))

    from_tag_id = None(from_tag_id)
    
    def get_root_tag(self = None):
        for tag_list in TME_GRAMMAR_VERSIONS.values():
            for tag in tag_list:
                if tag.tag_name in self.structure:
                    return tag
                raise RuntimeError('No root tag found that matches TME grammar.')

    
    def is_cmd_svc(self = None):
        root_tag = self.get_root_tag()
        if root_tag.tag_type == 'map' and root_tag.tag_group == 'CMD-SVC':
            pass
        return root_tag.tag_name.startswith('Svc')

    __classcell__ = None


def get_selections_for_tag_extended(tag_name = None):
    '''
    Looks up the given tag in ALL TME versions and combines accepted arguments.
    Returns in extended - (name, value) format.
    '''
    ret = []
    for v, tags in TME_GRAMMAR_VERSIONS.items():
        if 0 == v:
            continue
        tag = None(None((lambda x = None: x.tag_name == tag_name), tags))
        if 'ENUMS' in dir(tag.parser_class):
            ret.extend((lambda .0: [ (i.value, i.name) for i in .0 ])(tag.parser_class(None).ENUMS))
    if not ret:
        raise ProtocolError(f'''{tag_name} is not a selection or enumeration tag.''')
    return None(ret)


def get_selections_for_tag(tag_name = None):
    '''Looks up the given tag in ALL TME versions and combines accepted arguments. Simplified version.'''
    return set(map(itemgetter(1), get_selections_for_tag_extended(tag_name)))


def get_reference_tme_obj(reference_root = None):
    return TME.from_tag_id(reference_root, TME_GRAMMAR_VERSIONS)

get_reference_tme_obj = None(get_reference_tme_obj)

def validate_tag_grammar(tag_path = None):
    if not get_reference_tme_obj(390).is_item(tag_path.strip('/')):
        raise TMEGrammarException(f'''{tag_path} either violates the TME grammar or is not a valid DPR tag. Check the spelling.''')

