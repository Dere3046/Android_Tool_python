
'''Contains knowledge to build a COM object definition.

This module is used by both the @dynamic@ and @makepy@ modules to build
all knowledge of a COM object.

This module contains classes which contain the actual knowledge of the object.
This include parameter and return type information, the COM dispid and CLSID, etc.

Other modules may use this information to generate .py files, use the information
dynamically, or possibly even generate .html documentation for objects.
'''
import sys
import string
from keyword import iskeyword
import pythoncom
from pywintypes import TimeType
import winerror
import datetime

def _makeDocString(s):
    if sys.version_info < (3,):
        s = s.encode('mbcs')
    return repr(s)

error = 'PythonCOM.Client.Build error'

class NotSupportedException(Exception):
    pass

DropIndirection = 'DropIndirection'
NoTranslateTypes = [
    pythoncom.VT_BOOL,
    pythoncom.VT_CLSID,
    pythoncom.VT_CY,
    pythoncom.VT_DATE,
    pythoncom.VT_DECIMAL,
    pythoncom.VT_EMPTY,
    pythoncom.VT_ERROR,
    pythoncom.VT_FILETIME,
    pythoncom.VT_HRESULT,
    pythoncom.VT_I1,
    pythoncom.VT_I2,
    pythoncom.VT_I4,
    pythoncom.VT_I8,
    pythoncom.VT_INT,
    pythoncom.VT_NULL,
    pythoncom.VT_R4,
    pythoncom.VT_R8,
    pythoncom.VT_NULL,
    pythoncom.VT_STREAM,
    pythoncom.VT_UI1,
    pythoncom.VT_UI2,
    pythoncom.VT_UI4,
    pythoncom.VT_UI8,
    pythoncom.VT_UINT,
    pythoncom.VT_VOID]
NoTranslateMap = { }
for v in NoTranslateTypes:
    NoTranslateMap[v] = None

class MapEntry:
    '''Simple holder for named attibutes - items in a map.'''
    
    def __init__(self, desc_or_id, names, doc, resultCLSID, resultDoc, hidden = (None, None, pythoncom.IID_NULL, None, 0)):
        if type(desc_or_id) == type(0):
            self.dispid = desc_or_id
            self.desc = None
        else:
            self.dispid = desc_or_id[0]
            self.desc = desc_or_id
        self.names = names
        self.doc = doc
        self.resultCLSID = resultCLSID
        self.resultDocumentation = resultDoc
        self.wasProperty = 0
        self.hidden = hidden

    
    def __repr__(self):
        return 'MapEntry(dispid={s.dispid}, desc={s.desc}, names={s.names}, doc={s.doc!r}, resultCLSID={s.resultCLSID}, resultDocumentation={s.resultDocumentation}, wasProperty={s.wasProperty}, hidden={s.hidden}'.format(self, **('s',))

    
    def GetResultCLSID(self):
        rc = self.resultCLSID
        if rc == pythoncom.IID_NULL:
            return None

    
    def GetResultCLSIDStr(self):
        rc = self.GetResultCLSID()
        if rc is None:
            return 'None'
        return None(str(rc))

    
    def GetResultName(self):
        if self.resultDocumentation is None:
            return None
        return None.resultDocumentation[0]



class OleItem:
    typename = 'OleItem'
    
    def __init__(self, doc = (None,)):
        self.doc = doc
        if self.doc:
            self.python_name = MakePublicAttributeName(self.doc[0])
        else:
            self.python_name = None
        self.bWritten = 0
        self.bIsDispatch = 0
        self.bIsSink = 0
        self.clsid = None
        self.co_class = None



class DispatchItem(OleItem):
    typename = 'DispatchItem'
    
    def __init__(self, typeinfo, attr, doc, bForUser = (None, None, None, 1)):
        OleItem.__init__(self, doc)
        self.propMap = { }
        self.propMapGet = { }
        self.propMapPut = { }
        self.mapFuncs = { }
        self.defaultDispatchName = None
        self.hidden = 0
        if typeinfo:
            self.Build(typeinfo, attr, bForUser)
            return None

    
    def _propMapPutCheck_(self, key, item):
        (ins, outs, opts) = self.CountInOutOptArgs(item.desc[2])
        if ins > 1:
            if opts + 1 == ins or ins == item.desc[6] + 1:
                newKey = 'Set' + key
                deleteExisting = 0
            else:
                deleteExisting = 1
                if key in self.mapFuncs or key in self.propMapGet:
                    newKey = 'Set' + key
                else:
                    newKey = key
            item.wasProperty = 1
            self.mapFuncs[newKey] = item
            if deleteExisting:
                del self.propMapPut[key]
                return None
            return None

    
    def _propMapGetCheck_(self, key, item):
        (ins, outs, opts) = self.CountInOutOptArgs(item.desc[2])
        if ins > 0:
            if item.desc[6] == ins or ins == opts:
                newKey = 'Get' + key
                deleteExisting = 0
            else:
                deleteExisting = 1
                if key in self.mapFuncs:
                    newKey = 'Get' + key
                else:
                    newKey = key
            item.wasProperty = 1
            self.mapFuncs[newKey] = item
            if deleteExisting:
                del self.propMapGet[key]
                return None
            return None

    
    def _AddFunc_(self, typeinfo, fdesc, bForUser):
        pass
    # WARNING: Decompyle incomplete

    
    def _AddVar_(self, typeinfo, vardesc, bForUser):
        pass
    # WARNING: Decompyle incomplete

    
    def Build(self, typeinfo, attr, bForUser = (1,)):
        self.clsid = attr[0]
        self.bIsDispatch = attr.wTypeFlags & pythoncom.TYPEFLAG_FDISPATCHABLE != 0
        if typeinfo is None:
            return None
        for j in None(attr[6]):
            fdesc = typeinfo.GetFuncDesc(j)
            self._AddFunc_(typeinfo, fdesc, bForUser)
        for j in range(attr[7]):
            fdesc = typeinfo.GetVarDesc(j)
            self._AddVar_(typeinfo, fdesc, bForUser)
        for key, item in list(self.propMapGet.items()):
            self._propMapGetCheck_(key, item)
        for key, item in list(self.propMapPut.items()):
            self._propMapPutCheck_(key, item)

    
    def CountInOutOptArgs(self, argTuple):
        '''Return tuple counting in/outs/OPTS.  Sum of result may not be len(argTuple), as some args may be in/out.'''
        ins = out = opts = 0
        for argCheck in argTuple:
            inOut = argCheck[1]
            if inOut == 0:
                ins = ins + 1
                out = out + 1
                continue
            if inOut & pythoncom.PARAMFLAG_FIN:
                ins = ins + 1
            if inOut & pythoncom.PARAMFLAG_FOPT:
                opts = opts + 1
            if inOut & pythoncom.PARAMFLAG_FOUT:
                out = out + 1
        return (ins, out, opts)

    
    def MakeFuncMethod(self, entry, name, bMakeClass = (1,)):
        if entry.desc is not None:
            if len(entry.desc) < 6 or entry.desc[6] != -1:
                return self.MakeDispatchFuncMethod(entry, name, bMakeClass)
            return None.MakeVarArgsFuncMethod(entry, name, bMakeClass)

    
    def MakeDispatchFuncMethod(self, entry, name, bMakeClass = (1,)):
        fdesc = entry.desc
        doc = entry.doc
        names = entry.names
        ret = []
        if bMakeClass:
            linePrefix = '\t'
            defNamedOptArg = 'defaultNamedOptArg'
            defNamedNotOptArg = 'defaultNamedNotOptArg'
            defUnnamedArg = 'defaultUnnamedArg'
        else:
            linePrefix = ''
            defNamedOptArg = 'pythoncom.Missing'
            defNamedNotOptArg = 'pythoncom.Missing'
            defUnnamedArg = 'pythoncom.Missing'
        defOutArg = 'pythoncom.Missing'
        id = fdesc[0]
        s = linePrefix + 'def ' + name + '(self' + BuildCallList(fdesc, names, defNamedOptArg, defNamedNotOptArg, defUnnamedArg, defOutArg) + '):'
        ret.append(s)
        if doc and doc[1]:
            ret.append(linePrefix + '\t' + _makeDocString(doc[1]))
        resclsid = entry.GetResultCLSID()
        if resclsid:
            resclsid = "'%s'" % resclsid
        else:
            resclsid = 'None'
        retDesc = fdesc[8][:2]
        argsDesc = tuple((lambda .0: [ what[:2] for what in .0 ])(fdesc[2]))
        param_flags = (lambda .0: [ what[1] for what in .0 ])(fdesc[2])
        bad_params = (lambda .0: [ flag for flag in .0 if flag & (pythoncom.PARAMFLAG_FOUT | pythoncom.PARAMFLAG_FRETVAL) != 0 ])(param_flags)
        s = None
        if len(bad_params) == 0 and len(retDesc) == 2 and retDesc[1] == 0:
            rd = retDesc[0]
            if rd in NoTranslateMap:
                s = '%s\treturn self._oleobj_.InvokeTypes(%d, LCID, %s, %s, %s%s)' % (linePrefix, id, fdesc[4], retDesc, argsDesc, _BuildArgList(fdesc, names))
            elif rd in (pythoncom.VT_DISPATCH, pythoncom.VT_UNKNOWN):
                s = '%s\tret = self._oleobj_.InvokeTypes(%d, LCID, %s, %s, %s%s)\n' % (linePrefix, id, fdesc[4], retDesc, repr(argsDesc), _BuildArgList(fdesc, names))
                s = s + '%s\tif ret is not None:\n' % (linePrefix,)
                if rd == pythoncom.VT_UNKNOWN:
                    s = s + '%s\t\t# See if this IUnknown is really an IDispatch\n' % (linePrefix,)
                    s = s + '%s\t\ttry:\n' % (linePrefix,)
                    s = s + '%s\t\t\tret = ret.QueryInterface(pythoncom.IID_IDispatch)\n' % (linePrefix,)
                    s = s + '%s\t\texcept pythoncom.error:\n' % (linePrefix,)
                    s = s + '%s\t\t\treturn ret\n' % (linePrefix,)
                s = s + '%s\t\tret = Dispatch(ret, %s, %s)\n' % (linePrefix, repr(name), resclsid)
                s = s + '%s\treturn ret' % linePrefix
            elif rd == pythoncom.VT_BSTR:
                s = '%s\t# Result is a Unicode object\n' % (linePrefix,)
                s = s + '%s\treturn self._oleobj_.InvokeTypes(%d, LCID, %s, %s, %s%s)' % (linePrefix, id, fdesc[4], retDesc, repr(argsDesc), _BuildArgList(fdesc, names))
        if s is None:
            s = '%s\treturn self._ApplyTypes_(%d, %s, %s, %s, %s, %s%s)' % (linePrefix, id, fdesc[4], retDesc, argsDesc, repr(name), resclsid, _BuildArgList(fdesc, names))
        ret.append(s)
        ret.append('')
        return ret

    
    def MakeVarArgsFuncMethod(self, entry, name, bMakeClass = (1,)):
        fdesc = entry.desc
        names = entry.names
        doc = entry.doc
        ret = []
        argPrefix = 'self'
        if bMakeClass:
            linePrefix = '\t'
        else:
            linePrefix = ''
        ret.append(linePrefix + 'def ' + name + '(' + argPrefix + ', *args):')
        if doc and doc[1]:
            ret.append(linePrefix + '\t' + _makeDocString(doc[1]))
        if fdesc:
            invoketype = fdesc[4]
        else:
            invoketype = pythoncom.DISPATCH_METHOD
        s = linePrefix + '\treturn self._get_good_object_(self._oleobj_.Invoke(*(('
        ret.append(s + str(entry.dispid) + ",0,%d,1)+args)),'%s')" % (invoketype, names[0]))
        ret.append('')
        return ret



class VTableItem(DispatchItem):
    
    def Build(self, typeinfo, attr, bForUser = (1,)):
        DispatchItem.Build(self, typeinfo, attr, bForUser)
    # WARNING: Decompyle incomplete



class LazyDispatchItem(DispatchItem):
    typename = 'LazyDispatchItem'
    
    def __init__(self, attr, doc):
        self.clsid = attr[0]
        DispatchItem.__init__(self, None, attr, doc, 0)


typeSubstMap = {
    pythoncom.VT_HRESULT: pythoncom.VT_I4,
    pythoncom.VT_UINT: pythoncom.VT_UI4,
    pythoncom.VT_INT: pythoncom.VT_I4 }

def _ResolveType(typerepr, itypeinfo):
    pass
# WARNING: Decompyle incomplete


def _BuildArgList(fdesc, names):
    '''Builds list of args to the underlying Invoke method.'''
    numArgs = max(fdesc[6], len(fdesc[2]))
    names = list(names)
    if None in names:
        i = names.index(None)
        names[i] = 'arg%d' % (i,)
        if not None in names:
            names = list(map(MakePublicAttributeName, names[1:numArgs + 1]))
            name_num = 0
            if len(names) < numArgs:
                names.append('arg%d' % (len(names),))
                if not len(names) < numArgs:
                    for i in range(0, len(names), 5):
                        names[i] = names[i] + '\n\t\t\t'
                    return ',' + ', '.join(names)

valid_identifier_chars = string.ascii_letters + string.digits + '_'

def demunge_leading_underscores(className):
    i = 0
# WARNING: Decompyle incomplete


def MakePublicAttributeName(className, is_global = (False,)):
    if className[:2] == '__':
        return demunge_leading_underscores(className)
    if None == 'None':
        className = 'NONE'
    elif iskeyword(className):
        ret = className.capitalize()
        if ret == className:
            ret = ret.upper()
        return ret
    if is_global and hasattr(__builtins__, className):
        ret = className.capitalize()
        if ret == className:
            ret = ret.upper()
        return ret
    return None.join((lambda .0: [ char for char in .0 if char in valid_identifier_chars ])(className))


def MakeDefaultArgRepr(defArgVal):
    pass
# WARNING: Decompyle incomplete


def BuildCallList(fdesc, names, defNamedOptArg, defNamedNotOptArg, defUnnamedArg, defOutArg, is_comment = (False,)):
    '''Builds a Python declaration for a method.'''
    numArgs = len(fdesc[2])
    numOptArgs = fdesc[6]
    strval = ''
    if numOptArgs == -1:
        firstOptArg = numArgs
        numArgs = numArgs - 1
    else:
        firstOptArg = numArgs - numOptArgs
# WARNING: Decompyle incomplete

if __name__ == '__main__':
    print("Use 'makepy.py' to generate Python code - this module is just a helper")
    return None
