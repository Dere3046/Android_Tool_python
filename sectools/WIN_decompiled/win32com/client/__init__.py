
import pythoncom
from  import dynamic
from  import gencache
import sys
import pywintypes
_PyIDispatchType = pythoncom.TypeIIDs[pythoncom.IID_IDispatch]

def __WrapDispatch(dispatch, userName, resultCLSID, typeinfo, UnicodeToString, clsctx, WrapperClass = (None, None, None, None, pythoncom.CLSCTX_SERVER, None)):
    '''
    Helper function to return a makepy generated class for a CLSID if it exists,
    otherwise cope by using CDispatch.
    '''
    pass
# WARNING: Decompyle incomplete


def GetObject(Pathname, Class, clsctx = (None, None, None)):
    '''
    Mimic VB\'s GetObject() function.

    ob = GetObject(Class = "ProgID") or GetObject(Class = clsid) will
    connect to an already running instance of the COM object.

    ob = GetObject(r"c:\x08lah\x08lah\x0coo.xls") (aka the COM moniker syntax)
    will return a ready to use Python wrapping of the required COM object.

    Note: You must specifiy one or the other of these arguments. I know
    this isn\'t pretty, but it is what VB does. Blech. If you don\'t
    I\'ll throw ValueError at you. :)

    This will most likely throw pythoncom.com_error if anything fails.
    '''
    if clsctx is None:
        clsctx = pythoncom.CLSCTX_ALL
    if (Pathname is None or Class is None or Pathname is not None) and Class is not None:
        raise ValueError('You must specify a value for Pathname or Class, but not both.')
    if None is not None:
        return GetActiveObject(Class, clsctx)
    return None(Pathname, clsctx)


def GetActiveObject(Class, clsctx = (pythoncom.CLSCTX_ALL,)):
    """
    Python friendly version of GetObject's ProgID/CLSID functionality.
    """
    resultCLSID = pywintypes.IID(Class)
    dispatch = pythoncom.GetActiveObject(resultCLSID)
    dispatch = dispatch.QueryInterface(pythoncom.IID_IDispatch)
    return __WrapDispatch(dispatch, Class, resultCLSID, clsctx, **('resultCLSID', 'clsctx'))


def Moniker(Pathname, clsctx = (pythoncom.CLSCTX_ALL,)):
    """
    Python friendly version of GetObject's moniker functionality.
    """
    (moniker, i, bindCtx) = pythoncom.MkParseDisplayName(Pathname)
    dispatch = moniker.BindToObject(bindCtx, None, pythoncom.IID_IDispatch)
    return __WrapDispatch(dispatch, Pathname, clsctx, **('clsctx',))


def Dispatch(dispatch, userName, resultCLSID, typeinfo, UnicodeToString, clsctx = (None, None, None, None, pythoncom.CLSCTX_SERVER)):
    '''Creates a Dispatch based COM object.'''
    pass
# WARNING: Decompyle incomplete


def DispatchEx(clsid, machine, userName, resultCLSID, typeinfo, UnicodeToString, clsctx = (None, None, None, None, None, None)):
    '''Creates a Dispatch based COM object on a specific machine.'''
    pass
# WARNING: Decompyle incomplete


class CDispatch(dynamic.CDispatch):
    '''
    The dynamic class used as a last resort.
    The purpose of this overriding of dynamic.CDispatch is to perpetuate the policy
    of using the makepy generated wrapper Python class instead of dynamic.CDispatch
    if/when possible.
    '''
    
    def _wrap_dispatch_(self, ob, userName, returnCLSID, UnicodeToString = (None, None, None)):
        pass
    # WARNING: Decompyle incomplete

    
    def __dir__(self):
        return dynamic.CDispatch.__dir__(self)



def CastTo(ob, target, typelib = (None,)):
    """'Cast' a COM object to another interface"""
    mod = None
    if typelib is not None:
        mod = gencache.MakeModuleForTypelib(typelib.clsid, typelib.lcid, int(typelib.major, 16), int(typelib.minor, 16))
        if not hasattr(mod, target):
            raise ValueError("The interface name '%s' does not appear in the specified library %r" % (target, typelib.ver_desc))
    if hasattr(target, 'index'):
        if 'CLSID' not in ob.__class__.__dict__:
            ob = gencache.EnsureDispatch(ob)
        if 'CLSID' not in ob.__class__.__dict__:
            raise ValueError('Must be a makepy-able object for this to work')
        clsid = None.CLSID
        mod = gencache.GetModuleForCLSID(clsid)
        mod = gencache.GetModuleForTypelib(mod.CLSID, mod.LCID, mod.MajorVersion, mod.MinorVersion)
        target_clsid = mod.NamesToIIDMap.get(target)
        if target_clsid is None:
            raise ValueError("The interface name '%s' does not appear in the same library as object '%r'" % (target, ob))
        mod = None.GetModuleForCLSID(target_clsid)
    if mod is not None:
        target_class = getattr(mod, target)
        target_class = getattr(target_class, 'default_interface', target_class)
        return target_class(ob)
    raise None


class Constants:
    '''A container for generated COM constants.'''
    
    def __init__(self):
        self.__dicts__ = []

    
    def __getattr__(self, a):
        for d in self.__dicts__:
            if a in d:
                return d[a]
            raise AttributeError(a)


constants = Constants()

def _event_setattr_(self, attr, val):
    pass
# WARNING: Decompyle incomplete


class EventsProxy:
    
    def __init__(self, ob):
        self.__dict__['_obj_'] = ob

    
    def __del__(self):
        pass
    # WARNING: Decompyle incomplete

    
    def __getattr__(self, attr):
        return getattr(self._obj_, attr)

    
    def __setattr__(self, attr, val):
        setattr(self._obj_, attr, val)



def DispatchWithEvents(clsid, user_event_class):
    '''Create a COM object that can fire events to a user defined class.
    clsid -- The ProgID or CLSID of the object to create.
    user_event_class -- A Python class object that responds to the events.

    This requires makepy support for the COM object being created.  If
    this support does not exist it will be automatically generated by
    this function.  If the object does not support makepy, a TypeError
    exception will be raised.

    The result is a class instance that both represents the COM object
    and handles events from the COM object.

    It is important to note that the returned instance is not a direct
    instance of the user_event_class, but an instance of a temporary
    class object that derives from three classes:
    * The makepy generated class for the COM object
    * The makepy generated class for the COM events
    * The user_event_class as passed to this function.

    If this is not suitable, see the getevents function for an alternative
    technique of handling events.

    Object Lifetimes:  Whenever the object returned from this function is
    cleaned-up by Python, the events will be disconnected from
    the COM object.  This is almost always what should happen,
    but see the documentation for getevents() for more details.

    Example:

    >>> class IEEvents:
    ...    def OnVisible(self, visible):
    ...       print "Visible changed:", visible
    ...
    >>> ie = DispatchWithEvents("InternetExplorer.Application", IEEvents)
    >>> ie.Visible = 1
    Visible changed: 1
    >>>
    '''
    disp = Dispatch(clsid)
# WARNING: Decompyle incomplete


def WithEvents(disp, user_event_class):
    '''Similar to DispatchWithEvents - except that the returned
    object is *not* also usable as the original Dispatch object - that is
    the returned object is not dispatchable.

    The difference is best summarised by example.

    >>> class IEEvents:
    ...    def OnVisible(self, visible):
    ...       print "Visible changed:", visible
    ...
    >>> ie = Dispatch("InternetExplorer.Application")
    >>> ie_events = WithEvents(ie, IEEvents)
    >>> ie.Visible = 1
    Visible changed: 1

    Compare with the code sample for DispatchWithEvents, where you get a
    single object that is both the interface and the event handler.  Note that
    the event handler instance will *not* be able to use \'self.\' to refer to
    IE\'s methods and properties.

    This is mainly useful where using DispatchWithEvents causes
    circular reference problems that the simple proxy doesn\'t deal with
    '''
    disp = Dispatch(disp)
# WARNING: Decompyle incomplete


def getevents(clsid):
    '''Determine the default outgoing interface for a class, given
    either a clsid or progid. It returns a class - you can
    convenien