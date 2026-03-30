
import abc
import sys
import pathlib
from contextlib import suppress
if sys.version_info >= (3, 10):
    from zipfile import Path as ZipPath
else:
    from zipp import Path as ZipPath
# WARNING: Decompyle incomplete
