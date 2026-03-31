
from __future__ import annotations
import hmac

def bytes_eq(a = None, b = None):
    if not isinstance(a, bytes) or isinstance(b, bytes):
        raise TypeError('a and b must be bytes.')
    return None.compare_digest(a, b)

