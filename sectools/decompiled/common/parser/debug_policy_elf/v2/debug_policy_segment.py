
from binascii import hexlify
from typing import List, Optional, Union
from common.data.data import get_enabled_bit_indices_from_byte, hex_val, properties_repr
from common.data.defines import PAD_BYTE_0
from common.parser.debug_policy_elf.debug_policy_segment import DebugPolicySegmentCommon
from common.parser.debug_policy_elf.defines import DEBUG_POLICY_V2
from common.parser.debug_policy_elf.v1.defines import LOGS
from common.parser.debug_policy_elf.v2.defines import JTAG, NUM_ROOT_CERTIFICATE_HASHES, NUM_SERIAL_NUMBERS

class DebugPolicySegmentV2(DebugPolicySegmentCommon):
    VERSION = DEBUG_POLICY_V2
    FLAGS = DebugPolicySegmentCommon.FLAGS | {
        2: (JTAG, 'Enable JTAG'),
        3: (LOGS, 'Enable Logs') }
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.flags = 0
        self.software_id_bitmap = 0
        self.software_ids = []
        self.root_certificate_hash_count = 0
        self.root_certificate_hashes = []
        self.serial_number_count = 0
        self.serial_numbers = []
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        fields = super().get_fields() + [
            'flags',
            'software_id_bitmap',
            'root_certificate_hash_count']
        for i in range(NUM_ROOT_CERTIFICATE_HASHES):
            fields.append('root_certificate_hash_' + str(i))
        fields.append('serial_number_count')
        for i in range(NUM_SERIAL_NUMBERS):
            fields.append('serial_number_' + str(i))
        return fields

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return f'''{super().get_format()}QII{f'''{cls.hash_size()}s''' * NUM_ROOT_CERTIFICATE_HASHES}I{'I' * NUM_SERIAL_NUMBERS}'''

    get_format = None(get_format)
    
    def unpack_post_process(self):
        for flag_name, _ in self.FLAGS.items():
            setattr(self, flag_name, (self.flags & 1 << flag_bit) >> flag_bit)
        self.software_ids = get_enabled_bit_indices_from_byte(self.software_id_bitmap)
        for i in range(NUM_ROOT_CERTIFICATE_HASHES):
            if i < self.root_certificate_hash_count:
                self.root_certificate_hashes.append(getattr(self, 'root_certificate_hash_' + str(i)))
        for i in range(NUM_SERIAL_NUMBERS):
            if i < self.serial_number_count:
                self.serial_numbers.append(getattr(self, 'serial_number_' + str(i)))

    
    def validate_critical_fields(self = None):
        super().validate_critical_fields()
        if self.version != self.VERSION:
            raise RuntimeError(f'''Debug Policy Segment has invalid version: {self.version}.''')

    
    def pack_pre_process(self):
        self.flags = 0
        for flag_name, _ in self.FLAGS.items():
            self.flags |= getattr(self, flag_name) << flag_bit
        self.software_id_bitmap = 0
        for software_id in self.software_ids:
            self.software_id_bitmap |= 1 << software_id
        self.root_certificate_hash_count = len(self.root_certificate_hashes)
        for i in range(NUM_ROOT_CERTIFICATE_HASHES):
            if self.root_certificate_hashes and i < len(self.root_certificate_hashes):
                setattr(self, 'root_certificate_hash_' + str(i), self.root_certificate_hashes[i])
                continue
            setattr(self, 'root_certificate_hash_' + str(i), PAD_BYTE_0 * self.hash_size())
        self.serial_number_count = len(self.serial_numbers)
        for i in range(NUM_SERIAL_NUMBERS):
            if self.serial_numbers and i < len(self.serial_numbers):
                setattr(self, 'serial_number_' + str(i), self.serial_numbers[i])
                continue
            setattr(self, 'serial_number_' + str(i), 0)

    
    def get_header_properties(self):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self):
        string = 'Debug Policy Segment:\n' + properties_repr(self.get_header_properties())
        flags = (lambda .0 = None: [ description for flag_name, description in .0 if getattr(self, flag_name) ])(self.FLAGS.items())
        if flags:
            string += '\n\nDebug Policy Enabled Flags:\n' + properties_repr((lambda .0: [ (flag,) for flag in .0 ])(flags))
        if self.software_ids:
            string += '\n\nDebug Policy Enabled Software IDs:\n' + properties_repr((lambda .0: [ (hex_val(software_id, True, **('strip_leading_zeros',)),) for software_id in .0 ])(self.software_ids))
        if self.root_certificate_hashes:
            string += '\n\nDebug Policy Enabled OEM Root Certificate Hashes:\n' + properties_repr((lambda .0: [ ('0x' + hexlify(root_certificate_hash).decode(),) for root_certificate_hash in .0 ])(self.root_certificate_hashes))
        if self.serial_numbers:
            string += '\n\nDebug Policy Serial Numbers:\n' + properties_repr((lambda .0: [ (hex_val(serial_number, True, **('strip_leading_zeros',)),) for serial_number in .0 ])(self.serial_numbers))
        return string

    
    def set_serial_numbers(self, serial_numbers):
        serial_numbers = sorted((lambda .0: [ int(x, 16) for x in .0 ])(set(serial_numbers)))
        if len(serial_numbers) > NUM_SERIAL_NUMBERS:
            raise RuntimeError(f'''Debug Policy v{self.version} images support a maximum of {NUM_SERIAL_NUMBERS} serial numbers''')
        self.serial_numbers = None
        self.serial_number_count = len(self.serial_numbers)

    
    def set_oem_root_certificate_hashes(self = None, oem_root_certificate_hashes = None):
        if len(set(oem_root_certificate_hashes)) > NUM_ROOT_CERTIFICATE_HASHES:
            raise RuntimeError(f'''Debug Policy v{self.version} images support a maximum of {NUM_ROOT_CERTIFICATE_HASHES} OEM Root Certificate Hashes''')
        None().set_oem_root_certificate_hashes(oem_root_certificate_hashes)

    
    def set_qti_root_certificate_hashes(self, qti_root_certificate_hashes):
        raise RuntimeError(f'''Debug Policy v{self.version} images do not support QTI Root Certificate Hashes''')

    __classcell__ = None

