
'''Doctest module for HTML comparison.

Usage::

   >>> import lxml.html.usedoctest
   >>> # now do your HTML doctests ...

See `lxml.doctestcompare`.
'''
from lxml import doctestcompare
doctestcompare.temp_install(True, __name__, **('html', 'del_module'))
