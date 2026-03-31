
__doc__ = 'A multi-producer, multi-consumer queue.'
import threading
import types
from collections import deque
from heapq import heappush, heappop
from time import monotonic as time
# WARNING: Decompyle incomplete
