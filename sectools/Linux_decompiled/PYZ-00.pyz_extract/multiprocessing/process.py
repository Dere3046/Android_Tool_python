
__all__ = [
    'BaseProcess',
    'current_process',
    'active_children',
    'parent_process']
import os
import sys
import signal
import itertools
import threading
from _weakrefset import WeakSet
# WARNING: Decompyle incomplete
