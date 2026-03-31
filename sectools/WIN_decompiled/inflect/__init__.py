
__doc__ = '\ncorrectly generate plurals, ordinals, indefinite articles;\nconvert numbers to words\n\nCopyright (C) 2010 Paul Dyson\n\nBased upon the Perl module Lingua::EN::Inflect by Damian Conway.\n\nThe original Perl module Lingua::EN::Inflect by Damian Conway is\navailable from http://search.cpan.org/~dconway/\n\nThis module can be downloaded at http://pypi.org/project/inflect\n\nmethods:\n      classical inflect\n      plural plural_noun plural_verb plural_adj singular_noun no num a an\n      compare compare_nouns compare_verbs compare_adjs\n      present_participle\n      ordinal\n      number_to_words\n      join\n      defnoun defverb defadj defa defan\n\nINFLECTIONS:    classical inflect\n      plural plural_noun plural_verb plural_adj singular_noun compare\n      no num a an present_participle\n\nPLURALS:   classical inflect\n      plural plural_noun plural_verb plural_adj singular_noun no num\n      compare compare_nouns compare_verbs compare_adjs\n\nCOMPARISONS:    classical\n      compare compare_nouns compare_verbs compare_adjs\n\nARTICLES:   classical inflect num a an\n\nNUMERICAL:      ordinal number_to_words\n\nUSER_DEFINED:   defnoun defverb defadj defa defan\n\nExceptions:\n UnknownClassicalModeError\n BadNumValueError\n BadChunkingOptionError\n NumOutOfRangeError\n BadUserDefinedPatternError\n BadRcFileError\n BadGenderError\n\n'
import ast
import re
from typing import Dict, Union, Optional, Iterable, List, Match, Tuple, Callable, Sequence

class UnknownClassicalModeError(Exception):
    pass


class BadNumValueError(Exception):
    pass


class BadChunkingOptionError(Exception):
    pass


class NumOutOfRangeError(Exception):
    pass


class BadUserDefinedPatternError(Exception):
    pass


class BadRcFileError(Exception):
    pass


class BadGenderError(Exception):
    pass

STDOUT_ON = False

def print3(txt = None):
    if STDOUT_ON:
        print(txt)
        return None


def enclose(s = None):
    return f'''(?:{s})'''


def joinstem(cutpoint = None, words = None):
    '''
    join stem of each word in words into a string for regex
    each word is truncated at cutpoint
    cutpoint is usually negative indicating the number of letters to remove
    from the end of each word

    e.g.
    joinstem(-2, ["ephemeris", "iris", ".*itis"]) returns
    (?:ephemer|ir|.*it)

    '''
    if words is None:
        words = ''
    return None(None((lambda .0 = None: for w in .0:
w[:cutpoint])(words)))


def bysize(words = None):
    """
    take a list of words and return a dict of sets sorted by word length
    e.g.
    ret[3]=set(['ant', 'cat', 'dog', 'pig'])
    ret[4]=set(['frog', 'goat'])
    ret[5]=set(['horse'])
    ret[8]=set(['elephant'])
    """
    ret = { }
    for w in words:
        if len(w) not in ret:
            ret[len(w)] = set()
        ret[len(w)].add(w)
    return ret


def make_pl_si_lists(lst = None, plending = None, siendingsize = None, dojoinstem = (True,)):
    '''
    given a list of singular words: lst

    an ending to append to make the plural: plending

    the number of characters to remove from the singular
    before appending plending: siendingsize

    a flag whether to create a joinstem: dojoinstem

    return:
    a list of pluralised words: si_list (called si because this is what you need to
    look for to make the singular)

    the pluralised words as a dict of sets sorted by word length: si_bysize
    the singular words as a dict of sets sorted by word length: pl_bysize
    if dojoinstem is True: a regular expression that matches any of the stems: stem
    '''
    if siendingsize is not None:
        siendingsize = -siendingsize
    si_list = (lambda .0 = None: [ w[:siendingsize] + plending for w in .0 ])(lst)
    pl_bysize = bysize(lst)
    si_bysize = bysize(si_list)
    if dojoinstem:
        stem = joinstem(siendingsize, lst)
        return (si_list, si_bysize, pl_bysize, stem)
    return (None, si_bysize, pl_bysize)

pl_sb_irregular_s = {
    'corpus': 'corpuses|corpora',
    'opus': 'opuses|opera',
    'genus': 'genera',
    'mythos': 'mythoi',
    'penis': 'penises|penes',
    'testis': 'testes',
    'atlas': 'atlases|atlantes',
    'yes': 'yeses' }
# WARNING: Decompyle incomplete
