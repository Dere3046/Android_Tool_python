
from typing import Any, List, Tuple
from common.crypto.openssl.defines import ALGORITHM_ECDSA, CURVE_ASN1_TO_NORMALIZED_ASN1_NIST
from common.crypto.openssl.openssl import extract_signature_format_from_key, generate_signature, get_text_from_key
from common.data.data import and_separated
from common.parser.tme.dpr.dpr import DPR
from common.parser.tme.dpr.validations import TMEItemError
from common.parser.tme.tme_parser.defines import SIGNATURE_PATH
from core.tme_secure_debug.signer.plugin.tme_plugin_signer import invoke_plugin_sign
from core.tme_secure_debug.tme_signing_algorithm_details import tme_signing_algorithm_details
from profile.profile_core import SecurityProfile
from public.tme_signable import TMESignable

def _sign(tme = None, allowed_algorithm_ids = None, security_profile = None, plugin_signer_args = ('tme', TMESignable, 'allowed_algorithm_ids', List[str], 'plugin_signer_args', Any, 'return', Tuple[(str, bytes)])):
    '''
    The generic local signer for TMESignable objects which implements the plugin signer API.
    Note: Supports any TME object implementing TMESignable interface but has only been tested with DPR.
    '''
    pass
# WARNING: Decompyle incomplete


def local_sign(dpr = None, security_profile = None, attestation_private_key = None):
    '''
    The DPR local signer. Returns a new TME object.
    Expects attestation_private_key in either PEM/DER format.
    @return new signed DPR object.
    '''
    ret = invoke_plugin_sign(dpr, security_profile, _sign, attestation_private_key)
# WARNING: Decompyle incomplete

