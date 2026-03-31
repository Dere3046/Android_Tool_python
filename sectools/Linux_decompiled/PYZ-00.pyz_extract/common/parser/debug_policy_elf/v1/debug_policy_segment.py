
from binascii import hexlify
from typing import Optional
from common.data.data import hex_val, properties_repr
from common.parser.debug_policy_elf.debug_policy_segment import DebugPolicySegmentCommon
from common.parser.debug_policy_elf.defines import DEBUG_POLICY_V1
from common.parser.debug_policy_elf.v1.defines import LOGS, NUM_SOFTWARE_IDS

class DebugPolicySegmentV1(DebugPolicySegmentCommon):
    VERSION = DEBUG_POLICY_V1
    FLAGS = DebugPolicySegmentCommon.FLAGS | {
        4: (LOGS, 'Enable Logs') }
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.flags = 0
        self.data_size = 0
        self.software_id_count = 0
        self.serial_number_start = 0
        self.serial_number_end = 0
        self.software_ids = []
        self.root_certificate_hash_count = 0
        self.root_certificate_hashes = []
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        fields = super().get_fields() + [
            'serial_number_start',
            'serial_number_end',
            'reserved',
            'flags',
            'software_id_count']
        for i in range(NUM_SOFTWARE_IDS):
            fields.append('software_id_' + str(i))
        fields.append('root_certificate_hash_count')
        return fields

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return f'''{super().get_format()}IIIQI{'I' * NUM_SOFTWARE_IDS}I'''

    get_format = None(get_format)
    
    def unpack_post_process(self = None):
        for flag_name, _ in self.FLAGS.items():
            setattr(self, flag_name, (self.flags & 1 << flag_bit) >> flag_bit)
        for i in range(NUM_SOFTWARE_IDS):
            software_id = getattr(self, 'software_id_' + str(i))
            if i < self.software_id_count:
                self.software_ids.append(software_id)
    # WARNING: Decompyle incomplete

    
    def validate_critical_fields(self = None):
        super().validate_critical_fields()
        if self.version != self.VERSION:
            raise RuntimeError(f'''Debug Policy Segment has invalid version: {self.version}.''')

    
    def pack_pre_process(self = None):
        self.flags = 0
        for flag_name, _ in self.FLAGS.items():
            self.flags |= getattr(self, flag_name) << flag_bit
        self.software_id_count = len(self.software_ids)
        for i in range(NUM_SOFTWARE_IDS):
            if self.software_ids and i < len(self.software_ids):
                setattr(self, 'software_id_' + str(i), self.software_ids[i])
                continue
            setattr(self, 'software_id_' + str(i), 0)
        self.root_certificate_hash_count = len(self.root_certificate_hashes)

    
    def pack(self = None):
        data = super().pack()
        if self.root_certificate_hashes:
            data += b''.join(self.root_certificate_hashes)
        return memoryview(data)

    
    def get_size(self = None):
        return super().get_size() + self.hash_size() * self.root_certificate_hash_count

    
    def get_header_properties(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        string = 'Debug Policy Segment:\n' + properties_repr(self.get_header_properties())
        flags = (lambda .0 = None: [ description for flag_name, description in .0 if getattr(self, flag_name) ])(self.FLAGS.items())
        if flags:
            string += '\n\nDebug Policy Enabled Flags:\n' + properties_repr((lambda .0: [ (flag,) for flag in .0 ])(flags))
        if self.software_ids:
            string += '\n\nDebug Policy Enabled Software IDs:\n' + properties_repr((lambda .0: [ (hex_val(software_id, True, **('strip_leading_zeros',)),) for software_id in .0 ])(self.software_ids))
        if self.root_certificate_hashes:
            string += '\n\nDebug Policy Enabled OEM Root Certificate Hashes:\n' + properties_repr((lambda .0: [ ('0x' + hexlify(root_certificate_hash).decode(),) for root_certificate_hash in .0 ])(self.root_certificate_hashes))
        return string

    
    def set_serial_numbers(self = None, serial_numbers = None):
        converted_serial_numbers = (lambda .0: [ int(x, 16) for x in .0 ])(list(set(serial_numbers)))
        if len(converted_serial_numbers) > 1:
            raise RuntimeError(f'''Debug Policy v{self.version} images support a maximum of one serial number''')
        self.serial_number_start = None[0]
        self.serial_number_end = converted_serial_numbers[0]

    
    def set_oem_root_certificate_hashes(self = None, oem_root_certificate_hashes = None):
        super().set_oem_root_certificate_hashes(oem_root_certificate_hashes)
        self.data_size = self.get_size()

    
    def set_qti_root_certificate_hashes(self = None, qti_root_certificate_hashes = None):
        raise RuntimeError(f'''Debug Policy v{self.version} images do not support QTI Root Certificate Hashes''')

    __classcell__ = None

