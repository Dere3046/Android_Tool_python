
import re
from typing import cast
from lxml import etree
from lxml.etree import XMLSyntaxError
from cmd_line_interface.base_defines import auto_close_xml_type
from cmd_line_interface.sectools.defines import SECTOOLS_DESCRIPTION, SECTOOLS_VERSION
from common.data.data import and_separated, version_string_to_tuple
from profile import profile_version_parser
from profile.defines import SCHEMA_VERSIONS, SCHEMA_VERSION_PARSER_SCHEMA_LOCATION
from profile.schema import Profile

def validate_versions(parsed_profile = None):
    if not parsed_profile.minimum_sectools_version:
        raise RuntimeError('Security Profile is missing required attribute minimum_sectools_version.')
    if not None.schema_version:
        raise RuntimeError('Security Profile is missing required attribute schema_version.')
    if None(parsed_profile.minimum_sectools_version) > SECTOOLS_VERSION:
        raise RuntimeError(f'''{SECTOOLS_DESCRIPTION} does not meet version required by the Security Profile. Minimum required version is {parsed_profile.minimum_sectools_version}.''')
    if None(parsed_profile.schema_version) not in SCHEMA_VERSIONS:
        schema_versions = (lambda .0: [ '.'.join(map(str, schema_version)) for schema_version in .0 ])(SCHEMA_VERSIONS)
        raise RuntimeError(f'''Security Profile of schema version {parsed_profile.schema_version} is not supported. Supported schema versions are {and_separated(schema_versions)}.''')


def parse_security_profile(security_profile_data = None):
    pass
# WARNING: Decompyle incomplete

auto_close_security_profile_type = auto_close_xml_type(parse_security_profile)
