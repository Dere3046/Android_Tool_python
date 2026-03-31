
'''General client side utilities.

This module contains utility functions, used primarily by advanced COM
programmers, or other COM modules.
'''
import pythoncom
from win32com.client import Dispatch, _get_good_object_
PyIDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]

def WrapEnum(ob, resultCLSID = (None,)):
    '''Wrap an object in a VARIANT enumerator.

    All VT_DISPATCHs returned by the enumerator are converted to wrapper objects
    (which may be either a class instance, or a dynamic.Dispatch type object).

    '''
    if type(ob) != pythoncom.TypeIIDs[pythoncom.IID_IEnumVARIANT]:
        ob = ob.QueryInterface(pythoncom.IID_IEnumVARIANT)
    return EnumVARIANT(ob, resultCLSID)


class Enumerator:
    '''A class that provides indexed access into an Enumerator

    By wrapping a PyIEnum* object in this class, you can perform
    natural looping and indexing into the Enumerator.

    Looping is very efficient, but it should be noted that although random
    access is supported, the underlying object is still an enumerator, so
    this will force many reset-and-seek operations to find the requested index.

    '''
    
    def __init__(self, enum):
        self._oleobj_ = enum
        self.index = -1

    
    def __getitem__(self, index):
        return self.__GetIndex(index)

    
    def __call__(self, index):
        return self.__GetIndex(index)

    
    def __GetIndex(self, index):
        if type(index) != type(0):
            raise TypeError('Only integer indexes are supported for enumerators')
        if None != self.index + 1:
            self._oleobj_.Reset()
            if index:
                self._oleobj_.Skip(index)
        self.index = index
        result = self._oleobj_.Next(1)
        if len(result):
            return self._make_retval_(result[0])
        raise None('list index out of range')

    
    def Next(self, count = (1,)):
        ret = self._oleobj_.Next(count)
        realRets = []
        for r in ret:
            realRets.append(self._make_retval_(r))
        return tuple(realRets)

    
    def Reset(self):
        return self._oleobj_.Reset()

    
    def Clone(self):
        return self.__class__(self._oleobj_.Clone(), self.resultCLSID)

    
    def _make_retval_(self, result):
        return result



class EnumVARIANT(Enumerator):
    
    def __init__(self, enum, resultCLSID = (None,)):
        self.resultCLSID = resultCLSID
        Enumerator.__init__(self, enum)

    
    def _make_retval_(self, result):
        return _get_good_object_(result, self.resultCLSID, **('resultCLSID',))



class Iterator:
    
    def __init__(self, enum, resultCLSID = (None,)):
        self.resultCLSID = resultCLSID
        self._iter_ = iter(enum.QueryInterface(pythoncom.IID_IEnumVARIANT))

    
    def __iter__(self):
        return self

    
    def __next__(self):
        return _get_good_object_(next(self._iter_), self.resultCLSID, **('resultCLSID',))


