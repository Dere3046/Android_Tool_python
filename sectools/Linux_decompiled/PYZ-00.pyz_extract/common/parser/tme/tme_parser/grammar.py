
'''
Processes the unified TME tag repo (tme_tag_values) and generates the tag list.
'''
import json
from enum import Enum
from itertools import chain
from pathlib import Path
from typing import Any, Type
from common.parser.tme.tme_parser.defines import Tag, TagList
from common.parser.tme.tme_parser.tag_parsers import ByteArray, ConstrainedMapObject, DataOnly, Enumeration, GenericParser, Int16HexDataOnly, Int32Array, Int32Enumeration, Int32Hex, Int32Selection, Int32Version, Int64Hex, MapObject, RepeatableObject, Selection

def generate_tme_grammar(version = None, tme_tags = None, tme_relations = None, tme_enums = ('version', int, 'tme_tags', Any, 'tme_relations', Any, 'tme_enums', Any, 'return', TagList)):
    '''Parses a single version of the TME grammar.'''
    tag_list = TagList()
# WARNING: Decompyle incomplete


def generate_tme_grammar_versions(tme_tag_values_paths = None):
    '''Generates complete tags grammar - {version: tag_list}.'''
    files = [
        'tme_tags.json',
        'tme_enums.json',
        'tme_relations.json']
    tag_dict = { }
# WARNING: Decompyle incomplete

TME_GRAMMAR_PATH = Path(__file__).parent / 'tme_tag_values'
TME_GRAMMAR_VERSIONS: dict[(int, TagList)] = generate_tme_grammar_versions([
    TME_GRAMMAR_PATH])

class TMEGrammarException(Exception):
    '''Raised when TME grammar is violated, according to the relationships defined in tme_relations.json.'''
    pass

