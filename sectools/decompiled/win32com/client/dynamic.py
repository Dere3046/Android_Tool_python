
'''Support for dynamic COM client support.

Introduction
 Dynamic COM client support is the ability to use a COM server without
 prior knowledge of the server.  This can be used to talk to almost all
 COM servers, including much of MS Office.

 In general, you should not use this module directly - see below.

Example
 >>> import win32com.client
 >>> xl = win32com.client.Dispatch("Excel.Application")
 # The line above invokes the functionality of this class.
 # xl is now an object we can use to talk to Excel.
 >>> xl.Visible = 1 # The Excel window becomes visible.

'''
import sys
import traceback
import types
import pythoncom
import winerror
from  import build
from pywintypes import IIDType
import win32com.client as win32com
debugging = 0
debugging_attr = 0
LCID = 0
ERRORS_BAD_CONTEXT = [
    winerror.DISP_E_MEMBERNOTFOUND,
    winerror.DISP_E_BADPARAMCOUNT,
    winerror.DISP_E_PARAMNOTOPTIONAL,
    winerror.DISP_E_TYPEMISMATCH,
    winerror.E_INVALIDARG]
ALL_INVOKE_TYPES = [
    pythoncom.INVOKE_PROPERTYGET,
    pythoncom.INVOKE_PROPERTYPUT,
    pythoncom.INVOKE_PROPERTYPUTREF,
    pythoncom.INVOKE_FUNC]

def debug_print(*args):
    if debugging:
        for arg in args:
            print(arg, ' ', **('end',))
        print()
        return None


def debug_attr_print(*args):
    if debugging_attr:
        for arg in args:
            print(arg, ' ', **('end',))
        print()
        return None


def MakeMethod(func, inst, cls):
    return types.MethodType(func, inst)

PyIDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]
PyIUnknownType = pythoncom.TypeIIDs[pythoncom.IID_IUnknown]
_GoodDispatchTypes = (str, IIDType)
_defaultDispatchItem = build.DispatchItem

def _GetGoodDispatch(IDispatch, clsctx = (pythoncom.CLSCTX_SERVER,)):
    if isinstance(IDispatch, PyIDispatchType):
        return IDispatch
# WARNING: Decompyle incomplete


def _GetGoodDispatchAndUserName(IDispatch, userName, clsctx):
    if userName is None:
        if isinstance(IDispatch, str):
            userName = IDispatch
        else:
            userName = str(userName)
    return (_GetGoodDispatch(IDispatch, clsctx), userName)


def _GetDescInvokeType(entry, invoke_type):
    if not entry or entry.desc:
        return invoke_type
    if None.desc.desckind == pythoncom.DESCKIND_VARDESC:
        return invoke_type
    return None.desc.invkind


def Dispatch(IDispatch, userName, createClass, typeinfo, UnicodeToString, clsctx = (None, None, None, None, pythoncom.CLSCTX_SERVER)):
    pass
# WARNING: Decompyle incomplete


def MakeOleRepr(IDispatch, typeinfo, typecomp):
    olerepr = None
# WARNING: Decompyle incomplete


def DumbDispatch(IDispatch, userName, createClass, UnicodeToString, clsctx = (None, None, None, pythoncom.CLSCTX_SERVER)):
    '''Dispatch with no type info'''
    pass
# WARNING: Decompyle incomplete


class CDispatch:
    
    def __init__(self, IDispatch, olerepr, userName, UnicodeToString, lazydata = (None, None, None)):
        pass
    # WARNING: Decompyle incomplete

    
    def __call__(self, *args):
        """Provide 'default dispatch' COM functionality - allow instance to be called"""
        if self._olerepr_.defaultDispatchName:
            (invkind, dispid) = self._find_dispatch_type_(self._olerepr_.defaultDispatchName)
        else:
            invkind = pythoncom.DISPATCH_METHOD | pythoncom.DISPATCH_PROPERTYGET
            dispid = pythoncom.DISPID_VALUE
    # WARNING: Decompyle incomplete

    
    def __bool__(self):
        return True

    
    def __repr__(self):
        return '<COMObject %s>' % self._username_

    
    def __str__(self):
        pass
    # WARNING: Decompyle incomplete

    
    def __dir__(self):
        lst = list(self.__dict__.keys()) + dir(self.__class__) + self._dir_ole_()
    # WARNING: Decompyle incomplete

    
    def _dir_ole_(self):
        items_dict = { }
        for iTI in range(0, self._oleobj_.GetTypeInfoCount()):
            typeInfo = self._oleobj_.GetTypeInfo(iTI)
            self._Update