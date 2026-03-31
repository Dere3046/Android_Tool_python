
from __future__ import annotations
import re
from typing import NewType, cast
from packaging.licenses._spdx import EXCEPTIONS, LICENSES
__all__ = [
    'InvalidLicenseExpression',
    'NormalizedLicenseExpression',
    'canonicalize_license_expression']
license_ref_allowed = re.compile('^[A-Za-z0-9.-]*$')
NormalizedLicenseExpression = NewType('NormalizedLicenseExpression', str)

class InvalidLicenseExpression(ValueError):
    '''Raised when a license-expression string is invalid

    >>> canonicalize_license_expression("invalid")
    Traceback (most recent call last):
        ...
    packaging.licenses.InvalidLicenseExpression: Invalid license expression: \'invalid\'
    '''
    pass


def canonicalize_license_expression(raw_license_expression = None):
    if not raw_license_expression:
        message = f'''Invalid license expression: {raw_license_expression!r}'''
        raise InvalidLicenseExpression(message)
    license_expression = None.replace('(', ' ( ').replace(')', ' ) ')
    licenseref_prefix = 'LicenseRef-'
    license_refs = (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(license_expression.split())
    license_expression = license_expression.lower()
    tokens = license_expression.split()
    python_tokens = []
    for token in tokens:
        if token not in frozenset({'or', ')', 'and', '(', 'with'}):
            python_tokens.append('False')
            continue
        if token == 'with':
            python_tokens.append('or')
            continue
        if token == '(' and python_tokens and python_tokens[-1] not in frozenset({'or', 'and'}):
            message = f'''Invalid license expression: {raw_license_expression!r}'''
            raise InvalidLicenseExpression(message)
        None.append(token)
    python_expression = ' '.join(python_tokens)
# WARNING: Decompyle incomplete

