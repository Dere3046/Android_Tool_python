
'''Doctest module for XML comparison.

Usage::

   >>> import lxml.usedoctest
   >>> # now do your XML doctests ...

See `lxml.doctestcompare`
'''
from lxml import doctestcompare
doctestcompare.temp_install(__name__, **('del_module',))
