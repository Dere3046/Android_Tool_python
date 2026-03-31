
'''Utilities for selecting and enumerating the Type Libraries installed on the system
'''
import win32api
import win32con
import pythoncom

class TypelibSpec:
    
    def __init__(self, clsid, lcid, major, minor, flags = (0,)):
        self.clsid = str(clsid)
        self.lcid = int(lcid)
        self.major = major
        self.minor = minor
        self.dll = None
        self.desc = None
        self.ver_desc = None
        self.flags = flags

    
    def __getitem__(self, item):
        if item == 0:
            return self.ver_desc
        raise None('Cant index me!')

    
    def __lt__(self, other):
        if not self.ver_desc:
            pass
        if not self.desc:
            pass
        me = (''.lower(), ''.lower(), self.major, self.minor)
        if not other.ver_desc:
            pass
        if not other.desc:
            pass
        them = (''.lower(), ''.lower(), other.major, other.minor)
        return me < them

    
    def __eq__(self, other):
        if not self.ver_desc:
            pass
        if not other.ver_desc:
            pass
        if ''.lower() == ''.lower():
            if not self.desc:
                pass
            if not other.desc:
                pass
            if ''.lower() == ''.lower() and self.major == other.major:
                pass
        return self.minor == other.minor

    
    def Resolve(self):
        if self.dll is None:
            return 0
        tlb = None.LoadTypeLib(self.dll)
        self.FromTypelib(tlb, None)
        return 1

    
    def FromTypelib(self, typelib, dllName = (None,)):
        la = typelib.GetLibAttr()
        self.clsid = str(la[0])
        self.lcid = la[1]
        self.major = la[3]
        self.minor = la[4]
        if dllName:
            self.dll = dllName
            return None



def EnumKeys(root):
    index = 0
    ret = []
# WARNING: Decompyle incomplete

FLAG_RESTRICTED = 1
FLAG_CONTROL = 2
FLAG_HIDDEN = 4

def EnumTlbs(excludeFlags = (0,)):
    '''Return a list of TypelibSpec objects, one for each registered library.'''
    key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT, 'Typelib')
    iids = EnumKeys(key)
    results = []
# WARNING: Decompyle incomplete


def FindTlbsWithDescription(desc):
    '''Find all installed type libraries with the specified description'''
    ret = []
    items = EnumTlbs()
    for item in items:
        if item.desc == desc:
            ret.append(item)
    return ret


def SelectTlb(title, excludeFlags = ('Select Library', 0)):
    '''Display a list of all the type libraries, and select one.   Returns None if cancelled'''
    import pywin.dialogs.list as pywin
    items = EnumTlbs(excludeFlags)
    for i in items:
        i.major = int(i.major, 16)
        i.minor = int(i.minor, 16)
    items.sort()
    rc = pywin.dialogs.list.SelectFromLists(title, items, [
        'Type Library'])
    if rc is None:
        return None
    return None[rc]

if __name__ == '__main__':
    print(SelectTlb().__dict__)
    return None
