
from cmd_line_interface.base_defines import AutoCloseFileType, DYNAMIC_HELP_PLURAL, KWARGS_HELP, KWARGS_NARGS, KWARGS_READ_BINARY, KWARGS_TYPE
from cmd_line_interface.basecmdline import CMDLineGroup
from cmd_line_interface.sectools.cmd_line_common.defines import QTI, SECURITY_PROFILE
from cmd_line_interface.sectools.metadata import CONSUMES, DEPENDS_ON
from common.parser.tme.tme_parser.defines import HASH_VALUES_PATH, TEST_SIGNED_IMAGE_HASH_LIST_PATH
ENABLE_TEST_SIGNED = '--enable-test-signed'
ENABLE_TEST_SIGNED_HELP = 'File path of one or more QTI test-signed binaries for which to enable authentication. Binaries can be ELF with v7 Hash Table Segment or Image Authentication Request (IAR).'
QTI_TEST_SIGNED_IMAGES_GROUP = 'QTI Test Signed Images'
QTI_TEST_SIGNED_IMAGES_GROUP_HELP = f'''All options must be used with {QTI}. Some QTI test signing {DYNAMIC_HELP_PLURAL}'''

def software_image_id_to_cmd_argument_name(software_image_id = None):
    '''Defines the naming conversion from the SW ID id to the CMD argument.'''
    return f'''{ENABLE_TEST_SIGNED}-{software_image_id.replace('_SS_SWID', '').replace('_', '-').lower()}'''

TME_QTI_TEST_SIGNING_GROUP: CMDLineGroup = [
    ([
        ENABLE_TEST_SIGNED], {
        KWARGS_HELP: ENABLE_TEST_SIGNED_HELP,
        KWARGS_NARGS: '+',
        KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) }, {
        DEPENDS_ON: [
            QTI,
            SECURITY_PROFILE],
        CONSUMES: [
            TEST_SIGNED_IMAGE_HASH_LIST_PATH,
            HASH_VALUES_PATH,
            f'''{HASH_VALUES_PATH}/HashAlgorithmIdentifier''',
            f'''{HASH_VALUES_PATH}/HashArray''',
            f'''{TEST_SIGNED_IMAGE_HASH_LIST_PATH}/BootSubsystemSoftwareComponentIdentifier'''] })]
