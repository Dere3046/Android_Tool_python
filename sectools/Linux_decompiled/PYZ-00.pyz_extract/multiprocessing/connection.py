
__all__ = [
    'Client',
    'Listener',
    'Pipe',
    'wait']
import io
import os
import sys
import socket
import struct
import time
import tempfile
import itertools
import _multiprocessing
from  import util
from  import AuthenticationError, BufferTooShort
from context import reduction
_ForkingPickler = reduction.ForkingPickler
# WARNING: Decompyle incomplete
