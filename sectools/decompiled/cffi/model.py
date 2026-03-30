
import types
import weakref
from lock import allocate_lock
from error import CDefError, VerificationError, VerificationMissing
Q_CONST = 1
Q_RESTRICT = 2
Q_VOLATILE = 4

def qualify(quals, replace_with):
    if quals & Q_CONST:
        replace_with = ' const ' + replace_with.lstrip()
    if quals & Q_VOLATILE:
        replace_with = ' volatile ' + replace_with.lstrip()
    if quals & Q_RESTRICT:
        replace_with = ' __restrict ' + replace_with.lstrip()
    return replace_with


class BaseTypeByIdentity(object):
    is_array_type = False
    is_raw_function = False
    
    def get_c_name(self, replace_with, context, quals = ('', 'a C file', 0)):
        result = self.c_name_with_marker
    # WARNING: Decompyle incomplete

    
    def _get_c_name(self):
        return self.c_name_with_marker.replace('&', '')

    
    def has_c_name(self):
        return '$' not in self._get_c_name()

    
    def is_integer_type(self):
        return False

    
    def get_cached_btype(self, ffi, finishlist, can_delay = (False,)):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self):
        return '<%s>' % (self._get_c_name(),)

    
    def _get_items(self):
        return (lambda .0 = None: [ (name, getattr(self, name)) for name in .0 ])(self._attrs_)



class BaseType(BaseTypeByIdentity):
    
    def __eq__(self, other):
        if self.__class__ == other.__class__:
            pass
        return self._get_items() == other._get_items()

    
    def __ne__(self, other):
        return not (self == other)

    
    def __hash__(self):
        return hash((self.__class__, tuple(self._get_items())))



class VoidType(BaseType):
    _attrs_ = ()
    
    def __init__(self):
        self.c_name_with_marker = 'void&'

    
    def build_backend_type(self, ffi, finishlist):
        return global_cache(self, ffi, 'new_void_type')


void_type = VoidType()

class BasePrimitiveType(BaseType):
    
    def is_complex_type(self):
        return False



class PrimitiveType(BasePrimitiveType):
    __module__ = __name__
    __qualname__ = 'PrimitiveType'
    _attrs_ = ('name',)
# WARNING: Decompyle incomplete


class UnknownIntegerType(BasePrimitiveType):
    _attrs_ = ('name',)
    
    def __init__(self, name):
        self.name = name
        self.c_name_with_marker = name + '&'

    
    def is_integer_type(self):
        return True

    
    def build_backend_type(self, ffi, finishlist):
        raise NotImplementedError("integer type '%s' can only be used after compilation" % self.name)



class UnknownFloatType(BasePrimitiveType):
    _attrs_ = ('name',)
    
    def __init__(self, name):
        self.name = name
        self.c_name_with_marker = name + '&'

    
    def build_backend_type(self, ffi, finishlist):
        raise NotImplementedError("float type '%s' can only be used after compilation" % self.name)



class BaseFunctionType(BaseType):
    _attrs_ = ('args', 'result', 'ellipsis', 'abi')
    
    def __init__(self, args, result, ellipsis, abi = (None,)):
        self.args = args
        self.result = result
        self.ellipsis = ellipsis
        self.abi = abi
        reprargs = (lambda .0: [ arg._get_c_name() for arg in .0 ])(self.args)
        if self.ellipsis:
            reprargs.append('...')
        if not reprargs:
            pass
        reprargs = [
            'void']
        replace_with = self._base_pattern % (', '.join(reprargs),)
        if abi is not None:
            replace_with = replace_with[:1] + abi + ' ' + replace_with[1:]
        self.c_name_with_marker = self.result.c_name_with_marker.replace('&', replace_with)



class RawFunctionType(BaseFunctionType):
    _base_pattern = '(&)(%s)'
    is_raw_function = True
    
    def build_backend_type(self, ffi, finishlist):
        raise CDefError('cannot render the type %r: it is a function type, not a pointer-to-function type' % (self,))

    
    def as_function_pointer(self):
        return FunctionPtrType(self.args, self.result, self.ellipsis, self.abi)



class FunctionPtrType(BaseFunctionType):
    _base_pattern = '(*&)(%s)'
    
    def build_backend_type(self, ffi, finishlist):
        result = self.result.get_cached_btype(ffi, finishlist)
        args = []
        for tp in self.args:
            args.append(tp.get_cached_btype(ffi, finishlist))
        abi_args = ()
    # WARNING: Decompyle incomplete

    
    def as_raw_function(self):
        return RawFunctionType(self.args, self.result, self.ellipsis, self.abi)



class PointerType(BaseType):
    _attrs_ = ('totype', 'quals')
    
    def __init__(self, totype, quals = (0,)):
        self.totype = totype
        self.quals = quals
        extra = qualify(quals, ' *&')
        if totype.is_array_type:
            extra = '(%s)' % (extra.lstrip(),)
        self.c_name_with_marker = totype.c_name_with_marker.replace('&', extra)

    
    def build_backend_type(self, ffi, finishlist):
        BItem = self.totype.get_cached_btype(ffi, finishlist, True, **('can_delay',))
        return global_cache(self, ffi, 'new_pointer_type', BItem)


voidp_type = PointerType(void_type)

def ConstPointerType(totype):
    return PointerType(totype, Q_CONST)

const_voidp_type = ConstPointerType(void_type)

class NamedPointerType(PointerType):
    _attrs_ = ('totype', 'name')
    
    def __init__(self, totype, name, quals = (0,)):
        PointerType.__init__(self, totype, quals)
        self.name = name
        self.c_name_with_marker = name + '&'



class ArrayType(BaseType):
    _attrs_ = ('item', 'length')
    is_array_type = True
    
    def __init__(self, item, length):
        self.item = item
        self.length = length
        if length is None:
            brackets = '&[]'
        elif length == '...':
            brackets = '&[/*...*/]'
        else:
            brackets = '&[%s]' % length
        self.c_name_with_marker = self.item.c_name_with_marker.replace('&', brackets)

    
    def length_is_unknown(self):
        return isinstance(self.length, str)

    
    def resolve_length(self, newlength):
        return ArrayType(self.item, newlength)

    
    def build_backend_type(self, ffi, finishlist):
        if self.length_is_unknown():
            raise CDefError('cannot render the type %r: unknown length' % (self,))
        None.item.get_cached_btype(ffi, finishlist)
        BPtrItem = PointerType(self.item).get_cached_btype(ffi, finishlist)
        return global_cache(self, ffi, 'new_array_type', BPtrItem, self.length)


char_array_type = ArrayType(PrimitiveType('char'), None)

class StructOrUnionOrEnum(BaseTypeByIdentity):
    _attrs_ = ('name',)
    forcename = None
    
    def build_c_name_with_marker(self):
        if not self.forcename:
            pass
        name = '%s %s' % (self.kind, self.name)
        self.c_name_with_marker = name + '&'

    
    def force_the_name(self, forcename):
        self.forcename = forcename
        self.build_c_name_with_marker()

    
    def get_official_name(self):
        pass
    # WARNING: Decompyle incomplete



class StructOrUnion(StructOrUnionOrEnum):
    fixedlayout = None
    completed = 0
    partial = False
    packed = 0
    
    def __init__(self, name, fldnames, fldtypes, fldbitsize, fldquals = (None,)):
        self.name = name
        self.fldnames = fldnames
        self.fldtypes = fldtypes
        self.fldbitsize = fldbitsize
        self.fldquals = fldquals
        self.build_c_name_with_marker()

    
    def anonymous_struct_fields(self):
        if self.fldtypes is not None:
            for name, type in zip(self.fldnames, self.fldtypes):
                if name == '' and isinstance(type, StructOrUnion):
                    yield type
        return None

    
    def enumfields(self, expand_anonymous_struct_union = (True,)):
        fldquals = self.fldquals
        if fldquals is None:
            fldquals = (0,) * len(self.fldnames)
        for name, type, bitsize, quals in zip(self.fldnames, self.fldtypes, self.fldbitsize, fldquals):
            if name == '' and isinstance(type, StructOrUnion) and expand_anonymous_struct_union:
                for result in type.enumfields():
                    yield result
            yield (name, type, bitsize, quals)

    
    def force_flatten(self):
        names = []
        types = []
        bitsizes = []
        fldquals = []
        for name, type, bitsize, quals in self.enumfields():
            names.append(name)
            types.append(type)
            bitsizes.append(bitsize)
            fldquals.append(quals)
        self.fldnames = tuple(names)
        self.fldtypes = tuple(types)
        self.fldbitsize = tuple(bitsizes)
        self.fldquals = tuple(fldquals)

    
    def get_cached_btype(self, ffi, finishlist, can_delay = (False,)):
        BType = StructOrUnionOrEnum.get_cached_btype(self, ffi, finishlist, can_delay)
        if not can_delay:
            self.finish_backend_type(ffi, finishlist)
        return BType

    
    def finish_backend_type(self, ffi, finishlist):
        if self.completed:
            if self.completed != 2:
                raise NotImplementedError("recursive structure declaration for '%s'" % (self.name,))
            return None
        BType = None._cached_btypes[self]
        self.completed = 1
        if self.fldtypes is None:
            pass
    # WARNING: Decompyle incomplete

    
    def _verification_error(self, msg):
        raise VerificationError(msg)

    
    def check_not_partial(self):
        if self.partial or self.fixedlayout is None:
            raise VerificationMissing(self._get_c_name())
        return None

    
    def build_backend_type(self, ffi, finishlist):
        self.check_not_partial()
        finishlist.append(self)
        return global_cache(self, ffi, 'new_%s_type' % self.kind, self.get_official_name(), self, **('key',))



class StructType(StructOrUnion):
    kind = 'struct'


class UnionType(StructOrUnion):
    kind = 'union'


class EnumType(StructOrUnionOrEnum):
    kind = 'enum'
    partial = False
    partial_resolved = False
    
    def __init__(self, name, enumerators, enumvalues, baseinttype = (None,)):
        self.name = name
        self.enumerators = enumerators
        self.enumvalues = enumvalues
        self.baseinttype = baseinttype
        self.build_c_name_with_marker()

    
    def force_the_name(self, forcename):
        StructOrUnionOrEnum.force_the_name(self, forcename)
        if self.forcename is None:
            name = self.get_official_name()
            self.forcename = '$' + name.replace(' ', '_')
            return None

    
    def check_not_partial(self):
        if not self.partial or self.partial_resolved:
            raise VerificationMissing(self._get_c_name())
        return None

    
    def build_backend_type(self, ffi, finishlist):
        self.check_not_partial()
        base_btype = self.build_baseinttype(ffi, finishlist)
        return global_cache(self, ffi, 'new_enum_type', self.get_official_name(), self.enumerators, self.enumvalues, base_btype, self, **('key',))

    
    def build_baseinttype(self, ffi, finishlist):
        if self.baseinttype is not None:
            return self.baseinttype.get_cached_btype(ffi, finishlist)
        if None.enumvalues:
            smallest_value = min(self.enumvalues)
            largest_value = max(self.enumvalues)
    # WARNING: Decompyle incomplete



def unknown_type(name, structname = (None,)):
    if structname is None:
        structname = '$%s' % name
    tp = StructType(structname, None, None, None)
    tp.force_the_name(name)
    tp.origin = 'unknown_type'
    return tp


def unknown_ptr_type(name, structname = (None,)):
    if structname is None:
        structname = '$$%s' % name
    tp = StructType(structname, None, None, None)
    return NamedPointerType(tp, name)

global_lock = allocate_lock()
_typecache_cffi_backend = weakref.WeakValueDictionary()

def get_typecache(backend):
    if isinstance(backend, types.ModuleType):
        return _typecache_cffi_backend
    with None:
        if not hasattr(type(backend), '__typecache'):
            type(backend).__typecache = weakref.WeakValueDictionary()
    :
        if isinstance(backend, types.ModuleType):
            return _typecache_cffi_backend
        with None:
            if not hasattr(type(backend), '__typecache'):
                type(backend).__typecache = weakref.WeakValueDictionary()
        :
            if isinstance(backend, types.ModuleType):
                return _typecache_cffi_backend
            with None:
                if not hasattr(type(backend), '__typecache'):
                    type(backend).__typecache = weakref.WeakValueDictionary()
            :
                if isinstance(backend, types.ModuleType):
                    return _typecache_cffi_backend
                with None:
                    if not hasattr(type(backend), '__typecache'):
                        type(backend).__typecache = weakref.WeakValueDictionary()
                :
                    if isinstance(backend, types.ModuleType):
                        return _typecache_cffi_backend
                    with None:
                        if not hasattr(type(backend), '__typecache'):
                            type(backend).__typecache = weakref.WeakValueDictionary()
                    :
                        if isinstance(backend, types.ModuleType):
                            return _typecache_cffi_backend
                        with None:
                            if not hasattr(type(backend), '__typecache'):
                                type(backend).__typecache = weakref.WeakValueDictionary()
                        :
                            if isinstance(backend, types.ModuleType):
                                return _typecache_cffi_backend
                            with None:
                                if not hasattr(type(backend), '__typecache'):
                                    type(backend).__typecache = weakref.WeakValueDictionary()
                            :
                                if isinstance(backend, types.ModuleType):
                                    return _typecache_cffi_backend
                                with None:
                                    if not hasattr(type(backend), '__typecache'):
                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                :
                                    if isinstance(backend, types.ModuleType):
                                        return _typecache_cffi_backend
                                    with None:
                                        if not hasattr(type(backend), '__typecache'):
                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                    :
                                        if isinstance(backend, types.ModuleType):
                                            return _typecache_cffi_backend
                                        with None:
                                            if not hasattr(type(backend), '__typecache'):
                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                        :
                                            if isinstance(backend, types.ModuleType):
                                                return _typecache_cffi_backend
                                            with None:
                                                if not hasattr(type(backend), '__typecache'):
                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                            :
                                                if isinstance(backend, types.ModuleType):
                                                    return _typecache_cffi_backend
                                                with None:
                                                    if not hasattr(type(backend), '__typecache'):
                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                :
                                                    if isinstance(backend, types.ModuleType):
                                                        return _typecache_cffi_backend
                                                    with None:
                                                        if not hasattr(type(backend), '__typecache'):
                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                    :
                                                        if isinstance(backend, types.ModuleType):
                                                            return _typecache_cffi_backend
                                                        with None:
                                                            if not hasattr(type(backend), '__typecache'):
                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                        :
                                                            if isinstance(backend, types.ModuleType):
                                                                return _typecache_cffi_backend
                                                            with None:
                                                                if not hasattr(type(backend), '__typecache'):
                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                            :
                                                                if isinstance(backend, types.ModuleType):
                                                                    return _typecache_cffi_backend
                                                                with None:
                                                                    if not hasattr(type(backend), '__typecache'):
                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                :
                                                                    if isinstance(backend, types.ModuleType):
                                                                        return _typecache_cffi_backend
                                                                    with None:
                                                                        if not hasattr(type(backend), '__typecache'):
                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                    :
                                                                        if isinstance(backend, types.ModuleType):
                                                                            return _typecache_cffi_backend
                                                                        with None:
                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                        :
                                                                            if isinstance(backend, types.ModuleType):
                                                                                return _typecache_cffi_backend
                                                                            with None:
                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                            :
                                                                                if isinstance(backend, types.ModuleType):
                                                                                    return _typecache_cffi_backend
                                                                                with None:
                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                :
                                                                                    if isinstance(backend, types.ModuleType):
                                                                                        return _typecache_cffi_backend
                                                                                    with None:
                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                    :
                                                                                        if isinstance(backend, types.ModuleType):
                                                                                            return _typecache_cffi_backend
                                                                                        with None:
                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                        :
                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                return _typecache_cffi_backend
                                                                                            with None:
                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                            :
                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                    return _typecache_cffi_backend
                                                                                                with None:
                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                :
                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                        return _typecache_cffi_backend
                                                                                                    with None:
                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                    :
                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                            return _typecache_cffi_backend
                                                                                                        with None:
                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                        :
                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                return _typecache_cffi_backend
                                                                                                            with None:
                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                            :
                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                    return _typecache_cffi_backend
                                                                                                                with None:
                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                :
                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                        return _typecache_cffi_backend
                                                                                                                    with None:
                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                    :
                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                            return _typecache_cffi_backend
                                                                                                                        with None:
                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                        :
                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                return _typecache_cffi_backend
                                                                                                                            with None:
                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                            :
                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                with None:
                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                :
                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                    with None:
                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                    :
                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                        with None:
                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                        :
                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                            with None:
                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                            :
                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                with None:
                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                :
                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                    with None:
                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                    :
                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                        with None:
                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                        :
                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                            with None:
                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                            :
                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                with None:
                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                :
                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                    with None:
                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                    :
                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                        with None:
                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                        :
                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                            with None:
                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                            :
                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                with None:
                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                :
                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                    with None:
                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                    :
                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                        with None:
                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                        :
                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                            with None:
                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                            :
                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                with None:
                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                :
                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                    with None:
                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                    :
                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                        with None:
                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                        :
                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                            :
                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                :
                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                    :
                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                        :
                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                                                    with None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                        if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                                                            type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                                                        if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                                                            return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                                                        with None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                            if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                                                            if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                                                            with None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                                                if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                                                                with None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if not hasattr(type(backend), '__typecache'):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        type(backend).__typecache = weakref.WeakValueDictionary()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if isinstance(backend, types.ModuleType):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        return _typecache_cffi_backend
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    with Non