
import atexit
import os
import shutil
import tempfile
supportdir = tempfile.mkdtemp()
genpydir = os.path.join(supportdir, 'gen_py')
# WARNING: Decompyle incomplete
