
from typing import Any
from cmd_line_interface.sectools.cmd_line_common.defines import PLATFORM_BINDING, PRODUCT_SEGMENT_ID, SOC_FEATURE_ID
from common.data.data import hex_val
from common.parser.elf_with_hash_segment.v6.metadata.defines import FALSE, FALSE_TRUE_BOUND_DESCRIPTION, METADATA_MAJOR_VERSION_1, TRUE
from common.parser.elf_with_hash_segment.v6.metadata.v0_0.metadata_0_0 import MetadataV00

class MetadataV10(MetadataV00):
    MAJOR_VERSION: int = METADATA_MAJOR_VERSION_1
    FLAGS: list[tuple[(int, str, str)]] = MetadataV00.FLAGS + [
        (1024, 'in_use_jtag_id', 'Bound to JTAG ID'),
        (2048, 'oem_product_id_independent', 'Bound to OEM Product ID')]
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.jtag_id = 0
        self.in_use_jtag_id = FALSE
        self.oem_product_id_independent = FALSE
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_flags_properties(self = None):
        return [
            ('Bound to SoC Hardware Versions:', self.get_soc_hw_vers_bound()),
            ('Bound to Serial Numbers:', bool(self.use_serial_number_in_signing)),
            ('Bound to OEM ID:', self.get_oem_id_bound()),
            ('Transfer Root:', FALSE_TRUE_BOUND_DESCRIPTION.get(self.root_revoke_activate_enable, hex_val(self.root_revoke_activate_enable, True, **('strip_leading_zeros',)))),
            ('Transfer UIE Key:', FALSE_TRUE_BOUND_DESCRIPTION.get(self.uie_key_switch_enable, hex_val(self.uie_key_switch_enable, True, **('strip_leading_zeros',)))),
            (f'''{self.DEBUG_FLAG_DESCRIPTION}:''', self.DEBUG_DESCRIPTION_DICT.get(self.debug, hex_val(self.debug, True, **('strip_leading_zeros',)))),
            ('Bound to JTAG ID:', bool(self.in_use_jtag_id)),
            ('Bound to OEM Product ID:', self.get_oem_product_id_bound())]

    
    def set_platform_binding(self, soc_hw_versions = None, soc_feature_ids = None, jtag_ids = None, product_segment_ids = ('soc_hw_versions', list[int], 'soc_feature_ids', list[int], 'jtag_ids', list[int], 'product_segment_ids', list[int], 'return', None)):
        if soc_feature_ids:
            raise RuntimeError(f'''{PLATFORM_BINDING} {SOC_FEATURE_ID} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')
        if None:
            raise RuntimeError(f'''{PLATFORM_BINDING} {PRODUCT_SEGMENT_ID} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')
        if None:
            self.validate_soc_hw_vers(soc_hw_versions)
            self.soc_hw_vers = soc_hw_versions
            self.in_use_soc_hw_version = TRUE
        if jtag_ids:
            self.jtag_id = jtag_ids[0]
            self.in_use_jtag_id = TRUE
            return None

    
    def set_oem_id_and_oem_product_id(self = None, oem_id = None, oem_product_id = None):
        if oem_id is not None:
            self.oem_id = oem_id
        else:
            self.oem_id_independent = TRUE
        if oem_product_id is not None:
            self.oem_product_id = oem_product_id
            return None
        self.oem_product_id_independent = None

    
    def get_oem_product_id_bound(self = None):
        return not (self.oem_product_id_independent)

    __classcell__ = None

