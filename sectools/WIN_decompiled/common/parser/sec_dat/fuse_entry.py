
from typing import Any, List, Optional, Tuple, Union
from common.data.binary_struct import StructBase
from common.data.data import hex_val
from common.parser.sec_dat.defines import OPERATION_INT_TO_DESCRIPTION_V1, OPERATION_INT_TO_DESCRIPTION_V3, REGION_TYPE_INT_TO_DESCRIPTION_V1, REGION_TYPE_INT_TO_DESCRIPTION_V3

class FuseEntry(StructBase):
    REG_TYPE_INT_TO_DESCRIPTION = REGION_TYPE_INT_TO_DESCRIPTION_V1
    OPERATION_INT_TO_DESCRIPTION = OPERATION_INT_TO_DESCRIPTION_V1
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.region_type = 0
        self.address = 0
        self._lsb = 0
        self._msb = 0
        self.operation = 0
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def from_values(cls, region_type, address = None, lsb = None, msb = classmethod, operation = ('region_type', int, 'address', int, 'lsb', int, 'msb', int, 'operation', int, 'return', 'FuseEntry')):
        fuse_entry = cls()
        fuse_entry.region_type = region_type
        fuse_entry.address = address
        fuse_entry.lsb = lsb
        fuse_entry.msb = msb
        fuse_entry.operation = operation
        fuse_entry.validate()
        return fuse_entry

    from_values = None(from_values)
    
    def get_fields(cls = None):
        return [
            'region_type',
            'address',
            'lsb',
            'msb',
            'operation']

    get_fields = None(get_fields)
    
    def get_format(cls = None):
        return '<IIIII'

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        if self.region_type not in self.REG_TYPE_INT_TO_DESCRIPTION:
            raise RuntimeError(f'''Sec Dat Fuse Entry contains invalid Region Type: {self.region_type}.''')
        if None.operation not in self.OPERATION_INT_TO_DESCRIPTION:
            raise RuntimeError(f'''Sec Dat Fuse Entry contains invalid Operation: {self.operation}.''')

    
    def validate(self = None):
        self.validate_critical_fields()

    
    def validate_before_operation(self = None, **_):
        self.validate()

    
    def get_properties(self = None):
        return [
            ('Region Type', self.REG_TYPE_INT_TO_DESCRIPTION.get(self.region_type, self.region_type)),
            ('MSB', hex_val(self.msb)),
            ('LSB', hex_val(self.lsb, True, **('without_0x',))),
            ('Operation', self.OPERATION_INT_TO_DESCRIPTION.get(self.operation, self.operation)),
            ('Address', hex_val(self.address))]

    
    def __eq__(self = None, other = None):
        if not isinstance(other, type(self)):
            return False
        return (None.region_type, self.address, self.lsb, self.msb, self.operation) == (other.region_type, other.address, other.lsb, other.msb, other.operation)

    
    def lsb(self = None):
        return self._lsb

    lsb = None(lsb)
    
    def lsb(self = None, value = None):
        if not value <= value or value < 0x100000000L:
            pass
        else:
            0
    # WARNING: Decompyle incomplete

    lsb = None(lsb)
    
    def msb(self = None):
        return self._msb

    msb = None(msb)
    
    def msb(self = None, value = None):
        if not value <= value or value < 0x100000000L:
            pass
        else:
            0
    # WARNING: Decompyle incomplete

    msb = None(msb)
    __classcell__ = None


class FuseEntryV3(FuseEntry):
    REG_TYPE_INT_TO_DESCRIPTION = REGION_TYPE_INT_TO_DESCRIPTION_V3
    OPERATION_INT_TO_DESCRIPTION = OPERATION_INT_TO_DESCRIPTION_V3

