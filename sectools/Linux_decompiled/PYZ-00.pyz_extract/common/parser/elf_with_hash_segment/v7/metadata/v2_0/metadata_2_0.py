
from binascii import hexlify, unhexlify
from functools import reduce
from typing import Any
from cmd_line_interface.sectools.cmd_line_common.defines import PLATFORM_BINDING, PRODUCT_SEGMENT_ID
from cmd_line_interface.sectools.secure_image.defines import DISABLE, ENABLE, JTAG_DEBUG, NOP, TRANSFER_UIE_KEY
from common.data.data import comma_separated_string, get_enabled_bit_indices_from_byte, get_lsb, hex_val, plural_s, remove_list_items_and_retain_duplicates
from common.data.defines import PAD_BYTE_0, SHA512_SIZE, SHA_DESCRIPTION_TO_SIZE
from common.parser.elf_with_hash_segment.v6.metadata.defines import NUM_SERIAL_NUMBERS, NUM_SOC_HW_VERS
from common.parser.elf_with_hash_segment.v6.metadata.metadata import MetadataCommon
from common.parser.elf_with_hash_segment.v6.metadata.v1_0.metadata_1_0 import MetadataV10
from common.parser.elf_with_hash_segment.v7.metadata.defines import DEBUG_DESCRIPTION, FALSE, FALSE_TRUE_DESCRIPTION, METADATA_MAJOR_VERSION_2, OEM_LIFECYCLE_STATE_DESCRIPTION, OEM_LIFECYCLE_STATE_DESCRIPTION_TO_INT, OEM_ROOT_CERTIFICATE_HASH_ALGO_DESCRIPTION, OEM_ROOT_CERTIFICATE_HASH_ALGO_NA, SIZE_TO_OEM_ROOT_CERTIFICATE_HASH_ALGO, SOC_LIFECYCLE_STATE_DESCRIPTION, SOC_LIFECYCLE_STATE_DESCRIPTION_TO_INT, TRUE
from profile.schema import SerialBoundFeature

class MetadataV20(MetadataV10):
    MAJOR_VERSION: int = METADATA_MAJOR_VERSION_2
    DEBUG_FLAG: dict[(int, str)] = 'debug_lock'
    DEBUG_DESCRIPTION_DICT: dict[(int, str)] = DEBUG_DESCRIPTION
    FLAGS: list[tuple[(int, str, str)]] = [
        (3, 'soc_hw_version_bound', 'Bound to SoC Hardware Versions'),
        (12, 'soc_feature_id_bound', 'Bound to SoC Feature ID'),
        (48, 'jtag_id_bound', 'Bound to JTAG ID'),
        (192, 'serial_number_bound', 'Bound to Serial Numbers'),
        (768, 'oem_id_bound', 'Bound to OEM ID'),
        (3072, 'oem_product_id_bound', 'Bound to OEM Product ID'),
        (12288, 'soc_lifecycle_state_bound', 'Bound to SoC Lifecycle State'),
        (49152, 'oem_lifecycle_state_bound', 'Bound to OEM Lifecycle State'),
        (196608, 'oem_root_certificate_hash_bound', 'Bound to OEM Root Certificate Hash'),
        (786432, DEBUG_FLAG, MetadataV10.DEBUG_FLAG_DESCRIPTION),
        (3145728, 'root_revoke_activate_enable', 'Transfer Root')]
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.soc_feature_id = 0
        self.oem_root_certificate_hash = PAD_BYTE_0 * SHA512_SIZE
        self.oem_root_certificate_hash_algorithm = OEM_ROOT_CERTIFICATE_HASH_ALGO_NA
        self.soc_lifecycle_state = 0
        self.soc_lifecycle_states = []
        self.oem_lifecycle_state = 0
        self.soc_hw_version_bound = FALSE
        self.jtag_id_bound = FALSE
        self.soc_feature_id_bound = FALSE
        self.serial_number_bound = FALSE
        self.oem_id_bound = FALSE
        self.oem_product_id_bound = FALSE
        self.oem_root_certificate_hash_bound = FALSE
        self.soc_lifecycle_state_bound = FALSE
        self.oem_lifecycle_state_bound = FALSE
        self.debug_lock = FALSE
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        fields = MetadataCommon.get_fields() + [
            'anti_rollback_version',
            'mrc_index']
        for i in range(NUM_SOC_HW_VERS):
            fields.append('soc_hw_ver_' + str(i))
        fields += [
            'soc_feature_id',
            'jtag_id']
        for i in range(NUM_SERIAL_NUMBERS):
            fields.append('serial_number_' + str(i))
        fields += [
            'oem_id',
            'oem_product_id',
            'soc_lifecycle_state',
            'oem_lifecycle_state',
            'oem_root_certificate_hash_algorithm',
            'oem_root_certificate_hash',
            'flags']
        return fields

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        fields = {
            'major_version': cls.MAJOR_VERSION,
            'minor_version': cls.MINOR_VERSION,
            'anti_rollback_version': 0,
            'mrc_index': 0 }
        for i in range(NUM_SOC_HW_VERS):
            fields['soc_hw_ver_' + str(i)] = 0
        fields.update({
            'soc_feature_id': 0,
            'jtag_id': 0 })
        for i in range(NUM_SERIAL_NUMBERS):
            fields['serial_number_' + str(i)] = 0
        fields.update({
            'oem_id': 0,
            'oem_product_id': 0,
            'soc_lifecycle_state': 0,
            'oem_lifecycle_state': 0,
            'oem_root_certificate_hash_algorithm': OEM_ROOT_CERTIFICATE_HASH_ALGO_NA,
            'oem_root_certificate_hash': PAD_BYTE_0 * SHA512_SIZE,
            'flags': reduce((lambda x, y: x | FALSE << get_lsb(y)), (lambda .0: pass# WARNING: Decompyle incomplete
)(cls.FLAGS), 0) })
        return fields

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return f'''{MetadataCommon.get_format()}II{'I' * NUM_SOC_HW_VERS}II{'Q' * NUM_SERIAL_NUMBERS}IIIII64sI'''

    get_format = None(get_format)
    
    def unpack_post_process(self = None):
        super().unpack_post_process()
        soc_lifecycle_states = get_enabled_bit_indices_from_byte(self.soc_lifecycle_state)
        for soc_lifecycle_state in soc_lifecycle_states:
            self.soc_lifecycle_states.append(1 << soc_lifecycle_state)
        if self.oem_root_certificate_hash_algorithm in OEM_ROOT_CERTIFICATE_HASH_ALGO_DESCRIPTION or self.oem_root_certificate_hash_algorithm != OEM_ROOT_CERTIFICATE_HASH_ALGO_NA:
            oem_root_certificate_hash_algorithm = OEM_ROOT_CERTIFICATE_HASH_ALGO_DESCRIPTION[self.oem_root_certificate_hash_algorithm]
            root_certificate_hash_size = SHA_DESCRIPTION_TO_SIZE[oem_root_certificate_hash_algorithm]
            self.oem_root_certificate_hash = self.oem_root_certificate_hash[SHA512_SIZE - root_certificate_hash_size:]
            return None
        return None

    
    def validate_before_operation(self = None, **__):
        error = f'''{self.METADATA_STR} has invalid'''
        if self.soc_hw_version_bound == TRUE and all((lambda .0: for soc_hw_vers in .0:
soc_hw_vers == 0)(self.soc_hw_vers)):
            raise RuntimeError(f'''{self.METADATA_STR} is bound to SoC HW Version but does not contain any SoC HW Versions.''')
        if None.serial_number_bound == TRUE and all((lambda .0: for serial_number in .0:
serial_number == 0)(self.serial_numbers)):
            raise RuntimeError(f'''{self.METADATA_STR} is bound to Serial Numbers but does not contain any Serial Numbers.''')
        if None.soc_lifecycle_state_bound == TRUE:
            if not self.soc_lifecycle_states:
                raise RuntimeError(f'''{self.METADATA_STR} is bound to SoC Lifecycle State but does not contain any SoC Lifecycle States.''')
            for soc_lifecycle_state in None.soc_lifecycle_states:
                if soc_lifecycle_state not in SOC_LIFECYCLE_STATE_DESCRIPTION:
                    raise RuntimeError(f'''{error} SoC Lifecycle State: {self.soc_lifecycle_state}.''')
                if self.oem_lifecycle_state_bound == TRUE and self.oem_lifecycle_state not in OEM_LIFECYCLE_STATE_DESCRIPTION:
                    raise RuntimeError(f'''{error} OEM Lifecycle State: {self.oem_lifecycle_state}.''')
                if None.oem_root_certificate_hash_algorithm not in OEM_ROOT_CERTIFICATE_HASH_ALGO_DESCRIPTION:
                    raise RuntimeError(f'''{error} OEM Root Certificate Hash Algorithm: {self.oem_root_certificate_hash_algorithm}.''')
                None.validate_flags()
                return None

    
    def validate_flags(self = None):
        for _, flag_name, flag_description in self.FLAGS:
            if getattr(self, flag_name) not in self.DEBUG_DESCRIPTION_DICT if flag_name == self.DEBUG_FLAG else FALSE_TRUE_DESCRIPTION:
                raise RuntimeError(f'''{flag_description} has invalid value: {getattr(self, flag_name)}.''')
            return None

    
    def pack_pre_process(self = None):
        super().pack_pre_process()
        self.soc_lifecycle_state = 0
        for soc_lifecycle_state in self.soc_lifecycle_states:
            self.soc_lifecycle_state |= soc_lifecycle_state
        padding = PAD_BYTE_0 * (SHA512_SIZE - len(self.oem_root_certificate_hash))
        self.oem_root_certificate_hash = padding + self.oem_root_certificate_hash

    
    def mask_all_fields(self = None):
        super().mask_all_fields()
        self.soc_lifecycle_states = []

    
    def get_flags_properties(self = None):
        flag_properties = []
        for _, flag_name, flag_description in self.FLAGS:
            description_dict = self.DEBUG_DESCRIPTION_DICT if flag_name == self.DEBUG_FLAG else FALSE_TRUE_DESCRIPTION
            flag_properties.append((f'''{flag_description}:''', description_dict.get(getattr(self, flag_name), hex_val(getattr(self, flag_name), True, **('strip_leading_zeros',)))))
        return flag_properties

    
    def get_properties(self = None):
        properties = [
            ('Major Version:', self.major_version),
            ('Minor Version:', self.minor_version),
            ('Anti-Rollback Version:', hex_val(self.anti_rollback_version, True, **('strip_leading_zeros',))),
            ('Root Certificate Index:', self.mrc_index)]
        soc_hw_vers = remove_list_items_and_retain_duplicates(self.soc_hw_vers, [
            0])
        if soc_hw_vers:
            properties += [
                (f'''SoC Hardware Version{plural_s(soc_hw_vers)}:''', comma_separated_string((lambda .0: [ hex_val(x, 4, True, **('num_chars', 'strip_leading_zeros')) for x in .0 ])(soc_hw_vers), 'and', **('final_separator',)))]
        properties += [
            ('SoC Feature ID:', hex_val(self.soc_feature_id, True, **('strip_leading_zeros',))),
            ('JTAG ID:', hex_val(self.jtag_id, True, **('strip_leading_zeros',)))]
        serial_numbers = remove_list_items_and_retain_duplicates(self.serial_numbers, [
            0])
        if serial_numbers:
            properties += [
                (f'''Serial Number{plural_s(serial_numbers)}:''', comma_separated_string((lambda .0: [ hex_val(x, 16, True, **('num_chars', 'strip_leading_zeros')) for x in .0 ])(serial_numbers), 'and', **('final_separator',)))]
        properties += [
            ('OEM ID:', hex_val(self.oem_id, True, **('strip_leading_zeros',))),
            ('OEM Product ID:', hex_val(self.oem_product_id, True, **('strip_leading_zeros',)))]
        if self.soc_lifecycle_states:
            properties += [
                ('SoC Lifecycle States:', self._repr_soc_lifecycle_state_bitmap())]
        properties += [
            ('OEM Lifecycle State:', OEM_LIFECYCLE_STATE_DESCRIPTION.get(self.oem_lifecycle_state, hex_val(self.oem_lifecycle_state, True, **('strip_leading_zeros',)))),
            ('OEM Root Certificate Hash Algorithm:', OEM_ROOT_CERTIFICATE_HASH_ALGO_DESCRIPTION.get(self.oem_root_certificate_hash_algorithm, hex_val(self.oem_root_certificate_hash_algorithm, True, **('strip_leading_zeros',))))]
        if self.oem_root_certificate_hash_algorithm in OEM_ROOT_CERTIFICATE_HASH_ALGO_DESCRIPTION and self.oem_root_certificate_hash_algorithm != OEM_ROOT_CERTIFICATE_HASH_ALGO_NA:
            properties += [
                ('OEM Root Certificate Hash:', '0x' + hexlify(self.oem_root_certificate_hash).decode())]
        properties += self.get_flags_properties()
        return properties

    
    def _repr_soc_lifecycle_state_bitmap(self = None):
        return comma_separated_string((lambda .0: [ SOC_LIFECYCLE_STATE_DESCRIPTION[soc_lifecycle_state] for soc_lifecycle_state in .0 ])(self.soc_lifecycle_states), 'and', **('final_separator',))

    
    def set_software_id(self = None, software_id = None):
        pass

    
    def set_platform_binding(self, soc_hw_versions = None, soc_feature_ids = None, jtag_ids = None, product_segment_ids = ('soc_hw_versions', list[int], 'soc_feature_ids', list[int], 'jtag_ids', list[int], 'product_segment_ids', list[int], 'return', None)):
        if product_segment_ids:
            raise RuntimeError(f'''{PLATFORM_BINDING} {PRODUCT_SEGMENT_ID} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')
        if None:
            self.validate_soc_hw_vers(soc_hw_versions)
            self.soc_hw_vers = soc_hw_versions
            self.soc_hw_version_bound = TRUE
        if jtag_ids:
            self.jtag_id = jtag_ids[0]
            self.jtag_id_bound = TRUE
        if soc_feature_ids:
            self.soc_feature_id = soc_feature_ids[0]
            self.soc_feature_id_bound = TRUE
            return None

    
    def set_serial_numbers(self, serial_numbers = None, supports_serial_numbers = None, _ = None, fatal = ('serial_numbers', list[int] | None, 'supports_serial_numbers', SerialBoundFeature, 'fatal', bool, 'return', None)):
        if serial_numbers:
            if supports_serial_numbers.supports_single_serial or supports_serial_numbers.supports_multi_serials:
                if len(serial_numbers) > NUM_SERIAL_NUMBERS:
                    if fatal:
                        raise RuntimeError(f'''Number of serial numbers provided exceeds allowed maximum of {NUM_SERIAL_NUMBERS}.''')
                    return None
                self.serial_numbers = None
                self.serial_number_bound = TRUE
                return None
            return None

    
    def set_oem_id_and_oem_product_id(self = None, oem_id = None, oem_product_id = None):
        if oem_id is not None:
            self.oem_id = oem_id
            self.oem_id_bound = TRUE
        if oem_product_id is not None:
            self.oem_product_id = oem_product_id
            self.oem_product_id_bound = TRUE
            return None

    
    def set_root_revoke_activate_enable(self = None, transfer_root = None, *_):
        if transfer_root:
            self.root_revoke_activate_enable = TRUE
            return None
        self.root_revoke_activate_enable = None

    
    def set_oem_root_certificate_hash(self = None, oem_root_certificate_hash = None):
        if oem_root_certificate_hash:
            self.oem_root_certificate_hash = unhexlify(oem_root_certificate_hash[2:])
            self.oem_root_certificate_hash_bound = TRUE
            self.oem_root_certificate_hash_algorithm = SIZE_TO_OEM_ROOT_CERTIFICATE_HASH_ALGO[len(oem_root_certificate_hash[2:]) // 2]
            return None
        self.oem_root_certificate_hash_algorithm = None

    
    def set_soc_lifecycle_state(self = None, soc_lifecycle_states = None):
        if soc_lifecycle_states:
            self.soc_lifecycle_states = (lambda .0: [ SOC_LIFECYCLE_STATE_DESCRIPTION_TO_INT[soc_lifecycle_state] for soc_lifecycle_state in .0 ])(soc_lifecycle_states)
            self.soc_lifecycle_state_bound = TRUE
            return None

    
    def set_oem_lifecycle_state(self = None, oem_lifecycle_state = None):
        if oem_lifecycle_state is not None:
            self.oem_lifecycle_state = OEM_LIFECYCLE_STATE_DESCRIPTION_TO_INT[oem_lifecycle_state]
            self.oem_lifecycle_state_bound = TRUE
            return None

    
    def set_jtag_debug(self = None, jtag_debug = None):
        if jtag_debug == NOP:
            self.debug_lock = FALSE
            return None
        if None == DISABLE:
            self.debug_lock = TRUE
            return None
        if None == ENABLE:
            raise RuntimeError(f'''{JTAG_DEBUG} {ENABLE} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')

    
    def set_secondary_software_id(self = None, secondary_software_id = None, feature_id = None):
        pass

    
    def set_uie_key_switch_enable(self = None, transfer_uie_key = None, *_):
        if transfer_uie_key:
            raise RuntimeError(f'''{TRANSFER_UIE_KEY} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')

    
    def get_oem_id_bound(self = None):
        return self.oem_id_bound == TRUE

    
    def get_oem_product_id_bound(self = None):
        return self.oem_product_id_bound == TRUE

    
    def get_soc_hw_vers_bound(self = None):
        return self.soc_hw_version_bound == TRUE

    __classcell__ = None

