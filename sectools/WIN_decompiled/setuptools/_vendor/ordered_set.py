
__doc__ = '\nAn OrderedSet is a custom MutableSet that remembers its order, so that every\nentry has an index that can be looked up.\n\nBased on a recipe originally posted to ActiveState Recipes by Raymond Hettiger,\nand released under the MIT license.\n'
import itertools as it
from collections import deque
# WARNING: Decompyle incomplete
