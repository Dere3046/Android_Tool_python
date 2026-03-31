
from typing import Dict, List, Tuple
from common.data.binary_struct import StructBase
from common.data.data import get_lsb, hex_val
from common.parser.fuse_validator_payload.defines import DEFAULT_OPERATION_ID, FEATURE_ID_INT_TO_DESCRIPTION, FEATURE_ID_MASK, FEATURE_TYPE_COMPARISON, FEATURE_TYPE_INT_TO_DESCRIPTION, FEATURE_TYPE_MASK, OFF_TARGET_FEATURE_ID, ON_TARGET_FEATURE_ID
from common.parser.fuse_validator_payload.payload_request.defines import NO_RESPONSE_PAYLOAD_SIZE, QUERY_TZ_FOR_PAYLOAD_SIZE, RESPONSE_PAYLOAD_SIZE_INT_TO_DESCRIPTION, VALID_RESPONSE_ACTUAL_PAYLOAD_SIZE

class FuseValidatorPayloadRequestHeader(StructBase):
    feature_id: int = 'FuseValidatorPayloadRequestHeader'
    
    def get_fields(cls = None):
        return [
            'operation_id',
            'total_packet_size',
            'response_payload_size',
            'response_payload_size_type']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'operation_id': DEFAULT_OPERATION_ID,
            'total_packet_size': cls.get_size(),
            'response_payload_size': 0,
            'response_payload_size_type': VALID_RESPONSE_ACTUAL_PAYLOAD_SIZE }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '<IIHH'

    get_format = None(get_format)
    
    def unpack_post_process(self = None):
        self.feature_type = (self.operation_id & FEATURE_TYPE_MASK) >> get_lsb(FEATURE_TYPE_MASK)
        self.feature_id = (self.operation_id & FEATURE_ID_MASK) >> get_lsb(FEATURE_ID_MASK)

    
    def pack_pre_process(self = None):
        self.operation_id = self.feature_id << get_lsb(FEATURE_ID_MASK) | self.feature_type << get_lsb(FEATURE_TYPE_MASK)

    
    def validate_critical_fields(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def validate(self = None):
        self.validate_critical_fields()

    
    def get_properties(self = None):
        return [
            ('Feature Type:', FEATURE_TYPE_INT_TO_DESCRIPTION.get(self.feature_type, hex_val(self.feature_type, 4, **('num_chars',)))),
            ('Feature ID:', FEATURE_ID_INT_TO_DESCRIPTION.get(self.feature_id, hex_val(self.feature_id, 4, **('num_chars',)))),
            ('Total Packet Size:', f'''{self.total_packet_size} (bytes)'''),
            ('Response Payload Size Type:', RESPONSE_PAYLOAD_SIZE_INT_TO_DESCRIPTION.get(self.response_payload_size_type, hex_val(self.response_payload_size_type, 4, **('num_chars',)))),
            ('Response Payload Size:', f'''{self.response_payload_size} (bytes)''')]


