
from error import VerificationError

class CffiOp(object):
    
    def __init__(self, op, arg):
        self.op = op
        self.arg = arg

    
    def as_c_expr(self):
        pass
    # WARNING: Decompyle incomplete

    
    def as_python_bytes(self):
        if self.op is None and self.arg.isdigit():
            value = int(self.arg)
            if value >= 0x80000000L:
                raise OverflowError('cannot emit %r: limited to 2**31-1' % (self.arg,))
            return None(value)
        if None(self.arg, str):
            raise VerificationError('cannot emit to Python: %r' % (self.arg,))
        return None(self.arg << 8 | self.op)

    
    def __str__(self):
        classname = CLASS_NAME.get(self.op, self.op)
        return '(%s %s)' % (classname, self.arg)



def format_four_bytes(num):
    return '\\x%02X\\x%02X\\x%02X\\x%02X' % (num >> 24 & 255, num >> 16 & 255, num >> 8 & 255, num & 255)

OP_PRIMITIVE = 1
OP_POINTER = 3
OP_ARRAY = 5
OP_OPEN_ARRAY = 7
OP_STRUCT_UNION = 9
OP_ENUM = 11
OP_FUNCTION = 13
OP_FUNCTION_END = 15
OP_NOOP = 17
OP_BITFIELD = 19
OP_TYPENAME = 21
OP_CPYTHON_BLTN_V = 23
OP_CPYTHON_BLTN_N = 25
OP_CPYTHON_BLTN_O = 27
OP_CONSTANT = 29
OP_CONSTANT_INT = 31
OP_GLOBAL_VAR = 33
OP_DLOPEN_FUNC = 35
OP_DLOPEN_CONST = 37
OP_GLOBAL_VAR_F = 39
OP_EXTERN_PYTHON = 41
PRIM_VOID = 0
PRIM_BOOL = 1
PRIM_CHAR = 2
PRIM_SCHAR = 3
PRIM_UCHAR = 4
PRIM_SHORT = 5
PRIM_USHORT = 6
PRIM_INT = 7
PRIM_UINT = 8
PRIM_LONG = 9
PRIM_ULONG = 10
PRIM_LONGLONG = 11
PRIM_ULONGLONG = 12
PRIM_FLOAT = 13
PRIM_DOUBLE = 14
PRIM_LONGDOUBLE = 15
PRIM_WCHAR = 16
PRIM_INT8 = 17
PRIM_UINT8 = 18
PRIM_INT16 = 19
PRIM_UINT16 = 20
PRIM_INT32 = 21
PRIM_UINT32 = 22
PRIM_INT64 = 23
PRIM_UINT64 = 24
PRIM_INTPTR = 25
PRIM_UINTPTR = 26
PRIM_PTRDIFF = 27
PRIM_SIZE = 28
PRIM_SSIZE = 29
PRIM_INT_LEAST8 = 30
PRIM_UINT_LEAST8 = 31
PRIM_INT_LEAST16 = 32
PRIM_UINT_LEAST16 = 33
PRIM_INT_LEAST32 = 34
PRIM_UINT_LEAST32 = 35
PRIM_INT_LEAST64 = 36
PRIM_UINT_LEAST64 = 37
PRIM_INT_FAST8 = 38
PRIM_UINT_FAST8 = 39
PRIM_INT_FAST16 = 40
PRIM_UINT_FAST16 = 41
PRIM_INT_FAST32 = 42
PRIM_UINT_FAST32 = 43
PRIM_INT_FAST64 = 44
PRIM_UINT_FAST64 = 45
PRIM_INTMAX = 46
PRIM_UINTMAX = 47
PRIM_FLOATCOMPLEX = 48
PRIM_DOUBLECOMPLEX = 49
PRIM_CHAR16 = 50
PRIM_CHAR32 = 51
_NUM_PRIM = 52
_UNKNOWN_PRIM = -1
_UNKNOWN_FLOAT_PRIM = -2
_UNKNOWN_LONG_DOUBLE = -3
_IO_FILE_STRUCT = -1
# WARNING: Decompyle incomplete
