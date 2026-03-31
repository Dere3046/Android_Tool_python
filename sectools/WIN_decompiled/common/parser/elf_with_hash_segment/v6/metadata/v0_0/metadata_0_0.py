
from typing import Any
from cmd_line_interface.sectools.cmd_line_common.defines import INDEPENDENT, OEM_LIFECYCLE_STATE, PLATFORM_BINDING, PRODUCT_SEGMENT_ID, SERIAL_NUMBER, SOC_FEATURE_ID, SOC_LIFECYCLE_STATE
from cmd_line_interface.sectools.secure_image.defines import CRASH_DUMP, DISABLE, ENABLE, OEM_ROOT_CERTIFICATE_HASH
from common.data.binary_struct import DetailsTuple
from common.data.data import comma_separated_string, get_lsb, hex_val, plural_s, remove_list_items_and_retain_duplicates
from common.data.defines import PAD_BYTE_0
from common.parser.elf_with_hash_segment.v6.metadata.defines import DEBUG_DESCRIPTION, DEBUG_DISABLE, DEBUG_ENABLE, DEBUG_NOP, FALSE, FALSE_TRUE_BOUND_DESCRIPTION, METADATA_MAJOR_VERSION_0, METADATA_MINOR_VERSION_0, NUM_SERIAL_NUMBERS, NUM_SOC_HW_VERS, TRUE, TRUE_BOUND
from common.parser.elf_with_hash_segment.v6.metadata.metadata import MetadataCommon
from profile.schema import SerialBoundFeature

class MetadataV00(MetadataCommon):
    MAJOR_VERSION: int = METADATA_MAJOR_VERSION_0
    MINOR_VERSION: int = METADATA_MINOR_VERSION_0
    DEBUG_FLAG: str = 'debug'
    DEBUG_FLAG_DESCRIPTION: str = 'JTAG Debug'
    DEBUG_DESCRIPTION_DICT: dict[(int, str)] = DEBUG_DESCRIPTION
    FLAGS: list[tuple[(int, str, str)]] = [
        (1, 'rot_en', 'Root of Trust Enabled'),
        (2, 'in_use_soc_hw_version', 'Bound to SoC Hardware Versions'),
        (4, 'use_serial_number_in_signing', 'Bound to Serial Numbers'),
        (8, 'oem_id_independent', 'Bound to OEM ID'),
        (48, 'root_revoke_activate_enable', 'Transfer Root'),
        (192, 'uie_key_switch_enable', 'Transfer UIE Key'),
        (768, DEBUG_FLAG, DEBUG_FLAG_DESCRIPTION)]
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.software_id = 0
        self.soc_hw_vers = []
        self.jtag_id = 0
        self.serial_numbers = []
        self.oem_id = 0
        self.oem_product_id = 0
        self.anti_rollback_version = 0
        self.mrc_index = 0
        self.debug = DEBUG_NOP
        self.secondary_software_id = 0
        self.flags = 0
        self.in_use_soc_hw_version = FALSE
        self.use_serial_number_in_signing = FALSE
        self.oem_id_independent = FALSE
        self.root_revoke_activate_enable = FALSE
        self.uie_key_switch_enable = FALSE
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        fields = super().get_fields() + [
            'software_id',
            'jtag_id',
            'oem_id',
            'oem_product_id',
            'secondary_software_id',
            'flags']
        for i in range(NUM_SOC_HW_VERS):
            fields.append('soc_hw_ver_' + str(i))
        for i in range(NUM_SERIAL_NUMBERS):
            fields.append('serial_number_' + str(i))
        fields += [
            'mrc_index',
            'anti_rollback_version']
        return fields

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        fields = {
            'major_version': cls.MAJOR_VERSION,
            'minor_version': cls.MINOR_VERSION,
            'software_id': 0,
            'jtag_id': 0,
            'oem_id': 0,
            'oem_product_id': 0,
            'secondary_software_id': 0,
            'flags': 0 }
        for i in range(NUM_SOC_HW_VERS):
            fields['soc_hw_ver_' + str(i)] = 0
        for i in range(NUM_SERIAL_NUMBERS):
            fields['serial_number_' + str(i)] = 0
        fields.update({
            'mrc_index': 0,
            'anti_rollback_version': 0 })
        return fields

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + 'IIIIIIIIIIIIIIIIIIIIIIIIIIII'

    get_format = None(get_format)
    
    def unpack_post_process(self = None):
        self.soc_hw_vers = []
        for i in range(NUM_SOC_HW_VERS):
            self.soc_hw_vers.append(getattr(self, 'soc_hw_ver_' + str(i)))
        self.serial_numbers = []
        for i in range(NUM_SERIAL_NUMBERS):
            self.serial_numbers.append(getattr(self, 'serial_number_' + str(i)))
        for flag_mask, flag_name, _ in self.FLAGS:
            setattr(self, flag_name, (self.flags & flag_mask) >> get_lsb(flag_mask))

    
    def validate_critical_fields(self = None):
        if (self.major_version, self.minor_version) != (self.MAJOR_VERSION, self.MINOR_VERSION):
            raise RuntimeError(f'''{self.METADATA_STR} has invalid version: {self.major_version}.{self.minor_version}.''')

    
    def validate(self = None):
        self.validate_critical_fields()

    
    def validate_before_operation(self = None, **_):
        if self.in_use_soc_hw_version == TRUE and all((lambda .0: for soc_hw_vers in .0:
soc_hw_vers == 0)(self.soc_hw_vers)):
            raise RuntimeError(f'''{self.METADATA_STR} is bound to SoC HW Version but does not contain any SoC HW Versions.''')
        if None.use_serial_number_in_signing == TRUE or all((lambda .0: for serial_number in .0:
serial_number == 0)(self.serial_numbers)):
            raise RuntimeError(f'''{self.METADATA_STR} is bound to Serial Numbers but does not contain any Serial Numbers.''')
        return None

    
    def pack_pre_process(self = None):
        for i in range(NUM_SOC_HW_VERS):
            if i < len(self.soc_hw_vers):
                setattr(self, 'soc_hw_ver_' + str(i), self.soc_hw_vers[i])
                continue
            setattr(self, 'soc_hw_ver_' + str(i), 0)
        for i in range(NUM_SERIAL_NUMBERS):
            if i < len(self.serial_numbers):
                setattr(self, 'serial_number_' + str(i), self.serial_numbers[i])
                continue
            setattr(self, 'serial_number_' + str(i), 0)
        self.flags = 0
        for flag_mask, flag_name, _ in self.FLAGS:
            self.flags |= getattr(self, flag_name) << get_lsb(flag_mask)

    
    def mask_all_fields(self = None):
        self.soc_hw_vers = []
        self.serial_numbers = []
        self.flags = 0
        for attr in self.get_fields():
            if isinstance(getattr(self, attr), int):
                setattr(self, attr, 0)
                continue
            if isinstance(getattr(self, attr), bytes):
                setattr(self, attr, PAD_BYTE_0 * len(getattr(self, attr)))
        for _, flag_name, _ in self.FLAGS:
            setattr(self, flag_name, 0)

    
    def get_flags_properties(self = None):
        return [
            ('Bound to SoC Hardware Versions:', self.get_soc_hw_vers_bound()),
            ('Bound to JTAG ID:', not self.get_soc_hw_vers_bound()),
            ('Bound to Serial Numbers:', bool(self.use_serial_number_in_signing)),
            ('Bound to OEM ID:', self.get_oem_id_bound()),
            ('Bound to OEM Product ID:', self.get_oem_product_id_bound()),
            ('Transfer Root:', FALSE_TRUE_BOUND_DESCRIPTION.get(self.root_revoke_activate_enable, hex_val(self.root_revoke_activate_enable, True, **('strip_leading_zeros',)))),
            ('Transfer UIE Key:', FALSE_TRUE_BOUND_DESCRIPTION.get(self.uie_key_switch_enable, hex_val(self.uie_key_switch_enable, True, **('strip_leading_zeros',)))),
            (f'''{self.DEBUG_FLAG_DESCRIPTION}:''', self.DEBUG_DESCRIPTION_DICT.get(self.debug, hex_val(self.debug, True, **('strip_leading_zeros',))))]

    
    def get_properties(self = None):
        properties = [
            ('Major Version:', self.major_version),
            ('Minor Version:', self.minor_version),
            ('Software ID:', hex_val(self.software_id, True, **('strip_leading_zeros',))),
            ('JTAG ID:', hex_val(self.jtag_id, True, **('strip_leading_zeros',))),
            ('OEM ID:', hex_val(self.oem_id, True, **('strip_leading_zeros',))),
            ('OEM Product ID:', hex_val(self.oem_product_id, True, **('strip_leading_zeros',))),
            ('Secondary Software ID:', hex_val(self.secondary_software_id, True, **('strip_leading_zeros',)))]
        properties += self.get_flags_properties()
        soc_hw_vers = remove_list_items_and_retain_duplicates(self.soc_hw_vers, [
            0])
        if soc_hw_vers:
            properties += [
                (f'''SoC Hardware Version{plural_s(soc_hw_vers)}:''', comma_separated_string((lambda .0: [ hex_val(x, 4, True, **('num_chars', 'strip_leading_zeros')) for x in .0 ])(soc_hw_vers), 'and', **('final_separator',)))]
        serial_numbers = remove_list_items_and_retain_duplicates(self.serial_numbers, [
            0])
        if serial_numbers:
            properties += [
                (f'''Serial Number{plural_s(serial_numbers)}:''', comma_separated_string((lambda .0: [ hex_val(x, True, **('strip_leading_zeros',)) for x in .0 ])(serial_numbers), 'and', **('final_separator',)))]
        properties += [
            ('Root Certificate Index:', self.mrc_index),
            ('Anti-Rollback Version:', hex_val(self.anti_rollback_version, True, **('strip_leading_zeros',)))]
        return properties

    
    def get_details(self = None, authority = None):
        return (self.get_fields(), self.get_format(), {
            'flags': (lambda .0: pass# WARNING: Decompyle incomplete
)(self.FLAGS) })

    
    def set_software_id(self = None, software_id = None):
        self.software_id = software_id

    
    def validate_soc_hw_vers(soc_hw_vers = None):
        if len(soc_hw_vers) > NUM_SOC_HW_VERS:
            soc_hw_vers_string = comma_separated_string((lambda .0: [ hex(soc_hw_ver) for soc_hw_ver in .0 ])(soc_hw_vers), 'and', **('final_separator',))
            raise RuntimeError(f'''Cannot bind image to SOC HW Versions, {soc_hw_vers_string}, because maximum supported number of SOC HW Versions is {NUM_SOC_HW_VERS}.''')

    validate_soc_hw_vers = None(validate_soc_hw_vers)
    
    def set_platform_binding(self, soc_hw_versions = None, soc_feature_ids = None, jtag_ids = None, product_segment_ids = ('soc_hw_versions', list[int], 'soc_feature_ids', list[int], 'jtag_ids', list[int], 'product_segment_ids', list[int], 'return', None)):
        if soc_hw_versions and jtag_ids:
            raise RuntimeError(f'''Cannot simultaneously bind to both SOC HW Version and JTAG ID for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')
        if None:
            raise RuntimeError(f'''{PLATFORM_BINDING} {SOC_FEATURE_ID} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')
        if None:
            raise RuntimeError(f'''{PLATFORM_BINDING} {PRODUCT_SEGMENT_ID} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')
        if None:
            self.validate_soc_hw_vers(soc_hw_versions)
            self.soc_hw_vers = soc_hw_versions
            self.in_use_soc_hw_version = TRUE
            return None
        if None:
            self.jtag_id = jtag_ids[0]
            self.in_use_soc_hw_version = FALSE
            return None
        raise None(f'''{PLATFORM_BINDING} {INDEPENDENT} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')

    
    def set_serial_numbers(self, serial_numbers = None, supports_serial_numbers = None, serial_bound_device_restrictions = None, fatal = ('serial_numbers', list[int] | None, 'supports_serial_numbers', SerialBoundFeature, 'serial_bound_device_restrictions', dict[(SerialBoundFeature, bool)], 'fatal', bool, 'return', None)):
        pass
    # WARNING: Decompyle incomplete

    
    def set_oem_id_and_oem_product_id(self = None, oem_id = None, oem_product_id = None):
        if (oem_id, oem_product_id) == (None, None):
            self.oem_id_independent = TRUE
            self.oem_id = 1
            return None
        if None is not None:
            self.oem_id = oem_id
        if oem_product_id is not None:
            self.oem_product_id = oem_product_id
            return None

    
    def set_anti_rollback_version(self = None, anti_rollback_version = None):
        if anti_rollback_version is not None:
            self.anti_rollback_version = anti_rollback_version
            return None

    
    def set_root_revoke_activate_enable(self, transfer_root = None, serial_numbers = None, supports_serial_numbers = None, fatal = ('transfer_root', bool, 'serial_numbers', list[int] | None, 'supports_serial_numbers', SerialBoundFeature, 'fatal', bool, 'return', None)):
        if transfer_root:
            if serial_numbers:
                if supports_serial_numbers.supports_single_serial or supports_serial_numbers.supports_multi_serials:
                    if len(serial_numbers) > NUM_SERIAL_NUMBERS:
                        if fatal:
                            raise RuntimeError(f'''Number of serial numbers provided exceeds allowed maximum of {NUM_SERIAL_NUMBERS}.''')
                        self.root_revoke_activate_enable = None
                        return None
                    self.root_revoke_activate_enable = None
                    return None
                self.root_revoke_activate_enable = None
                return None
            return None

    
    def set_oem_root_certificate_hash(self = None, oem_root_certificate_hash = None):
        if oem_root_certificate_hash:
            raise RuntimeError(f'''{OEM_ROOT_CERTIFICATE_HASH} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')

    
    def set_soc_lifecycle_state(self = None, soc_lifecycle_states = None):
        if soc_lifecycle_states:
            raise RuntimeError(f'''{SOC_LIFECYCLE_STATE} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')

    
    def set_oem_lifecycle_state(self = None, oem_lifecycle_state = None):
        if oem_lifecycle_state:
            raise RuntimeError(f'''{OEM_LIFECYCLE_STATE} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')

    
    def set_jtag_debug(self = None, jtag_debug = None):
        if jtag_debug == DISABLE:
            self.debug = DEBUG_DISABLE
            return None
        if None == ENABLE:
            self.debug = DEBUG_ENABLE
            return None
        self.debug = None

    
    def set_secondary_software_id(self = None, secondary_software_id = None, feature_id = None):
        if secondary_software_id is not None:
            self.secondary_software_id = secondary_software_id
        if feature_id is not None:
            self.secondary_software_id = feature_id
            return None

    
    def set_uie_key_switch_enable(self = None, transfer_uie_key = None, serial_numbers = None, supports_serial_numbers = ('transfer_uie_key', bool, 'serial_numbers', list[int] | None, 'supports_serial_numbers', SerialBoundFeature, 'return', None)):
        if transfer_uie_key:
            if serial_numbers:
                if supports_serial_numbers.supports_single_serial or supports_serial_numbers.supports_multi_serials:
                    if len(serial_numbers) > NUM_SERIAL_NUMBERS:
                        raise RuntimeError(f'''Number of serial numbers provided exceeds allowed maximum of {NUM_SERIAL_NUMBERS}.''')
                    self.uie_key_switch_enable = None
                    return None
                self.uie_key_switch_enable = None
                return None
            return None

    
    def set_crash_dump(self = None, crash_dump = None):
        if crash_dump:
            raise RuntimeError(f'''{CRASH_DUMP} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')

    
    def __eq__(self = None, metadata = None):
        match = False
        if isinstance(metadata, Metadata):
            metadata_1 = self.__class__(self.pack(), True, **('bypass_validation',))
            metadata_2 = metadata.__class__(metadata.pack(), True, **('bypass_validation',))
            if set(metadata_1.soc_hw_vers) == set(metadata_2.soc_hw_vers):
                pass
            match = set(metadata_1.serial_numbers) == set(metadata_2.serial_numbers)
            for None in self.get_fields():
                field = None
                if not None((lambda .0 = None: for field_name in .0:
field_name in field)(('soc_hw_ver', 'serial_number'))):
                    if match:
                        pass
                    match = getattr(metadata_1, field) == getattr(metadata_2, field)
        return match

    
    def get_oem_id_bound(self = None):
        if not (self.oem_id_independent):
            pass
        return not self.is_all_padding()

    
    def get_oem_product_id_bound(self = None):
        if not (self.oem_id_independent):
            pass
        return not self.is_all_padding()

    
    def get_soc_hw_vers_bound(self = None):
        return bool(self.in_use_soc_hw_version)

    __classcell__ = None

Metadata = MetadataV00
