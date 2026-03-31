
from __future__ import annotations
import abc
import ipaddress
import typing
from email.utils import parseaddr
from cryptography.x509.name import Name
from cryptography.x509.oid import ObjectIdentifier
_IPAddressTypes = typing.Union[(ipaddress.IPv4Address, ipaddress.IPv6Address, ipaddress.IPv4Network, ipaddress.IPv6Network)]

class UnsupportedGeneralNameType(Exception):
    pass

GeneralName = <NODE:27>((lambda : 
def value(self = None):
'''
        Return the value of the object
        '''
passvalue = None(None(value))), 'GeneralName', abc.ABCMeta, **('metaclass',))

class RFC822Name(GeneralName):
    
    def __init__(self = None, value = None):
        pass
    # WARNING: Decompyle incomplete

    
    def value(self = None):
        return self._value

    value = None(value)
    
    def _init_without_validation(cls = None, value = None):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    _init_without_validation = None(_init_without_validation)
    
    def __repr__(self = None):
        return f'''<RFC822Name(value={self.value!r})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, RFC822Name):
            return NotImplemented
        return None.value == other.value

    
    def __hash__(self = None):
        return hash(self.value)



class DNSName(GeneralName):
    
    def __init__(self = None, value = None):
        pass
    # WARNING: Decompyle incomplete

    
    def value(self = None):
        return self._value

    value = None(value)
    
    def _init_without_validation(cls = None, value = None):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    _init_without_validation = None(_init_without_validation)
    
    def __repr__(self = None):
        return f'''<DNSName(value={self.value!r})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, DNSName):
            return NotImplemented
        return None.value == other.value

    
    def __hash__(self = None):
        return hash(self.value)



class UniformResourceIdentifier(GeneralName):
    
    def __init__(self = None, value = None):
        pass
    # WARNING: Decompyle incomplete

    
    def value(self = None):
        return self._value

    value = None(value)
    
    def _init_without_validation(cls = None, value = None):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    _init_without_validation = None(_init_without_validation)
    
    def __repr__(self = None):
        return f'''<UniformResourceIdentifier(value={self.value!r})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, UniformResourceIdentifier):
            return NotImplemented
        return None.value == other.value

    
    def __hash__(self = None):
        return hash(self.value)



class DirectoryName(GeneralName):
    
    def __init__(self = None, value = None):
        if not isinstance(value, Name):
            raise TypeError('value must be a Name')
        self._value = None

    
    def value(self = None):
        return self._value

    value = None(value)
    
    def __repr__(self = None):
        return f'''<DirectoryName(value={self.value})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, DirectoryName):
            return NotImplemented
        return None.value == other.value

    
    def __hash__(self = None):
        return hash(self.value)



class RegisteredID(GeneralName):
    
    def __init__(self = None, value = None):
        if not isinstance(value, ObjectIdentifier):
            raise TypeError('value must be an ObjectIdentifier')
        self._value = None

    
    def value(self = None):
        return self._value

    value = None(value)
    
    def __repr__(self = None):
        return f'''<RegisteredID(value={self.value})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, RegisteredID):
            return NotImplemented
        return None.value == other.value

    
    def __hash__(self = None):
        return hash(self.value)



class IPAddress(GeneralName):
    
    def __init__(self = None, value = None):
        if not isinstance(value, (ipaddress.IPv4Address, ipaddress.IPv6Address, ipaddress.IPv4Network, ipaddress.IPv6Network)):
            raise TypeError('value must be an instance of ipaddress.IPv4Address, ipaddress.IPv6Address, ipaddress.IPv4Network, or ipaddress.IPv6Network')
        self._value = None

    
    def value(self = None):
        return self._value

    value = None(value)
    
    def _packed(self = None):
        if isinstance(self.value, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            return self.value.packed
        return None.value.network_address.packed + self.value.netmask.packed

    
    def __repr__(self = None):
        return f'''<IPAddress(value={self.value})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, IPAddress):
            return NotImplemented
        return None.value == other.value

    
    def __hash__(self = None):
        return hash(self.value)



class OtherName(GeneralName):
    
    def __init__(self = None, type_id = None, value = None):
        if not isinstance(type_id, ObjectIdentifier):
            raise TypeError('type_id must be an ObjectIdentifier')
        if not None(value, bytes):
            raise TypeError('value must be a binary string')
        self._type_id = None
        self._value = value

    
    def type_id(self = None):
        return self._type_id

    type_id = None(type_id)
    
    def value(self = None):
        return self._value

    value = None(value)
    
    def __repr__(self = None):
        return f'''<OtherName(type_id={self.type_id}, value={self.value!r})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, OtherName):
            return NotImplemented
        if None.type_id == other.type_id:
            pass
        return self.value == other.value

    
    def __hash__(self = None):
        return hash((self.type_id, self.value))


