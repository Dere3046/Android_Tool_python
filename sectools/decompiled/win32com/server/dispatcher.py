
__doc__ = 'Dispatcher\n\nPlease see policy.py for a discussion on dispatchers and policies\n'
import pythoncom
import traceback
import win32api
from sys import exc_info
from win32com.server.exception import IsCOMServerException
from win32com.util import IIDToInterfaceName
import win32com

class DispatcherBase:
    '''The base class for all Dispatchers.

    This dispatcher supports wrapping all operations in exception handlers,
    and all the necessary delegation to the policy.

    This base class supports the printing of "unexpected" exceptions.  Note, however,
    that exactly where the output of print goes may not be useful!  A derived class may
    provide additional semantics for this.
    '''
    
    def __init__(self, policyClass, object):
        self.policy = policyClass(object)
        self.logger = getattr(win32com, 'logger', None)

    
    def _CreateInstance_(self, clsid, reqIID):
        
        try:
            self.policy._CreateInstance_(clsid, reqIID)
        finally:
            return None
            return None


    
    def _QueryInterface_(self, iid):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _Invoke_(self, dispid, lcid, wFlags, args):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _GetIDsOfNames_(self, names, lcid):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _GetTypeInfo_(self, index, lcid):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _GetTypeInfoCount_(self):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _GetDispID_(self, name, fdex):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _InvokeEx_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _DeleteMemberByName_(self, name, fdex):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _DeleteMemberByDispID_(self, id):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _GetMemberProperties_(self, id, fdex):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _GetMemberName_(self, dispid):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _GetNextDispID_(self, fdex, flags):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _GetNameSpaceParent_(self):
        
        try:
            pass
        finally:
            return None
            return None


    
    def _HandleException_(self):
        '''Called whenever an exception is raised.

        Default behaviour is to print the exception.
        '''
        if not IsCOMServerException():
            if self.logger is not None:
                self.logger.exception('pythoncom server error')
                raise 
            None.print_exc()
        raise 

    
    def _trace_(self, *args):
        if self.logger is not None:
            record = ' '.join(map(str, args))
            self.logger.debug(record)
            return None
        for arg in None[:-1]:
            print(arg, ' ', **('end',))
        print(args[-1])



class DispatcherTrace(DispatcherBase):
    """A dispatcher, which causes a 'print' line for each COM function called."""
    
    def _QueryInterface_(self, iid):
        rc = DispatcherBase._QueryInterface_(self, iid)
        if not rc:
            self._trace_('in %s._QueryInterface_ with unsupported IID %s (%s)' % (repr(self.policy._obj_), IIDToInterfaceName(iid), iid))
        return rc

    
    def _GetIDsOfNames_(self, names, lcid):
        self._trace_("in _GetIDsOfNames_ with '%s' and '%d'\n" % (names, lcid))
        return DispatcherBase._GetIDsOfNames_(self, names, lcid)

    
    def _GetTypeInfo_(self, index, lcid):
        self._trace_('in _GetTypeInfo_ with index=%d, lcid=%d\n' % (index, lcid))
        return DispatcherBase._GetTypeInfo_(self, index, lcid)

    
    def _GetTypeInfoCount_(self):
        self._trace_('in _GetTypeInfoCount_\n')
        return DispatcherBase._GetTypeInfoCount_(self)

    
    def _Invoke_(self, dispid, lcid, wFlags, args):
        self._trace_('in _Invoke_ with', dispid, lcid, wFlags, args)
        return DispatcherBase._Invoke_(self, dispid, lcid, wFlags, args)

    
    def _GetDispID_(self, name, fdex):
        self._trace_('in _GetDispID_ with', name, fdex)
        return DispatcherBase._GetDispID_(self, name, fdex)

    
    def _InvokeEx_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider):
        self._trace_('in %r._InvokeEx_-%s%r [%x,%s,%r]' % (self.policy._obj_, dispid, args, wFlags, lcid, serviceProvider))
        return DispatcherBase._InvokeEx_(self, dispid, lcid, wFlags, args, kwargs, serviceProvider)

    
    def _DeleteMemberByName_(self, name, fdex):
        self._trace_('in _DeleteMemberByName_ with', name, fdex)
        return DispatcherBase._DeleteMemberByName_(self, name, fdex)

    
    def _DeleteMemberByDispID_(self, id):
        self._trace_('in _DeleteMemberByDispID_ with', id)
        return DispatcherBase._DeleteMemberByDispID_(self, id)

    
    def _GetMemberProperties_(self, id, fdex):
        self._trace_('in _GetMemberProperties_ with', id, fdex)
        return DispatcherBase._GetMemberProperties_(self, id, fdex)

    
    def _GetMemberName_(self, dispid):
        self._trace_('in _GetMemberName_ with', dispid)
        return DispatcherBase._GetMemberName_(self, dispid)

    
    def _GetNextDispID_(self, fdex, flags):
        self._trace_('in _GetNextDispID_ with', fdex, flags)
        return DispatcherBase._GetNextDispID_(self, fdex, flags)

    
    def _GetNameSpaceParent_(self):
        self._trace_('in _GetNameSpaceParent_')
        return DispatcherBase._GetNameSpaceParent_(self)



class DispatcherWin32trace(DispatcherTrace):
    '''A tracing dispatcher that sends its output to the win32trace remote collector.'''
    
    def __init__(self, policyClass, object):
        DispatcherTrace.__init__(self, policyClass, object)
        if self.logger is None:
            import win32traceutil
        self._trace_('Object with win32trace dispatcher created (object=%s)' % repr(object))



class DispatcherOutputDebugString(DispatcherTrace):
    '''A tracing dispatcher that sends its output to win32api.OutputDebugString'''
    
    def _trace_(self, *args):
        for arg in args[:-1]:
            win32api.OutputDebugString(str(arg) + ' ')
        win32api.OutputDebugString(str(args[-1]) + '\n')



class DispatcherWin32dbg(DispatcherBase):
    '''A source-level debugger dispatcher

    A dispatcher which invokes the debugger as an object is instantiated, or
    when an unexpected exception occurs.

    Requires Pythonwin.
    '''
    
    def __init__(self, policyClass, ob):
        pywin.debugger.brk()
        print('The DispatcherWin32dbg dispatcher is deprecated!')
        print('Please let me know if this is a problem.')
        print('Uncomment the relevant lines in dispatcher.py to re-enable')
        DispatcherBase.__init__(self, policyClass, ob)

    
    def _HandleException_(self):
        '''Invoke the debugger post mortem capability'''
        (typ, val, tb) = exc_info()
        debug = 0
    # WARNING: Decompyle incomplete


# WARNING: Decompyle incomplete
