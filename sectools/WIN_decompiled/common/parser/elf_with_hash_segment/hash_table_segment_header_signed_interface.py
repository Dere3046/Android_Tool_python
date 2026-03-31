
from abc import ABC, abstractmethod

class HashTableSegmentHeaderSignedInterface(ABC):
    
    def is_unsigned(self = None):
        '''Returns True if an image contains neither OEM nor QTI signatures.'''
        pass

    is_unsigned = None(is_unsigned)
    
    def is_oem_exclusive_signed(self = None, contains_padding = None):
        '''Returns True if an image is OEM signed and cannot be QTI signed.'''
        pass

    is_oem_exclusive_signed = None(is_oem_exclusive_signed)
    
    def is_qti_exclusive_signed(self = None, contains_padding = None):
        '''Returns True if an image is QTI signed and cannot be OEM signed.'''
        pass

    is_qti_exclusive_signed = None(is_qti_exclusive_signed)
    
    def is_oem_signed_double_signable(self = None, contains_padding = None):
        '''Returns True if an image is OEM signed and can be QTI signed in the future.'''
        pass

    is_oem_signed_double_signable = None(is_oem_signed_double_signable)
    
    def is_qti_signed_double_signable(self = None, contains_padding = None):
        '''Returns True if an image is QTI signed and can be OEM signed in the future.'''
        pass

    is_qti_signed_double_signable = None(is_qti_signed_double_signable)
    
    def is_double_signed(self = None):
        '''Returns True if an image contains both OEM and QTI signatures.'''
        pass

    is_double_signed = None(is_double_signed)

