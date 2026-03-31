
from typing import Any
from cmd_line_interface.sectools.cmd_line_common.defines import PLATFORM_BINDING, SOC_FEATURE_ID
from common.data.data import hex_val
from common.parser.elf_with_hash_segment.v7.metadata.defines import FALSE, METADATA_MAJOR_VERSION_3, TRUE
from common.parser.elf_with_hash_segment.v7.metadata.v2_0.metadata_2_0 import MetadataV20

class MetadataV30(MetadataV20):
    MAJOR_VERSION: int = METADATA_MAJOR_VERSION_3
    FLAGS: list[tuple[(int, str, str)]] = list(MetadataV20.FLAGS)
    FLAGS[1] = (12, 'product_segment_id_bound', 'Bound to Product Segment ID')
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.product_segment_id = 0
        self.product_segment_id_bound = FALSE
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        fields = list(MetadataV20.get_fields())
        fields[fields.index('soc_feature_id')] = 'product_segment_id'
        return fields

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_properties(self = None):
        properties = super().get_properties()
        index = next((lambda .0: for description, _ in .0:
if description == 'SoC Feature ID:':
indexcontinueNone)(enumerate(properties)))
        properties[index] = ('Product Segment ID:', hex_val(self.product_segment_id, True, **('strip_leading_zeros',)))
        return properties

    
    def set_platform_binding(self, soc_hw_versions = None, soc_feature_ids = None, jtag_ids = None, product_segment_ids = ('soc_hw_versions', list[int], 'soc_feature_ids', list[int], 'jtag_ids', list[int], 'product_segment_ids', list[int], 'return', None)):
        if soc_feature_ids:
            raise RuntimeError(f'''{PLATFORM_BINDING} {SOC_FEATURE_ID} is not supported for {self.METADATA_STR} Version {self.major_version}.{self.minor_version}.''')
        if None:
            self.validate_soc_hw_vers(soc_hw_versions)
            self.soc_hw_vers = soc_hw_versions
            self.soc_hw_version_bound = TRUE
        if jtag_ids:
            self.jtag_id = jtag_ids[0]
            self.jtag_id_bound = TRUE
        if product_segment_ids:
            self.product_segment_id = product_segment_ids[0]
            self.product_segment_id_bound = TRUE
            return None

    __classcell__ = None

