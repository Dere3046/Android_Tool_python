"""Hash table segment header implementation."""

from common.data.binary_struct import StructBase


class HashTableSegmentHeaderCommon(StructBase):
    """Hash table segment header common base."""

    STRUCT_FORMAT = '<IIIIIIIIII'
    STRUCT_FIELDS = (
        'reserved', 'version', 'common_metadata_size', 'qti_metadata_size',
        'oem_metadata_size', 'hash_table_size', 'qti_sig_size',
        'qti_cert_chain_size', 'oem_sig_size', 'oem_cert_chain_size',
    )

    def __init__(self, data=None, **kwargs):
        for field in self.STRUCT_FIELDS:
            setattr(self, field, 0)
        if data:
            self.unpack(data)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
