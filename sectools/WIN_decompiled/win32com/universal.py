
import types
import pythoncom
from win32com.client import gencache
com_error = pythoncom.com_error
_univgw = pythoncom._univgw

def RegisterInterfaces(typelibGUID, lcid, major, minor, interface_names = (None,)):
    ret = []
# WARNING: Decompyle incomplete


def _doCreateVTable(iid, interface_name, is_dispatch, method_defs):
    defn = Definition(iid, is_dispatch, method_defs)
    vtbl = _univgw.CreateVTable(defn, is_dispatch)
    _univgw.RegisterVTable(vtbl, iid, interface_name)


def _CalcTypeSize(typeTuple):
    t = typeTuple[0]
    if t & (pythoncom.VT_BYREF | pythoncom.VT_ARRAY):
        cb = _univgw.SizeOfVT(pythoncom.VT_PTR)[1]
        return cb
    if None == pythoncom.VT_RECORD:
        cb = _univgw.SizeOfVT(pythoncom.VT_PTR)[1]
        return cb
    cb = None.SizeOfVT(t)[1]
    return cb


class Arg:
    
    def __init__(self, arg_info, name = (None,)):
        self.name = name
        (self.vt, self.inOut, self.default, self.clsid) = arg_info
        self.size = _CalcTypeSize(arg_info)
        self.offset = 0



class Method:
    
    def __init__(self, method_info, isEventSink = (0,)):
        (all_names, dispid, desc) = method_info
        name = all_names[0]
        names = all_names[1:]
        invkind = desc[4]
        arg_defs = desc[2]
        ret_def = desc[8]
        self.dispid = dispid
        self.invkind = invkind
        if isEventSink and name[:2] != 'On':
            name = 'On%s' % name
        self.name = name
        cbArgs = 0
        self.args = []
        for argDesc in arg_defs:
            arg = Arg(argDesc)
            arg.offset = cbArgs
            cbArgs = cbArgs + arg.size
            self.args.append(arg)
        self.cbArgs = cbArgs
        self._gw_in_args = self._GenerateInArgTuple()
        self._gw_out_args = self._GenerateOutArgTuple()

    
    def _GenerateInArgTuple(self):
        l = []
        for arg in self.args:
            if arg.inOut & pythoncom.PARAMFLAG_FIN or arg.inOut == 0:
                l.append((arg.vt, arg.offset, arg.size))
        return tuple(l)

    
    def _GenerateOutArgTuple(self):
        l = []
        for arg in self.args:
            if arg.inOut & pythoncom.PARAMFLAG_FOUT and arg.inOut & pythoncom.PARAMFLAG_FRETVAL or arg.inOut == 0:
                l.append((arg.vt, arg.offset, arg.size, arg.clsid))
        return tuple(l)



class Definition:
    
    def __init__(self, iid, is_dispatch, method_defs):
        self._iid = iid
        self._methods = []
        self._is_dispatch = is_dispatch
        for info in method_defs:
            entry = Method(info)
            self._methods.append(entry)

    
    def iid(self):
        return self._iid

    
    def vtbl_argsizes(self):
        return (lambda .0: [ m.cbArgs for m in .0 ])(self._methods)

    
    def vtbl_argcounts(self):
        return (lambda .0: [ len(m.args) for m in .0 ])(self._methods)

    
    def dispatch(self, ob, index, argPtr, ReadFromInTuple, WriteFromOutTuple = (_univgw.ReadFromInTuple, _univgw.WriteFromOutTuple)):
        '''Dispatch a call to an interface method.'''
        meth = self._methods[index]
        hr = 0
        args = ReadFromInTuple(meth._gw_in_args, argPtr)
        ob = getattr(ob, 'policy', ob)
        ob._dispid_to_func_[meth.dispid] = meth.name
        retVal = ob._InvokeEx_(meth.dispid, 0, meth.invkind, args, None, None)
        if type(retVal) == tuple:
            if len(retVal) == len(meth._gw_out_args) + 1:
                hr = retVal[0]
                retVal = retVal[1:]
            else:
                raise TypeError('Expected %s return values, got: %s' % (len(meth._gw_out_args) + 1, len(retVal)))
            retVal = [
                None]
            retVal.extend([
                None] * (len(meth._gw_out_args) - 1))
            retVal = tuple(retVal)
            WriteFromOutTuple(retVal, meth._gw_out_args, argPtr)
            return hr


