
__doc__ = 'Base implementation of event loop.\n\nThe event loop can be broken up into a multiplexer (the part\nresponsible for notifying us of I/O events) and the event loop proper,\nwhich wraps a multiplexer with functionality for scheduling callbacks,\nimmediately or at a given time in the future.\n\nWhenever a public API takes a callback, subsequent positional\narguments will be passed to the callback if/when it is called.  This\navoids the proliferation of trivial lambdas implementing closures.\nKeyword arguments for the callback are not supported; this is a\nconscious design decision, leaving the door open for keyword arguments\nto modify the meaning of the API call itself.\n'
import collections
import collections.abc as collections
import concurrent.futures as concurrent
import functools
import heapq
import itertools
import os
import socket
import stat
import subprocess
import threading
import time
import traceback
import sys
import warnings
import weakref
# WARNING: Decompyle incomplete
