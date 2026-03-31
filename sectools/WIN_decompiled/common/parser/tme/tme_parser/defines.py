
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Optional
Tag = namedtuple('Tag', 'tag_symbol tag_id parser_class tag_name tag_type tag_group')
DEBUG_POLICY_DATA_PATH = '/SvcDebugPolicy/DebugPolicyData'
SIGNATURE_PATH = '/SvcDebugPolicy/Signature'
DEBUG_VECTOR_PATH = f'''{DEBUG_POLICY_DATA_PATH}/DebugVector'''
FINGERPRINT_HASH_VALUE_PATH = f'''{DEBUG_POLICY_DATA_PATH}/FingerprintHashValue'''
DP_CHIP_CONSTRAINTS_PATH = f'''{DEBUG_POLICY_DATA_PATH}/ChipConstraints'''
DEBUG_OPTIONS_PATH = f'''{DEBUG_POLICY_DATA_PATH}/DebugOptions'''
TEST_SIGNED_IMAGE_HASH_LIST_PATH = f'''{DEBUG_POLICY_DATA_PATH}/TestSignedImageHashList'''
OEM_TEST_ROOT_CA_HASH_VALUES_PATH = f'''{DEBUG_POLICY_DATA_PATH}/OemTestRootCaHashValues'''
OEM_CRASH_DUMP_PUBLIC_KEY_PATH = f'''{DEBUG_POLICY_DATA_PATH}/OemCrashDumpPublicKey'''
TEST_SIGNED_IMAGE_VECTOR_PATH = f'''{DEBUG_POLICY_DATA_PATH}/TestSignedImageVector'''
OEM_BATCH_KEY_HASH_PATH = f'''{DP_CHIP_CONSTRAINTS_PATH}/OemBatchKeyHash'''
CHIP_UNIQUE_IDENTIFIER_PATH = f'''{DP_CHIP_CONSTRAINTS_PATH}/ChipUniqueIdentifier'''
OEM_RC_HASH_PATH = f'''{DP_CHIP_CONSTRAINTS_PATH}/OemRcHash'''
HASH_VALUES_PATH = f'''{TEST_SIGNED_IMAGE_HASH_LIST_PATH}/HashValues'''
ENTITLEMENT_CERTIFICATE_PATH = 'SvcDebugPolicy/EntitlementCertificate'
DEBUG_ENTITLEMENT_PATH = f'''{ENTITLEMENT_CERTIFICATE_PATH}/Entitlements/DebugEntitlement'''
AUTHORIZED_DEBUG_VECTOR_PATH = f'''{DEBUG_ENTITLEMENT_PATH}/AuthorizedDebugVector'''
AUTHORIZED_DEBUG_OPTIONS_PATH = f'''{DEBUG_ENTITLEMENT_PATH}/AuthorizedDebugOptions'''
DEC_CHIP_CONSTRAINTS_PATH = f'''{DEBUG_ENTITLEMENT_PATH}/ChipConstraints'''
INSTANTIATION_CONSTRAINTS_PATH = f'''{DEBUG_ENTITLEMENT_PATH}/InstantiationConstraints'''
COMMAND_ENTITLEMENT_PATH = 'EntitlementCertificate/Entitlements/CommandEntitlement'
COMMAND_ENTITLEMENT_INSTANTIATION_CONSTRAINTS_PATH = f'''{COMMAND_ENTITLEMENT_PATH}/InstantiationConstraints'''
COMMAND_ENTITLEMENT_CHIP_CONSTRAINTS_PATH = f'''{COMMAND_ENTITLEMENT_PATH}/ChipConstraints'''
COMMAND_ENTITLEMENT_PUBLIC_KEY_PATH = f'''{COMMAND_ENTITLEMENT_PATH}/PublicKey'''
COMMAND_ENTITLEMENT_CHIP_UNIQUE_IDENTIFIER_PATH = f'''{COMMAND_ENTITLEMENT_CHIP_CONSTRAINTS_PATH}/ChipUniqueIdentifier'''
COMMAND_ENTITLEMENT_SERIAL_NUMBER_PATH = f'''{COMMAND_ENTITLEMENT_CHIP_UNIQUE_IDENTIFIER_PATH}/SerialNumber'''
IS_CHIP_UNIQUE_ID_BOUND = 'IS_CHIP_UNIQUE_ID_BOUND'

class TagList(list):
    """The list that knows about it's content - Tag objects."""
    
    def append(self = None, tag = None):
        if tag.tag_id in (lambda .0: [ i.tag_id for i in .0 ])(self):
            raise RuntimeError(f'''The TME spec requires the tag id\'s to be unique, however, duplicates detected: {tag.tag_id}''')
        None().append(tag)

    __classcell__ = None

SharedState = dataclass(<NODE:12>)
