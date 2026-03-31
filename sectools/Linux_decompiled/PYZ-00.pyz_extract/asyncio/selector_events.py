
__doc__ = 'Event loop using a selector and related classes.\n\nA selector is a "notify-when-ready" multiplexer.  For a subclass which\nalso includes support for signal handling, see the unix_events sub-module.\n'
__all__ = ('BaseSelectorEventLoop',)
import collections
import errno
import functools
import selectors
import socket
import warnings
import weakref
# WARNING: Decompyle incomplete
