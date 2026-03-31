
__doc__ = '\npyparsing module - Classes and methods to define and execute parsing grammars\n=============================================================================\n\nThe pyparsing module is an alternative approach to creating and executing simple grammars,\nvs. the traditional lex/yacc approach, or the use of regular expressions.  With pyparsing, you\ndon\'t need to learn a new syntax for defining grammars or matching expressions - the parsing module\nprovides a library of classes that you use to construct the grammar directly in Python.\n\nHere is a program to parse "Hello, World!" (or any greeting of the form \nC{"<salutation>, <addressee>!"}), built up using L{Word}, L{Literal}, and L{And} elements \n(L{\'+\'<ParserElement.__add__>} operator gives L{And} expressions, strings are auto-converted to\nL{Literal} expressions)::\n\n    from pyparsing import Word, alphas\n\n    # define grammar of a greeting\n    greet = Word(alphas) + "," + Word(alphas) + "!"\n\n    hello = "Hello, World!"\n    print (hello, "->", greet.parseString(hello))\n\nThe program outputs the following::\n\n    Hello, World! -> [\'Hello\', \',\', \'World\', \'!\']\n\nThe Python representation of the grammar is quite readable, owing to the self-explanatory\nclass names, and the use of \'+\', \'|\' and \'^\' operators.\n\nThe L{ParseResults} object returned from L{ParserElement.parseString<ParserElement.parseString>} can be accessed as a nested list, a dictionary, or an\nobject with named attributes.\n\nThe pyparsing module handles some of the problems that are typically vexing when writing text parsers:\n - extra or missing whitespace (the above program will also handle "Hello,World!", "Hello  ,  World  !", etc.)\n - quoted strings\n - embedded comments\n\n\nGetting Started -\n-----------------\nVisit the classes L{ParserElement} and L{ParseResults} to see the base classes that most other pyparsing\nclasses inherit from. Use the docstrings for examples of how to:\n - construct literal match expressions from L{Literal} and L{CaselessLiteral} classes\n - construct character word-group expressions using the L{Word} class\n - see how to create repetitive expressions using L{ZeroOrMore} and L{OneOrMore} classes\n - use L{\'+\'<And>}, L{\'|\'<MatchFirst>}, L{\'^\'<Or>}, and L{\'&\'<Each>} operators to combine simple expressions into more complex ones\n - associate names with your parsed results using L{ParserElement.setResultsName}\n - find some helpful expression short-cuts like L{delimitedList} and L{oneOf}\n - find more useful common expressions in the L{pyparsing_common} namespace class\n'
__version__ = '2.2.1'
__versionTime__ = '18 Sep 2018 00:49 UTC'
__author__ = 'Paul McGuire <ptmcg@users.sourceforge.net>'
import string
from weakref import ref as wkref
import copy
import sys
import warnings
import re
import sre_constants
import collections
import pprint
import traceback
import types
from datetime import datetime
# WARNING: Decompyle incomplete
