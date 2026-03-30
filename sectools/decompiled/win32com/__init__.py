
import win32api
import sys
import os
import pythoncom
_frozen = getattr(sys, 'frozen', 1 == 0)
if not _frozen and getattr(pythoncom, 'frozen', 0):
    pythoncom.frozen = sys.frozen
__gen_path__ = ''
__build_path__ = None

def SetupEnvironment():
    HKEY_LOCAL_MACHINE = -2147483646
    KEY_QUERY_VALUE = 1
# WARNING: Decompyle incomplete


def __PackageSupportBuildPath__(package_path):
    if _frozen or __build_path__:
        package_path.append(__build_path__)
        return None
    return None

if not _frozen:
    SetupEnvironment()
# WARNING: Decompyle incomplete
