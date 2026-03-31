
import sys

def disable_importlib_metadata_finder(metadata):
    """
    Ensure importlib_metadata doesn't provide older, incompatible
    Distributions.

    Workaround for #3102.
    """
    pass
# WARNING: Decompyle incomplete

if sys.version_info < (3, 10):
    from setuptools.extern import importlib_metadata as metadata
    disable_importlib_metadata_finder(metadata)
else:
    from importlib.metadata import metadata
if sys.version_info < (3, 9):
    from setuptools.extern import importlib_resources as resources
    return None
from importlib.resources import resources
