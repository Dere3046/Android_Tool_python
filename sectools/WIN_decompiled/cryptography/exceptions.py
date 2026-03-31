
from __future__ import annotations
import typing
from cryptography.hazmat.bindings._rust import exceptions as rust_exceptions
if typing.TYPE_CHECKING:
    from cryptography.hazmat.bindings._rust import openssl as rust_openssl
_Reasons = rust_exceptions._Reasons

class UnsupportedAlgorithm(Exception):
    
    def __init__(self = None, message = None, reason = None):
        super().__init__(message)
        self._reason = reason

    __classcell__ = None


class AlreadyFinalized(Exception):
    pass


class AlreadyUpdated(Exception):
    pass


class NotYetFinalized(Exception):
    pass


class InvalidTag(Exception):
    pass


class InvalidSignature(Exception):
    pass


class InternalError(Exception):
    
    def __init__(self = None, msg = None, err_code = None):
        super().__init__(msg)
        self.err_code = err_code

    __classcell__ = None


class InvalidKey(Exception):
    pass

