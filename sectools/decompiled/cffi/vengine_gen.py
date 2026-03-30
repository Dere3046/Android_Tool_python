
import sys
import os
import types
from  import model
from error import VerificationError

class VGenericEngine(object):
    _class_key = 'g'
    _gen_python_module = False
    
    def __init__(self, verifier):
        self.verifier = verifier
        self.ffi = verifier.ffi
        self.export_symbols = []
        self._struct_pending_verification = { }

    
    def patch_extension_kwds(self, kwds):
        kwds.setdefault('export_symbols', self.export_symbols)

    
    def find_module(self, module_name, path, so_suffixes):
        for so_suffix in so_suffixes:
            basename = module_name + so_suffix
            if path is None:
                path = sys.path
            for dirname in path:
                filename = os.path.join(dirname, basename)
                if os.path.isfile(filename):
                    return filename
                return None

    
    def collect_types(self):
        pass

    
    def _prnt(self, what = ('',)):
        self._f.write(what + '\n')

    
    def write_source_to_f(self):
        prnt = self._prnt
        prnt(cffimod_header)
        prnt(self.verifier.preamble)
        self._generate('decl')
        if sys.platform == 'win32':
            if sys.version_info >= (3,):
                prefix = 'PyInit_'
            else:
                prefix = 'init'
            modname = self.verifier.get_module_name()
            prnt('void %s%s(void) { }\n' % (prefix, modname))
            return None

    
    def load_library(self, flags = (0,)):
        backend = self.ffi._backend
        filename = os.path.join(os.curdir, self.verifier.modulefilename)
        module = backend.load_library(filename, flags)
        self._load(module, 'loading')
        
        def FFILibrary():
            '''VGenericEngine.load_library.<locals>.FFILibrary'''
            __module__ = __name__
            __qualname__ = 'VGenericEngine.load_library.<locals>.FFILibrary'
        # WARNING: Decompyle incomplete

        FFILibrary = None(FFILibrary, 'FFILibrary', types.ModuleType)
        library = FFILibrary('')
        self._load(module, 'loaded', library, **('library',))
        return library

    
    def _get_declarations(self):
        lst = (lambda .0: [ (key, tp) for tp, qual in .0 ])(self.ffi._parser._declarations.items())
        lst.sort()
        return lst

    
    def _generate(self, step_name):
        pass
    # WARNING: Decompyle incomplete

    
    def _load(self, module, step_name, **kwds):
        pass
    # WARNING: Decompyle incomplete

    
    def _generate_nothing(self, tp, name):
        pass

    
    def _loaded_noop(self, tp, name, module, **kwds):
        pass

    _generate_gen_typedef_decl = _generate_nothing
    _loading_gen_typedef = _loaded_noop
    _loaded_gen_typedef = _loaded_noop
    
    def _generate_gen_function_decl(self, tp, name):
        pass
    # WARNING: Decompyle incomplete

    _loading_gen_function = _loaded_noop
    
    def _loaded_gen_function(self, tp, name, module, library):
        pass
    # WARNING: Decompyle incomplete

    
    def _make_struct_wrapper(self, oldfunc, i, tp, base_tp):
        backend = self.ffi._backend
        BType = self.ffi._get_cached_btype(tp)
        if i == 'result':
            ffi = self.ffi
            
            def newfunc(*args):
                res = ffi.new(BType)
            # WARNING: Decompyle incomplete

        else:
            
            def newfunc(*args):
                args = args[:i] + (backend.newp(BType, args[i]),) + args[i + 1:]
            # WARNING: Decompyle incomplete

        newfunc._cffi_base_type = base_tp
        return newfunc

    
    def _generate_gen_struct_decl(self, tp, name):
        pass
    # WARNING: Decompyle incomplete

    
    def _loading_gen_struct(self, tp, name, module):
        self._loading_struct_or_union(tp, 'struct', name, module)

    
    def _loaded_gen_struct(self, tp, name, module, **kwds):
        self._loaded_struct_or_union(tp)

    
    def _generate_gen_union_decl(self, tp, name):
        pass
    # WARNING: Decompyle incomplete

    
    def _loading_gen_union(self, tp, name, module):
        self._loading_struct_or_union(tp, 'union', name, module)

    
    def _loaded_gen_union(self, tp, name, module, **kwds):
        self._loaded_struct_or_union(tp)

    
    def _generate_struct_or_union_decl(self, tp, prefix, name):
        if tp.fldnames is None:
            return None
        checkfuncname = None % (prefix, name)
        layoutfuncname = '_cffi_layout_%s_%s' % (prefix, name)
        cname = ('%s %s' % (prefix, name)).strip()
        prnt = self._prnt
        prnt('static void %s(%s *p)' % (checkfuncname, cname))
        prnt('{')
        prnt('  /* only to generate compile-time warnings or errors */')
        prnt('  (void)p;')
    # WARNING: Decompyle incomplete

    
    def _loading_struct_or_union(self, tp, prefix, name, module):
        if tp.fldnames is None:
            return None
        layoutfuncname = None % (prefix, name)
        BFunc = self.ffi._typeof_locked('intptr_t(*)(intptr_t)')[0]
        function = module.load_function(BFunc, layoutfuncname)
        layout = []
        num = 0
        x = function(num)
        if x < 0:
            pass
        else:
            layout.append(x)
            num += 1
    # WARNING: Decompyle incomplete

    
    def _loaded_struct_or_union(self, tp):
        if tp.fldnames is None:
            return None
        None.ffi._get_cached_btype(tp)
    # WARNING: Decompyle incomplete

    
    def _generate_gen_anonymous_decl(self, tp, name):
        if isinstance(tp, model.EnumType):
            self._generate_gen_enum_decl(tp, name, '')
            return None
        None._generate_struct_or_union_decl(tp, '', name)

    
    def _loading_gen_anonymous(self, tp, name, module):
        if isinstance(tp, model.EnumType):
            self._loading_gen_enum(tp, name, module, '')
            return None
        None._loading_struct_or_union(tp, '', name, module)

    
    def _loaded_gen_anonymous(self, tp, name, module, **kwds):
        pass
    # WARNING: Decompyle incomplete

    
    def _generate_gen_const(self, is_int, name, tp, category, check_value = (None, 'const', None)):
        prnt = self._prnt
        funcname = '_cffi_%s_%s' % (category, name)
        self.export_symbols.append(funcname)
    # WARNING: Decompyle incomplete

    
    def _generate_gen_constant_decl(self, tp, name):
        if isinstance(tp, model.PrimitiveType):
            pass
        is_int = tp.is_integer_type()
        self._generate_gen_const(is_int, name, tp)

    _loading_gen_constant = _loaded_noop
    
    def _load_constant(self, is_int, tp, name, module, check_value = (None,)):
        funcname = '_cffi_const_%s' % name
    # WARNING: Decompyle incomplete

    
    def _loaded_gen_constant(self, tp, name, module, library):
        if isinstance(tp, model.PrimitiveType):
            pass
        is_int = tp.is_integer_type()
        value = self._load_constant(is_int, tp, name, module)
        setattr(library, name, value)
        type(library)._cffi_dir.append(name)

    
    def _check_int_constant_value(self, name, value):
        prnt = self._prnt
        if value <= 0:
            prnt('  if ((%s) > 0 || (long)(%s) != %dL) {' % (name, name, value))
        else:
            prnt('  if ((%s) <= 0 || (unsigned long)(%s) != %dUL) {' % (name, name, value))
        prnt('    char buf[64];')
        prnt('    if ((%s) <= 0)' % name)
        prnt('        sprintf(buf, "%%ld", (long)(%s));' % name)
        prnt('    else')
        prnt('        sprintf(buf, "%%lu", (unsigned long)(%s));' % name)
        prnt('    sprintf(out_error, "%s has the real value %s, not %s",')
        prnt('            "%s", buf, "%d");' % (name[:100], value))
        prnt('    return -1;')
        prnt('  }')

    
    def _load_known_int_constant(self, module, funcname):
        BType = self.ffi._typeof_locked('char[]')[0]
        BFunc = self.ffi._typeof_locked('int(*)(char*)')[0]
        function = module.load_function(BFunc, funcname)
        p = self.ffi.new(BType, 256)
        if function(p) < 0:
            error = self.ffi.string(p)
            if sys.version_info >= (3,):
                error = str(error, 'utf-8')
            raise VerificationError(error)

    
    def _enum_funcname(self, prefix, name):
        name = name.replace('$', '___D_')
        return '_cffi_e_%s_%s' % (prefix, name)

    
    def _generate_gen_enum_decl(self, tp, name, prefix = ('enum',)):
        if tp.partial:
            for enumerator in tp.enumerators:
                self._generate_gen_const(True, enumerator)
            return None
        funcname = None._enum_funcname(prefix, name)
        self.export_symbols.append(funcname)
        prnt = self._prnt
        prnt('int %s(char *out_error)' % funcname)
        prnt('{')
        for enumerator, enumvalue in zip(tp.enumerators, tp.enumvalues):
            self._check_int_constant_value(enumerator, enumvalue)
        prnt('  return 0;')
        prnt('}')
        prnt()

    
    def _loading_gen_enum(self, tp, name, module, prefix = ('enum',)):
        if tp.partial:
            enumvalues = (lambda .0 = None: [ self._load_constant(True, tp, enumerator, module) for enumerator in .0 ])(tp.enumerators)
            tp.enumvalues = tuple(enumvalues)
            tp.partial_resolved = True
            return None
        funcname = None._enum_funcname(prefix, name)
        self._load_known_int_constant(module, funcname)

    
    def _loaded_gen_enum(self, tp, name, module, library):
        for enumerator, enumvalue in zip(tp.enumerators, tp.enumvalues):
            setattr(library, enumerator, enumvalue)
            type(library)._cffi_dir.append(enumerator)

    
    def _generate_gen_macro_decl(self, tp, name):
        if tp == '...':
            check_value = None
        else:
            check_value = tp
        self._generate_gen_const(True, name, check_value, **('check_value',))

    _loading_gen_macro = _loaded_noop
    
    def _loaded_gen_macro(self, tp, name, module, library):
        if tp == '...':
            check_value = None
        else:
            check_value = tp
        value = self._load_constant(True, tp, name, module, check_value, **('check_value',))
        setattr(library, name, value)
        type(library)._cffi_dir.append(name)

    
    def _generate_gen_variable_decl(self, tp, name):
        if isinstance(tp, model.ArrayType):
            if tp.length_is_unknown():
                prnt = self._prnt
                funcname = '_cffi_sizeof_%s' % (name,)
                self.export_symbols.append(funcname)
                prnt('size_t %s(void)' % funcname)
                prnt('{')
                prnt('  return sizeof(%s);' % (name,))
                prnt('}')
            tp_ptr = model.PointerType(tp.item)
            self._generate_gen_const(False, name, tp_ptr)
            return None
        tp_ptr = None.PointerType(tp)
        self._generate_gen_const(False, name, tp_ptr, 'var', **('category',))

    _loading_gen_variable = _loaded_noop
    
    def _loaded_gen_variable(self, tp, name, module, library):
        if isinstance(tp, model.ArrayType):
            if tp.length_is_unknown():
                funcname = '_cffi_sizeof_%s' % (name,)
                BFunc = self.ffi._typeof_locked('size_t(*)(void)')[0]
                function = module.load_function(BFunc, funcname)
                size = function()
                BItemType = self.ffi._get_cached_btype(tp.item)
                (length, rest) = divmod(size, self.ffi.sizeof(BItemType))
                if rest != 0:
                    raise VerificationError('bad size: %r does not seem to be an array of %s' % (name, tp.item))
                tp = None.resolve_length(length)
            tp_ptr = model.PointerType(tp.item)
            value = self._load_constant(False, tp_ptr, name, module)
            if tp.length is not None:
                BArray = self.ffi._get_cached_btype(tp)
                value = self.ffi.cast(BArray, value)
            setattr(library, name, value)
            type(library)._cffi_dir.append(name)
            return None
        funcname = None % name
        BFunc = self.ffi._typeof_locked(tp.get_c_name('*(*)(void)', name))[0]
        function = module.load_function(BFunc, funcname)
        ptr = function()
        
        def getter(library = None):
            return ptr[0]

        
        def setter(library = None, value = None):
            ptr[0] = value

        setattr(type(library), name, property(getter, setter))
        type(library)._cffi_dir.append(name)


cffimod_header = '\n#include <stdio.h>\n#include <stddef.h>\n#include <stdarg.h>\n#include <errno.h>\n#include <sys/types.h>   /* XXX for ssize_t on some platforms */\n\n/* this block of #ifs should be kept exactly identical between\n   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py\n   and cffi/_cffi_include.h */\n#if defined(_MSC_VER)\n# include <malloc.h>   /* for alloca() */\n# if _MSC_VER < 1600   /* MSVC < 2010 */\n   typedef __int8 int8_t;\n   typedef __int16 int16_t;\n   typedef __int32 int32_t;\n   typedef __int64 int64_t;\n   typedef unsigned __int8 uint8_t;\n   typedef unsigned __int16 uint16_t;\n   typedef unsigned __int32 uint32_t;\n   typedef unsigned __int64 uint64_t;\n   typedef __int8 int_least8_t;\n   typedef __int16 int_least16_t;\n   typedef __int32 int_least32_t;\n   typedef __int64 int_least64_t;\n   typedef unsigned __int8 uint_least8_t;\n   typedef unsigned __int16 uint_least16_t;\n   typedef unsigned __int32 uint_least32_t;\n   typedef unsigned __int64 uint_least64_t;\n   typedef __int8 int_fast8_t;\n   typedef __int16 int_fast16_t;\n   typedef __int32 int_fast32_t;\n   typedef __int64 int_fast64_t;\n   typedef unsigned __int8 uint_fast8_t;\n   typedef unsigned __int16 uint_fast16_t;\n   typedef unsigned __int32 uint_fast32_t;\n   typedef unsigned __int64 uint_fast64_t;\n   typedef __int64 intmax_t;\n   typedef unsigned __int64 uintmax_t;\n# else\n#  include <stdint.h>\n# endif\n# if _MSC_VER < 1800   /* MSVC < 2013 */\n#  ifndef __cplusplus\n    typedef unsigned char _Bool;\n#  endif\n# endif\n#else\n# include <stdint.h>\n# if (defined (__SVR4) && defined (__sun)) || defined(_AIX) || defined(__hpux)\n#  include <alloca.h>\n# endif\n#endif\n'
