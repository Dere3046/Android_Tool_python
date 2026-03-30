
import os
import sys
import io
from  import ffiplatform, model
from error import VerificationError
from cffi_opcode import *
VERSION_BASE = 9729
VERSION_EMBEDDED = 9985
VERSION_CHAR16CHAR32 = 10241
if not sys.platform != 'win32' and sys.version_info < (3, 0):
    pass
USE_LIMITED_API = sys.version_info >= (3, 5)

class GlobalExpr:
    
    def __init__(self, name, address, type_op, size, check_value = (0, 0)):
        self.name = name
        self.address = address
        self.type_op = type_op
        self.size = size
        self.check_value = check_value

    
    def as_c_expr(self):
        return '  { "%s", (void *)%s, %s, (void *)%s },' % (self.name, self.address, self.type_op.as_c_expr(), self.size)

    
    def as_python_expr(self):
        return "b'%s%s',%d" % (self.type_op.as_python_bytes(), self.name, self.check_value)



class FieldExpr:
    
    def __init__(self, name, field_offset, field_size, fbitsize, field_type_op):
        self.name = name
        self.field_offset = field_offset
        self.field_size = field_size
        self.fbitsize = fbitsize
        self.field_type_op = field_type_op

    
    def as_c_expr(self):
        spaces = ' ' * len(self.name)
        return '  { "%s", %s,\n' % (self.name, self.field_offset) + '     %s   %s,\n' % (spaces, self.field_size) + '     %s   %s },' % (spaces, self.field_type_op.as_c_expr())

    
    def as_python_expr(self):
        raise NotImplementedError

    
    def as_field_python_expr(self):
        if self.field_type_op.op == OP_NOOP:
            size_expr = ''
        elif self.field_type_op.op == OP_BITFIELD:
            size_expr = format_four_bytes(self.fbitsize)
        else:
            raise NotImplementedError
        return None % (self.field_type_op.as_python_bytes(), size_expr, self.name)



class StructUnionExpr:
    
    def __init__(self, name, type_index, flags, size, alignment, comment, first_field_index, c_fields):
        self.name = name
        self.type_index = type_index
        self.flags = flags
        self.size = size
        self.alignment = alignment
        self.comment = comment
        self.first_field_index = first_field_index
        self.c_fields = c_fields

    
    def as_c_expr(self):
        if self.comment:
            return '  { "%s", %d, %s,' % (self.name, self.type_index, self.flags) + '\n    %s, %s, ' % (self.size, self.alignment) + '%d, %d ' % (self.first_field_index, len(self.c_fields)) + '/* %s */ ' % self.comment + '},'
        return None + '  { "%s", %d, %s,' % (self.name, self.type_index, self.flags) + '\n    %s, %s, ' % (self.size, self.alignment) + '%d, %d ' % (self.first_field_index, len(self.c_fields)) + '},'

    
    def as_python_expr(self):
        flags = eval(self.flags, G_FLAGS)
        fields_expr = (lambda .0: [ c_field.as_field_python_expr() for c_field in .0 ])(self.c_fields)
        return "(b'%s%s%s',%s)" % (format_four_bytes(self.type_index), format_four_bytes(flags), self.name, ','.join(fields_expr))



class EnumExpr:
    
    def __init__(self, name, type_index, size, signed, allenums):
        self.name = name
        self.type_index = type_index
        self.size = size
        self.signed = signed
        self.allenums = allenums

    
    def as_c_expr(self):
        return '  { "%s", %d, _cffi_prim_int(%s, %s),\n    "%s" },' % (self.name, self.type_index, self.size, self.signed, self.allenums)

    
    def as_python_expr(self):
        prim_index = {
            (1, 0): PRIM_UINT8,
            (1, 1): PRIM_INT8,
            (2, 0): PRIM_UINT16,
            (2, 1): PRIM_INT16,
            (4, 0): PRIM_UINT32,
            (4, 1): PRIM_INT32,
            (8, 0): PRIM_UINT64,
            (8, 1): PRIM_INT64 }[(self.size, self.signed)]
        return "b'%s%s%s\\x00%s'" % (format_four_bytes(self.type_index), format_four_bytes(prim_index), self.name, self.allenums)



class TypenameExpr:
    
    def __init__(self, name, type_index):
        self.name = name
        self.type_index = type_index

    
    def as_c_expr(self):
        return '  { "%s", %d },' % (self.name, self.type_index)

    
    def as_python_expr(self):
        return "b'%s%s'" % (format_four_bytes(self.type_index), self.name)



class Recompiler:
    _num_externpy = 0
    
    def __init__(self, ffi, module_name, target_is_python = (False,)):
        self.ffi = ffi
        self.module_name = module_name
        self.target_is_python = target_is_python
        self._version = VERSION_BASE

    
    def needs_version(self, ver):
        self._version = max(self._version, ver)

    
    def collect_type_table(self):
        self._typesdict = { }
        self._generate('collecttype')
        all_decls = sorted(self._typesdict, str, **('key',))
        self.cffi_types = []
    # WARNING: Decompyle incomplete

    
    def _enum_fields(self, tp):
        expand_anonymous_struct_union = not (self.target_is_python)
        return tp.enumfields(expand_anonymous_struct_union)

    
    def _do_collect_type(self, tp):
        if not isinstance(tp, model.BaseTypeByIdentity):
            if isinstance(tp, tuple):
                for x in tp:
                    self._do_collect_type(x)
            return None
        if None not in self._typesdict:
            self._typesdict[tp] = None
            if isinstance(tp, model.FunctionPtrType):
                self._do_collect_type(tp.as_raw_function())
                return None
            if None(tp, model.StructOrUnion):
                if tp.fldtypes is not None or tp not in self.ffi._parser._included_declarations:
                    for name1, tp1, _, _ in self._enum_fields(tp):
                        self._do_collect_type(self._field_type(tp, name1, tp1))
                    return None
                return None
            return None
        for _, x in None._get_items():
            self._do_collect_type(x)
        return None

    
    def _generate(self, step_name):
        lst = self.ffi._parser._declarations.items()
    # WARNING: Decompyle incomplete

    ALL_STEPS = [
        'global',
        'field',
        'struct_union',
        'enum',
        'typename']
    
    def collect_step_tables(self):
        self._lsts = { }
        for step_name in self.ALL_STEPS:
            self._lsts[step_name] = []
        self._seen_struct_unions = set()
        self._generate('ctx')
        self._add_missing_struct_unions()
        for step_name in self.ALL_STEPS:
            lst = self._lsts[step_name]
            if step_name != 'field':
                lst.sort((lambda entry: entry.name), **('key',))
            self._lsts[step_name] = tuple(lst)
        lst = self._lsts['struct_union']
    # WARNING: Decompyle incomplete

    
    def _prnt(self, what = ('',)):
        self._f.write(what + '\n')

    
    def write_source_to_f(self, f, preamble):
        pass
    # WARNING: Decompyle incomplete

    
    def _rel_readlines(self, filename):
        g = open(os.path.join(os.path.dirname(__file__), filename), 'r')
        lines = g.readlines()
        g.close()
        return lines

    
    def write_c_source_to_f(self, f, preamble):
        self._f = f
        prnt = self._prnt
        if self.ffi._embedding is not None:
            prnt('#define _CFFI_USE_EMBEDDING')
        if not USE_LIMITED_API:
            prnt('#define _CFFI_NO_LIMITED_API')
        lines = self._rel_readlines('_cffi_include.h')
        i = lines.index('#include "parse_c_type.h"\n')
        lines[i:i + 1] = self._rel_readlines('parse_c_type.h')
        prnt(''.join(lines))
        base_module_name = self.module_name.split('.')[-1]
        if self.ffi._embedding is not None:
            prnt('#define _CFFI_MODULE_NAME  "%s"' % (self.module_name,))
            prnt('static const char _CFFI_PYTHON_STARTUP_CODE[] = {')
            self._print_string_literal_in_array(self.ffi._embedding)
            prnt('0 };')
            prnt('#ifdef PYPY_VERSION')
            prnt('# define _CFFI_PYTHON_STARTUP_FUNC  _cffi_pypyinit_%s' % (base_module_name,))
            prnt('#elif PY_MAJOR_VERSION >= 3')
            prnt('# define _CFFI_PYTHON_STARTUP_FUNC  PyInit_%s' % (base_module_name,))
            prnt('#else')
            prnt('# define _CFFI_PYTHON_STARTUP_FUNC  init%s' % (base_module_name,))
            prnt('#endif')
            lines = self._rel_readlines('_embedding.h')
            i = lines.index('#include "_cffi_errors.h"\n')
            lines[i:i + 1] = self._rel_readlines('_cffi_errors.h')
            prnt(''.join(lines))
            self.needs_version(VERSION_EMBEDDED)
        prnt('/************************************************************/')
        prnt()
        prnt(preamble)
        prnt()
        prnt('/************************************************************/')
        prnt()
        prnt('static void *_cffi_types[] = {')
        typeindex2type = dict((lambda .0: [ (i, tp) for tp, i in .0 ])(self._typesdict.items()))
        for i, op in enumerate(self.cffi_types):
            comment = ''
            if i in typeindex2type:
                comment = ' // ' + typeindex2type[i]._get_c_name()
            prnt('/* %2d */ %s,%s' % (i, op.as_c_expr(), comment))
        if not self.cffi_types:
            prnt('  0')
        prnt('};')
        prnt()
        self._seen_constants = set()
        self._generate('decl')
        nums = { }
        for step_name in self.ALL_STEPS:
            lst = self._lsts[step_name]
            nums[step_name] = len(lst)
            if nums[step_name] > 0:
                prnt('static const struct _cffi_%s_s _cffi_%ss[] = {' % (step_name, step_name))
                for entry in lst:
                    prnt(entry.as_c_expr())
                prnt('};')
                prnt()
    # WARNING: Decompyle incomplete

    
    def _to_py(self, x):
        if isinstance(x, str):
            return "b'%s'" % (x,)
        if None(x, (list, tuple)):
            rep = (lambda .0 = None: [ self._to_py(item) for item in .0 ])(x)
            if len(rep) == 1:
                rep.append('')
            return '(%s)' % (','.join(rep),)
        return None.as_python_expr()

    
    def write_py_source_to_f(self, f):
        self._f = f
        prnt = self._prnt
        prnt('# auto-generated file')
        prnt('import _cffi_backend')
        if not self.ffi._included_ffis:
            pass
        num_includes = len(())
    # WARNING: Decompyle incomplete

    
    def _gettypenum(self, type):
        return self._typesdict[type]

    
    def _convert_funcarg_to_c(self, tp, fromvar, tovar, errcode):
        extraarg = ''
        if not isinstance(tp, model.BasePrimitiveType) and tp.is_complex_type():
            if tp.is_integer_type() and tp.name != '_Bool':
                converter = '_cffi_to_c_int'
                extraarg = ', %s' % tp.name
            elif isinstance(tp, model.UnknownFloatType):
                converter = '(%s)_cffi_to_c_double' % (tp.get_c_name(''),)
            else:
                cname = tp.get_c_name('')
                converter = '(%s)_cffi_to_c_%s' % (cname, tp.name.replace(' ', '_'))
                if cname in ('char16_t', 'char32_t'):
                    self.needs_version(VERSION_CHAR16CHAR32)
            errvalue = '-1'
        elif isinstance(tp, model.PointerType):
            self._convert_funcarg_to_c_ptr_or_array(tp, fromvar, tovar, errcode)
            return None
        if isinstance(tp, model.StructOrUnionOrEnum) or isinstance(tp, model.BasePrimitiveType):
            self._prnt('  if (_cffi_to_c((char *)&%s, _cffi_type(%d), %s) < 0)' % (tovar, self._gettypenum(tp), fromvar))
            self._prnt('    %s;' % errcode)
            return None
        if None(tp, model.FunctionPtrType):
            converter = '(%s)_cffi_to_c_pointer' % tp.get_c_name('')
            extraarg = ', _cffi_type(%d)' % self._gettypenum(tp)
            errvalue = 'NULL'
        else:
            raise NotImplementedError(tp)
        None._prnt('  %s = %s(%s%s);' % (tovar, converter, fromvar, extraarg))
        self._prnt('  if (%s == (%s)%s && PyErr_Occurred())' % (tovar, tp.get_c_name(''), errvalue))
        self._prnt('    %s;' % errcode)

    
    def _extra_local_variables(self, tp, localvars, freelines):
        if isinstance(tp, model.PointerType):
            localvars.add('Py_ssize_t datasize')
            localvars.add('struct _cffi_freeme_s *large_args_free = NULL')
            freelines.add('if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);')
            return None

    
    def _convert_funcarg_to_c_ptr_or_array(self, tp, fromvar, tovar, errcode):
        self._prnt('  datasize = _cffi_prepare_pointer_call_argument(')
        self._prnt('      _cffi_type(%d), %s, (char **)&%s);' % (self._gettypenum(tp), fromvar, tovar))
        self._prnt('  if (datasize != 0) {')
        self._prnt('    %s = ((size_t)datasize) <= 640 ? (%s)alloca((size_t)datasize) : NULL;' % (tovar, tp.get_c_name('')))
        self._prnt('    if (_cffi_convert_array_argument(_cffi_type(%d), %s, (char **)&%s,' % (self._gettypenum(tp), fromvar, tovar))
        self._prnt('            datasize, &large_args_free) < 0)')
        self._prnt('      %s;' % errcode)
        self._prnt('  }')

    
    def _convert_expr_from_c(self, tp, var, context):
        if isinstance(tp, model.BasePrimitiveType):
            if tp.is_integer_type() and tp.name != '_Bool':
                return '_cffi_from_c_int(%s, %s)' % (var, tp.name)
            if None(tp, model.UnknownFloatType):
                return '_cffi_from_c_double(%s)' % (var,)
            if not None.name != 'long double' and tp.is_complex_type():
                cname = tp.name.replace(' ', '_')
                if cname in ('char16_t', 'char32_t'):
                    self.needs_version(VERSION_CHAR16CHAR32)
                return '_cffi_from_c_%s(%s)' % (cname, var)
            return None % (var, self._gettypenum(tp))
        if None(tp, (model.PointerType, model.FunctionPtrType)):
            return '_cffi_from_c_pointer((char *)%s, _cffi_type(%d))' % (var, self._gettypenum(tp))
        if None(tp, model.ArrayType):
            return '_cffi_from_c_pointer((char *)%s, _cffi_type(%d))' % (var, self._gettypenum(model.PointerType(tp.item)))
        if None(tp, model.StructOrUnion):
            if tp.fldnames is None:
                raise TypeError("'%s' is used as %s, but is opaque" % (tp._get_c_name(), context))
            return None % (var, self._gettypenum(tp))
        if None(tp, model.EnumType):
            return '_cffi_from_c_deref((char *)&%s, _cffi_type(%d))' % (var, self._gettypenum(tp))
        raise None(tp)

    
    def _typedef_type(self, tp, name):
        return self._global_type(tp, '(*(%s *)0)' % (name,))

    
    def _generate_cpy_typedef_collecttype(self, tp, name):
        self._do_collect_type(self._typedef_type(tp, name))

    
    def _generate_cpy_typedef_decl(self, tp, name):
        pass

    
    def _typedef_ctx(self, tp, name):
        type_index = self._typesdict[tp]
        self._lsts['typename'].append(TypenameExpr(name, type_index))

    
    def _generate_cpy_typedef_ctx(self, tp, name):
        tp = self._typedef_type(tp, name)
        self._typedef_ctx(tp, name)
        if getattr(tp, 'origin', None) == 'unknown_type':
            self._struct_ctx(tp, tp.name, None, **('approxname',))
            return None
        if None(tp, model.NamedPointerType):
            self._struct_ctx(tp.totype, tp.totype.name, tp.name, tp, **('approxname', 'named_ptr'))
            return None

    
    def _generate_cpy_function_collecttype(self, tp, name):
        self._do_collect_type(tp.as_raw_function())
        if not tp.ellipsis or self.target_is_python:
            self._do_collect_type(tp)
            return None
        return None

    
    def _generate_cpy_function_decl(self, tp, name):
        pass
    # WARNING: Decompyle incomplete

    
    def _generate_cpy_function_ctx(self, tp, name):
        if not tp.ellipsis and self.target_is_python:
            self._generate_cpy_constant_ctx(tp, name)
            return None
        type_index = None._typesdict[tp.as_raw_function()]
        numargs = len(tp.args)
        if self.target_is_python:
            meth_kind = OP_DLOPEN_FUNC
        elif numargs == 0:
            meth_kind = OP_CPYTHON_BLTN_N
        elif numargs == 1:
            meth_kind = OP_CPYTHON_BLTN_O
        else:
            meth_kind = OP_CPYTHON_BLTN_V
        self._lsts['global'].append(GlobalExpr(name, '_cffi_f_%s' % name, CffiOp(meth_kind, type_index), '_cffi_d_%s' % name, **('size',)))

    
    def _field_type(self, tp_struct, field_name, tp_field):
        if isinstance(tp_field, model.ArrayType):
            actual_length = tp_field.length
            if actual_length == '...':
                ptr_struct_name = tp_struct.get_c_name('*')
                actual_length = '_cffi_array_len(((%s)0)->%s)' % (ptr_struct_name, field_name)
            tp_item = self._field_type(tp_struct, '%s[0]' % field_name, tp_field.item)
            tp_field = model.ArrayType(tp_item, actual_length)
        return tp_field

    
    def _struct_collecttype(self, tp):
        self._do_collect_type(tp)
        if self.target_is_python:
            for fldtype in tp.anonymous_struct_fields():
                self._struct_collecttype(fldtype)
        return None

    
    def _struct_decl(self, tp, cname, approxname):
        if tp.fldtypes is None:
            return None
        prnt = None._prnt
        checkfuncname = '_cffi_checkfld_%s' % (approxname,)
        prnt('_CFFI_UNUSED_FN')
        prnt('static void %s(%s *p)' % (checkfuncname, cname))
        prnt('{')
        prnt('  /* only to generate compile-time warnings or errors */')
        prnt('  (void)p;')
    # WARNING: Decompyle incomplete

    
    def _struct_ctx(self, tp, cname, approxname, named_ptr = (None,)):
        type_index = self._typesdict[tp]
        reason_for_not_expanding = None
        flags = []
        if isinstance(tp, model.UnionType):
            flags.append('_CFFI_F_UNION')
        if tp.fldtypes is None:
            flags.append('_CFFI_F_OPAQUE')
            reason_for_not_expanding = 'opaque'
        if tp not in self.ffi._parser._included_declarations:
            if named_ptr is None or named_ptr not in self.ffi._parser._included_declarations:
                if tp.fldtypes is None:
                    pass
                elif tp.partial or any(tp.anonymous_struct_fields()):
                    pass
                else:
                    flags.append('_CFFI_F_CHECK_FIELDS')
                if tp.packed:
                    if tp.packed > 1:
                        raise NotImplementedError('%r is declared with \'pack=%r\'; only 0 or 1 are supported in API mode (try to use "...;", which does not require a \'pack\' declaration)' % (tp, tp.packed))
                    None.append('_CFFI_F_PACKED')
                else:
                    flags.append('_CFFI_F_EXTERNAL')
                    reason_for_not_expanding = 'external'
        if not '|'.join(flags):
            pass
        flags = '0'
        c_fields = []
        self._lsts['struct_union'].append(StructUnionExpr(tp.name, type_index, flags, size, align, comment, first_field_index, c_fields))
        self._seen_struct_unions.add(tp)

    
    def _check_not_opaque(self, tp, location):
        if isinstance(tp, model.ArrayType):
            tp = tp.item
            if isinstance(tp, model.ArrayType) or isinstance(tp, model.StructOrUnion) or tp.fldtypes is None:
                raise TypeError('%s is of an opaque type (not declared in cdef())' % location)
            return None

    
    def _add_missing_struct_unions(self):
        lst = list(self._struct_unions.items())
        lst.sort((lambda tp_order: tp_order[1]), **('key',))
        for tp, order in lst:
            if tp not in self._seen_struct_unions:
                if tp.partial:
                    raise NotImplementedError('internal inconsistency: %r is partial but was not seen at this point' % (tp,))
                if None.name.startswith('$') and tp.name[1:].isdigit():
                    approxname = tp.name[1:]
                elif tp.name == '_IO_FILE' and tp.forcename == 'FILE':
                    approxname = 'FILE'
                    self._typedef_ctx(tp, 'FILE')
                else:
                    raise NotImplementedError('internal inconsistency: %r' % (tp,))
                None._struct_ctx(tp, None, approxname)

    
    def _generate_cpy_struct_collecttype(self, tp, name):
        self._struct_collecttype(tp)

    _generate_cpy_union_collecttype = _generate_cpy_struct_collecttype
    
    def _struct_names(self, tp):
        cname = tp.get_c_name('')
        if ' ' in cname:
            return (cname, cname.replace(' ', '_'))
        return (None, '_' + cname)

    
    def _generate_cpy_struct_decl(self, tp, name):
        pass
    # WARNING: Decompyle incomplete

    _generate_cpy_union_decl = _generate_cpy_struct_decl
    
    def _generate_cpy_struct_ctx(self, tp, name):
        pass
    # WARNING: Decompyle incomplete

    _generate_cpy_union_ctx = _generate_cpy_struct_ctx
    
    def _generate_cpy_anonymous_collecttype(self, tp, name):
        if isinstance(tp, model.EnumType):
            self._generate_cpy_enum_collecttype(tp, name)
            return None
        None._struct_collecttype(tp)

    
    def _generate_cpy_anonymous_decl(self, tp, name):
        if isinstance(tp, model.EnumType):
            self._generate_cpy_enum_decl(tp)
            return None
        None._struct_decl(tp, name, 'typedef_' + name)

    
    def _generate_cpy_anonymous_ctx(self, tp, name):
        if isinstance(tp, model.EnumType):
            self._enum_ctx(tp, name)
            return None
        None._struct_ctx(tp, name, 'typedef_' + name)

    
    def _generate_cpy_const(self, is_int, name, tp, category, check_value = (None, 'const', None)):
        if (category, name) in self._seen_constants:
            raise VerificationError("duplicate declaration of %s '%s'" % (category, name))
        None._seen_constants.add((category, name))
        prnt = self._prnt
        funcname = '_cffi_%s_%s' % (category, name)
        if is_int:
            prnt('static int %s(unsigned long long *o)' % funcname)
            prnt('{')
            prnt('  int n = (%s) <= 0;' % (name,))
            prnt('  *o = (unsigned long long)((%s) | 0);  /* check that %s is an integer */' % (name, name))
            if check_value is not None:
                if check_value > 0:
                    check_value = '%dU' % (check_value,)
                prnt('  if (!_cffi_check_int(*o, n, %s))' % (check_value,))
                prnt('    n |= 2;')
            prnt('  return n;')
            prnt('}')
    # WARNING: Decompyle incomplete

    
    def _generate_cpy_constant_collecttype(self, tp, name):
        is_int = tp.is_integer_type()
        if is_int or self.target_is_python:
            self._do_collect_type(tp)
            return None

    
    def _generate_cpy_constant_decl(self, tp, name):
        is_int = tp.is_integer_type()
        self._generate_cpy_const(is_int, name, tp)

    
    def _generate_cpy_constant_ctx(self, tp, name):
        if self.target_is_python and tp.is_integer_type():
            type_op = CffiOp(OP_CONSTANT_INT, -1)
        elif self.target_is_python:
            const_kind = OP_DLOPEN_CONST
        else:
            const_kind = OP_CONSTANT
        type_index = self._typesdict[tp]
        type_op = CffiOp(const_kind, type_index)
        self._lsts['global'].append(GlobalExpr(name, '_cffi_const_%s' % name, type_op))

    
    def _generate_cpy_enum_collecttype(self, tp, name):
        self._do_collect_type(tp)

    
    def _generate_cpy_enum_decl(self, tp, name = (None,)):
        for enumerator in tp.enumerators:
            self._generate_cpy_const(True, enumerator)

    
    def _enum_ctx(self, tp, cname):
        type_index = self._typesdict[tp]
        type_op = CffiOp(OP_ENUM, -1)
        if self.target_is_python:
            tp.check_not_partial()
        for enumerator, enumvalue in zip(tp.enumerators, tp.enumvalues):
            self._lsts['global'].append(GlobalExpr(enumerator, '_cffi_const_%s' % enumerator, type_op, enumvalue, **('check_value',)))
        if not cname is not None and '$' not in cname and self.target_is_python:
            size = 'sizeof(%s)' % cname
            signed = '((%s)-1) <= 0' % cname
        else:
            basetp = tp.build_baseinttype(self.ffi, [])
            size = self.ffi.sizeof(basetp)
            signed = int(int(self.ffi.cast(basetp, -1)) < 0)
        allenums = ','.join(tp.enumerators)
        self._lsts['enum'].append(EnumExpr(tp.name, type_index, size, signed, allenums))

    
    def _generate_cpy_enum_ctx(self, tp, name):
        self._enum_ctx(tp, tp._get_c_name())

    
    def _generate_cpy_macro_collecttype(self, tp, name):
        pass

    
    def _generate_cpy_macro_decl(self, tp, name):
        if tp == '...':
            check_value = None
        else:
            check_value = tp
        self._generate_cpy_const(True, name, check_value, **('check_value',))

    
    def _generate_cpy_macro_ctx(self, tp, name):
        if tp == '...':
            if self.target_is_python:
                raise VerificationError("cannot use the syntax '...' in '#define %s ...' when using the ABI mode" % (name,))
            check_value = None
        else:
            check_value = tp
        type_op = CffiOp(OP_CONSTANT_INT, -1)
        self._lsts['global'].append(GlobalExpr(name, '_cffi_const_%s' % name, type_op, check_value, **('check_value',)))

    
    def _global_type(self, tp, global_name):
        if isinstance(tp, model.ArrayType):
            actual_length = tp.length
            if actual_length == '...':
                actual_length = '_cffi_array_len(%s)' % (global_name,)
            tp_item = self._global_type(tp.item, '%s[0]' % global_name)
            tp = model.ArrayType(tp_item, actual_length)
        return tp

    
    def _generate_cpy_variable_collecttype(self, tp, name):
        self._do_collect_type(self._global_type(tp, name))

    
    def _generate_cpy_variable_decl(self, tp, name):
        prnt = self._prnt
        tp = self._global_type(tp, name)
        if isinstance(tp, model.ArrayType) and tp.length is None:
            tp = tp.item
            ampersand = ''
        else:
            ampersand = '&'
        decl = '*_cffi_var_%s(void)' % (name,)
        prnt('static ' + tp.get_c_name(decl, self._current_quals, **('quals',)))
        prnt('{')
        prnt('  return %s(%s);' % (ampersand, name))
        prnt('}')
        prnt()

    
    def _generate_cpy_variable_ctx(self, tp, name):
        tp = self._global_type(tp, name)
        type_index = self._typesdict[tp]
        if self.target_is_python:
            op = OP_GLOBAL_VAR
        else:
            op = OP_GLOBAL_VAR_F
        self._lsts['global'].append(GlobalExpr(name, '_cffi_var_%s' % name, CffiOp(op, type_index)))

    
    def _generate_cpy_extern_python_collecttype(self, tp, name):
        pass
    # WARNING: Decompyle incomplete

    _generate_cpy_dllexport_python_collecttype = _generate_cpy_extern_python_plus_c_collecttype = _generate_cpy_extern_python_collecttype
    
    def _extern_python_decl(self, tp, name, tag_and_space):
        prnt = self._prnt
        if isinstance(tp.result, model.VoidType):
            size_of_result = '0'
        else:
            context = 'result of %s' % name
            size_of_result = '(int)sizeof(%s)' % (tp.result.get_c_name('', context),)
        prnt('static struct _cffi_externpy_s _cffi_externpy__%s =' % name)
        prnt('  { "%s.%s", %s, 0, 0 };' % (self.module_name, name, size_of_result))
        prnt()
        arguments = []
        context = 'argument of %s' % name
        for i, type in enumerate(tp.args):
            arg = type.get_c_name(' a%d' % i, context)
            arguments.append(arg)
        repr_arguments = ', '.join(arguments)
        if not repr_arguments:
            pass
        repr_arguments = 'void'
        name_and_arguments = '%s(%s)' % (name, repr_arguments)
        if tp.abi == '__stdcall':
            name_and_arguments = '_cffi_stdcall ' + name_and_arguments
        
        def may_need_128_bits(tp):
            if isinstance(tp, model.PrimitiveType):
                pass
            return tp.name == 'long double'

        size_of_a = max(len(tp.args) * 8, 8)
        if may_need_128_bits(tp.result):
            size_of_a = max(size_of_a, 16)
        if isinstance(tp.result, model.StructOrUnion):
            size_of_a = 'sizeof(%s) > %d ? sizeof(%s) : %d' % (tp.result.get_c_name(''), size_of_a, tp.result.get_c_name(''), size_of_a)
        prnt('%s%s' % (tag_and_space, tp.result.get_c_name(name_and_arguments)))
        prnt('{')
        prnt('  char a[%s];' % size_of_a)
        prnt('  char *p = a;')
        for i, type in enumerate(tp.args):
            arg = 'a%d' % i
            if isinstance(type, model.StructOrUnion) or may_need_128_bits(type):
                arg = '&' + arg
                type = model.PointerType(type)
            prnt('  *(%s)(p + %d) = %s;' % (type.get_c_name('*'), i * 8, arg))
        prnt('  _cffi_call_python(&_cffi_externpy__%s, p);' % name)
        if not isinstance(tp.result, model.VoidType):
            prnt('  return *(%s)p;' % (tp.result.get_c_name('*'),))
        prnt('}')
        prnt()
        self._num_externpy += 1

    
    def _generate_cpy_extern_python_decl(self, tp, name):
        self._extern_python_decl(tp, name, 'static ')

    
    def _generate_cpy_dllexport_python_decl(self, tp, name):
        self._extern_python_decl(tp, name, 'CFFI_DLLEXPORT ')

    
    def _generate_cpy_extern_python_plus_c_decl(self, tp, name):
        self._extern_python_decl(tp, name, '')

    
    def _generate_cpy_extern_python_ctx(self, tp, name):
        if self.target_is_python:
            raise VerificationError('cannot use \'extern "Python"\' in the ABI mode')
        if None.ellipsis:
            raise NotImplementedError('a vararg function is extern "Python"')
        type_index = None._typesdict[tp]
        type_op = CffiOp(OP_EXTERN_PYTHON, type_index)
        self._lsts['global'].append(GlobalExpr(name, '&_cffi_externpy__%s' % name, type_op, name))

    _generate_cpy_dllexport_python_ctx = _generate_cpy_extern_python_plus_c_ctx = _generate_cpy_extern_python_ctx
    
    def _print_string_literal_in_array(self, s):
        prnt = self._prnt
        prnt('// # NB. this is not a string because of a size limit in MSVC')
        if not isinstance(s, bytes):
            s = s.encode('utf-8')
        else:
            s.decode('utf-8')
    # WARNING: Decompyle incomplete

    
    def _emit_bytecode_VoidType(self, tp, index):
        self.cffi_types[index] = CffiOp(OP_PRIMITIVE, PRIM_VOID)

    
    def _emit_bytecode_PrimitiveType(self, tp, index):
        prim_index = PRIMITIVE_TO_INDEX[tp.name]
        self.cffi_types[index] = CffiOp(OP_PRIMITIVE, prim_index)

    
    def _emit_bytecode_UnknownIntegerType(self, tp, index):
        s = '_cffi_prim_int(sizeof(%s), (\n           ((%s)-1) | 0 /* check that %s is an integer type */\n         ) <= 0)' % (tp.name, tp.name, tp.name)
        self.cffi_types[index] = CffiOp(OP_PRIMITIVE, s)

    
    def _emit_bytecode_UnknownFloatType(self, tp, index):
        s = '_cffi_prim_float(sizeof(%s) *\n           (((%s)1) / 2) * 2 /* integer => 0, float => 1 */\n         )' % (tp.name, tp.name)
        self.cffi_types[index] = CffiOp(OP_PRIMITIVE, s)

    
    def _emit_bytecode_RawFunctionType(self, tp, index):
        self.cffi_types[index] = CffiOp(OP_FUNCTION, self._typesdict[tp.result])
        index += 1
        for tp1 in tp.args:
            realindex = self._typesdict[tp1]
            if index != realindex:
                if isinstance(tp1, model.PrimitiveType):
                    self._emit_bytecode_PrimitiveType(tp1, index)
                else:
                    self.cffi_types[index] = CffiOp(OP_NOOP, realindex)
            index += 1
        flags = int(tp.ellipsis)
        if tp.abi is not None:
            if tp.abi == '__stdcall':
                flags |= 2
            else:
                raise NotImplementedError('abi=%r' % (tp.abi,))
            self.cffi_types[index] = None(OP_FUNCTION_END, flags)
            return None

    
    def _emit_bytecode_PointerType(self, tp, index):
        self.cffi_types[index] = CffiOp(OP_POINTER, self._typesdict[tp.totype])

    _emit_bytecode_ConstPointerType = _emit_bytecode_PointerType
    _emit_bytecode_NamedPointerType = _emit_bytecode_PointerType
    
    def _emit_bytecode_FunctionPtrType(self, tp, index):
        raw = tp.as_raw_function()
        self.cffi_types[index] = CffiOp(OP_POINTER, self._typesdict[raw])

    
    def _emit_bytecode_ArrayType(self, tp, index):
        item_index = self._typesdict[tp.item]
        if tp.length is None:
            self.cffi_types[index] = CffiOp(OP_OPEN_ARRAY, item_index)
            return None
        if None.length == '...':
            raise VerificationError("type %s badly placed: the '...' array length can only be used on global arrays or on fields of structures" % (str(tp).replace('/*...*/', '...'),))
    # WARNING: Decompyle incomplete

    
    def _emit_bytecode_StructType(self, tp, index):
        struct_index = self._struct_unions[tp]
        self.cffi_types[index] = CffiOp(OP_STRUCT_UNION, struct_index)

    _emit_bytecode_UnionType = _emit_bytecode_StructType
    
    def _emit_bytecode_EnumType(self, tp, index):
        enum_index = self._enums[tp]
        self.cffi_types[index] = CffiOp(OP_ENUM, enum_index)


if sys.version_info >= (3,):
    NativeIO = io.StringIO
else:
    
    class NativeIO(io.BytesIO):
        
        def write(self = None, s = None):
            if isinstance(s, unicode):
                s = s.encode('ascii')
            super(NativeIO, self).write(s)

        __classcell__ = None


def _make_c_or_py_source(ffi, module_name, preamble, target_file, verbose):
    if verbose:
        print('generating %s' % (target_file,))
    recompiler = Recompiler(ffi, module_name, preamble is None, **('target_is_python',))
    recompiler.collect_type_table()
    recompiler.collect_step_tables()
    f = NativeIO()
    recompiler.write_source_to_f(f, preamble)
    output = f.getvalue()
# WARNING: Decompyle incomplete


def make_c_source(ffi, module_name, preamble, target_c_file, verbose = (False,)):
    pass
# WARNING: Decompyle incomplete


def make_py_source(ffi, module_name, target_py_file, verbose = (False,)):
    return _make_c_or_py_source(ffi, module_name, None, target_py_file, verbose)


def _modname_to_file(outputdir, modname, extension):
    parts = modname.split('.')
# WARNING: Decompyle incomplete


def _patch_meth(patchlist, cls, name, new_meth):
    old = getattr(cls, name)
    patchlist.append((cls, name, old))
    setattr(cls, name, new_meth)
    return old


def _unpatch_meths(patchlist):
    for cls, name, old_meth in reversed(patchlist):
        setattr(cls, name, old_meth)


def _patch_for_embedding(patchlist):
    if sys.platform == 'win32':
        MSVCCompiler = MSVCCompiler
        import distutils.msvc9compiler
        _patch_meth(patchlist, MSVCCompiler, '_remove_visual_c_ref', (lambda self, manifest_file: manifest_file))
    if sys.platform == 'darwin':
        CCompiler = CCompiler
        import distutils.ccompiler
        
        def my_link_shared_object(self = None, *args, **kwds):
            if '-bundle' in self.linker_so:
                self.linker_so = list(self.linker_so)
                i = self.linker_so.index('-bundle')
                self.linker_so[i] = '-dynamiclib'
        # WARNING: Decompyle incomplete

        old_link_shared_object = _patch_meth(patchlist, CCompiler, 'link_shared_object', my_link_shared_object)
        return None


def _patch_for_target(patchlist, target):
    build_ext = build_ext
    import distutils.command.build_ext
    if target.endswith('.*'):
        target = target[:-2]
        if sys.platform == 'win32':
            target += '.dll'
        elif sys.platform == 'darwin':
            target += '.dylib'
        else:
            target += '.so'
    None(None, None, None, (lambda self = None, ext_name = None: target))


def recompile(ffi, module_name, preamble, tmpdir, call_c_compiler, c_file, source_extension, extradir, compiler_verbose, target, debug = ('.', True, None, '.c', None, 1, None, None), **kwds):
    if not isinstance(module_name, str):
        module_name = module_name.encode('ascii')
    if ffi._windows_unicode:
        ffi._apply_windows_unicode(kwds)
# WARNING: Decompyle incomplete

