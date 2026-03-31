
from typing import Type
from common.data.base_parser import BaseParserGenerator
from common.data.data import properties_repr
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.data_encryption_parameters_common import DataEncryptionParametersCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.xts.data_encryption_parameters_header import DataEncryptionParametersHeaderXTS

class DataEncryptionParametersXTS(DataEncryptionParametersCommon, BaseParserGenerator):
    HEADER_CLASS: Type[DataEncryptionParametersHeaderXTS] = DataEncryptionParametersHeaderXTS
    
    def create_default(self = None, seed = None, **_):
        self.header = self.HEADER_CLASS.from_fields(seed, **('seed',))

    
    def __repr__(self = None):
        pass
    # WARNING: Decompyle incomplete


