
import sys
from  import context
__all__ = (lambda .0: [ x for x in .0 if x.startswith('_') ])(dir(context._default_context))
globals().update((lambda .0: for name in .0:
(name, getattr(context._default_context, name)))(__all__))
SUBDEBUG = 5
SUBWARNING = 25
if '__main__' in sys.modules:
    sys.modules['__mp_main__'] = sys.modules['__main__']
    return None
