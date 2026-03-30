
from binascii import unhexlify
from copy import deepcopy
from inspect import signature
from operator import attrgetter
from pathlib import Path
from re import findall
from typing import Any, Callable
from common.crypto.openssl.openssl import get_asn1_text
from common.data.data import and_separated, plural_s
from common.data.defines import PAD_BYTE_0
from common.parser.tme.base_tme import BaseTME
from common.parser.tme.tme_parser.tme import TME
from common.parser.tme.tme_signable_interface import TMESignableInterface
from common.subprocess.subprocess import get_function_from_script
from core.tme_secure_debug.tme_signing_algorithm_details import tme_signing_algorithm_details
from profile.profile_core import SecurityProfile
SIGN_FUNCTION_SIGNATURE = '(tme: public.tme_signable.TMESignable, allowed_algorithm_ids: List[str], security_profile, plugin_signer_args: Any) -> Tuple[str, bytes]'
SIGN_FUNCTION_NAME = 'sign'

def plugin_sign(tme = None, security_profile = None, plugin_signer = None, plugin_signer_args = ('tme', TMESignableInterface, 'security_profile', SecurityProfile, 'plugin_signer', Path, 'plugin_signer_args', Any, 'return', BaseTME)):
    '''The DPR plugin signer.'''
    sign_function = get_function_from_script(plugin_signer, SIGN_FUNCTION_SIGNATURE, SIGN_FUNCTION_NAME)
    return invoke_plugin_sign(tme, security_profile, sign_function, plugin_signer_args)


def invoke_plugin_sign(tme = None, security_profile = None, plugin_signer_func = None, plugin_signer_args = ('tme', TMESignableInterface, 'security_profile', SecurityProfile, 'plugin_signer_func', Callable, 'plugin_signer_args', Any, 'return', BaseTME)):
    '''
    The generic plugin signer. Supports any TME object implementing TMESignable interface.
    Note: that is in theory, tested only with DPR so far.
    '''
    allowed_algorithm_ids = security_profile.tme_debugging_features.seq_signing_algorithms.supported_seq_signing_algorithms.value
# WARNING: Decompyle incomplete

