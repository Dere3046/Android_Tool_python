
import profile
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.base_defines import ENCRYPT_THEN_SIGN, SIGN
from cmd_line_interface.sectools.secure_image.defines import ENCRYPT, ENCRYPTION_ORDER
from common.parser.hash_segment.defines import AUTHORITY_QTI
from common.parser.hash_segment.hash_segment_common import HashTableSegmentCommon
from common.parser.mdt.mdt import MDT
from core.profile_validator.defines import ENCRYPTED_THEN_SIGNED, QBEC, SIGNED_THEN_ENCRYPTED
from core.secure_image.encrypter.utils import validate_encryption_order_arguments_against_encryption_type

def get_order_of_operations(parsed_args = None, authority = None):
    '''
    Returns the order in which to perform the hash/sign and encrypt operations regardless of authority. Whether the
    operation is actually to be performed is checked downstream.
    '''
    operations_order = SIGNED_THEN_ENCRYPTED
# WARNING: Decompyle incomplete


def validate_infile_type_against_current_operations(parsed_args = None, authority = None, parsed_image = None, operations_order = ('parsed_args', NamespaceWithGet, 'authority', str, 'parsed_image', MDT | HashTableSegmentCommon, 'operations_order', str, 'return', None)):
    operation_string = 'encrypt then sign' if parsed_args.get(SIGN) else 'encrypt'
# WARNING: Decompyle incomplete


def get_augmented_error_string(parsed_args = None):
    if parsed_args.get(ENCRYPTION_ORDER):
        error = f'''Check argument {ENCRYPTION_ORDER}.'''
        return error
    if None.get(ENCRYPT_THEN_SIGN):
        error = f'''Remove {ENCRYPT_THEN_SIGN} from the command.'''
        return error
    error = f'''{ENCRYPTION_ORDER}.'''
    return error

