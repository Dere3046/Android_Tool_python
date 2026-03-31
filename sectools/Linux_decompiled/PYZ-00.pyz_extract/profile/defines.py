
from collections import namedtuple
from pathlib import Path
from common.utils import SECTOOLS_PATH
from profile.schema.v1_0 import profile_parser as parser_1_0
from profile.schema.v1_1 import profile_parser as parser_1_1
from profile.schema.v1_2 import profile_parser as parser_1_2
from profile.schema.v1_3 import profile_parser as parser_1_3
from profile.schema.v1_4 import profile_parser as parser_1_4
from profile.schema.v1_5 import profile_parser as parser_1_5
from profile.schema.v1_6 import profile_parser as parser_1_6
from profile.schema.v1_7 import profile_parser as parser_1_7
from profile.schema.v1_8 import profile_parser as parser_1_8
SCHEMA_VERSION_1_0 = (1, 0)
SCHEMA_VERSION_1_1 = (1, 1)
SCHEMA_VERSION_1_2 = (1, 2)
SCHEMA_VERSION_1_3 = (1, 3)
SCHEMA_VERSION_1_4 = (1, 4)
SCHEMA_VERSION_1_5 = (1, 5)
SCHEMA_VERSION_1_6 = (1, 6)
SCHEMA_VERSION_1_7 = (1, 7)
SCHEMA_VERSION_1_8 = (1, 8)
SCHEMA_VERSIONS = [
    SCHEMA_VERSION_1_0,
    SCHEMA_VERSION_1_1,
    SCHEMA_VERSION_1_2,
    SCHEMA_VERSION_1_3,
    SCHEMA_VERSION_1_4,
    SCHEMA_VERSION_1_5,
    SCHEMA_VERSION_1_6,
    SCHEMA_VERSION_1_7,
    SCHEMA_VERSION_1_8]
SchemaParser = namedtuple('SchemaParser', ('parser', 'schema_location'))
SCHEMA_VERSION_PARSER_SCHEMA_LOCATION = {
    SCHEMA_VERSION_1_8: SchemaParser(parser_1_8, Path(SECTOOLS_PATH) / 'profile/schema/v1_8/profile_1_8.xsd'),
    SCHEMA_VERSION_1_7: SchemaParser(parser_1_7, Path(SECTOOLS_PATH) / 'profile/schema/v1_7/profile_1_7.xsd'),
    SCHEMA_VERSION_1_6: SchemaParser(parser_1_6, Path(SECTOOLS_PATH) / 'profile/schema/v1_6/profile_1_6.xsd'),
    SCHEMA_VERSION_1_5: SchemaParser(parser_1_5, Path(SECTOOLS_PATH) / 'profile/schema/v1_5/profile_1_5.xsd'),
    SCHEMA_VERSION_1_4: SchemaParser(parser_1_4, Path(SECTOOLS_PATH) / 'profile/schema/v1_4/profile_1_4.xsd'),
    SCHEMA_VERSION_1_3: SchemaParser(parser_1_3, Path(SECTOOLS_PATH) / 'profile/schema/v1_3/profile_1_3.xsd'),
    SCHEMA_VERSION_1_2: SchemaParser(parser_1_2, Path(SECTOOLS_PATH) / 'profile/schema/v1_2/profile_1_2.xsd'),
    SCHEMA_VERSION_1_1: SchemaParser(parser_1_1, Path(SECTOOLS_PATH) / 'profile/schema/v1_1/profile_1_1.xsd'),
    SCHEMA_VERSION_1_0: SchemaParser(parser_1_0, Path(SECTOOLS_PATH) / 'profile/schema/v1_0/profile_1_0.xsd') }
START = 'START'
END = 'END'
ANY = 'ANY'
UNKNOWN = 'UNKNOWN'
SOC_HW_VERSIONS = 'soc_hw_versions'
JTAG_IDS = 'jtag_ids'
SOC_FEATURE_IDS = 'soc_feature_ids'
PRODUCT_SEGMENT_IDS = 'product_segment_ids'
# WARNING: Decompyle incomplete
