
from operator import attrgetter
from typing import Iterable, List, NamedTuple
from common.crypto.openssl.defines import CURVE_NIST_TO_ASN1, SIGNATURE_DESCRIPTION_TO_SIZE, SignatureDescription
from common.data.data import and_separated, plural_s
from common.parser.tme.tme_parser.tme import get_selections_for_tag

class SigningAlgorithm(NamedTuple):
    min_signature_size: int = 'SigningAlgorithm'


def tme_signing_algorithm_details(algorithm_ids = None):
    '''
    A helper function that extracts the supported TME ECDSA curves and corresponding hash algorithms
    (defined by TME protocol).
    @return a list (of at least one) SigningAlgorithm items (never empty list). Or throw.
    '''
    allowed_algorithm_names = sorted(get_selections_for_tag('AlgorithmIdentifier') - {
        'NONE'})
# WARNING: Decompyle incomplete

