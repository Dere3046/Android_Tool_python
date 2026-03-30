
from cmd_line_interface.base_defines import KWARGS_HELP, KWARGS_NARGS, KWARGS_TYPE
from cmd_line_interface.basecmdline import CMDLineGroup
from cmd_line_interface.sectools.cmd_line_common.defines import OEM_TEST_ROOT_CERTIFICATE_HASH, QTI, sha256_sha384_sha512_hash
from cmd_line_interface.sectools.metadata import CONSUMES, INCOMPATIBLE_WITH
from common.parser.tme.tme_parser.defines import OEM_TEST_ROOT_CA_HASH_VALUES_PATH
OEM_TEST_ROOT_CERTIFICATE_HASH_HELP = 'Specify one or more SHA384 or SHA512 OEM root certificate hash strings. They provide alternative roots of trust when authenticating OEM-signed images. The maximum number of supported hashes depends on the Security Profile.'
OEM_TEST_SIGNED_IMAGES_GROUP = 'OEM Test Signed Images'
TME_OEM_TEST_SIGNING_GROUP: CMDLineGroup = [
    ([
        OEM_TEST_ROOT_CERTIFICATE_HASH], {
        KWARGS_HELP: OEM_TEST_ROOT_CERTIFICATE_HASH_HELP,
        KWARGS_TYPE: sha256_sha384_sha512_hash,
        KWARGS_NARGS: '+' }, {
        INCOMPATIBLE_WITH: [
            QTI],
        CONSUMES: [
            OEM_TEST_ROOT_CA_HASH_VALUES_PATH,
            f'''{OEM_TEST_ROOT_CA_HASH_VALUES_PATH}/HashArray''',
            f'''{OEM_TEST_ROOT_CA_HASH_VALUES_PATH}/HashAlgorithmIdentifier'''] })]
