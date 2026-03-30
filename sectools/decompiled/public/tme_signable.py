
from abc import ABC, abstractmethod
from typing import Any

class TMESignable(ABC):
    '''This interface is implemented by signable TME objects (e.g., DPR) and is available for use with plugin signer.'''
    
    def get_signable_data(self = None, algorithm_id = None):
        '''
        Returns the binary data to sign. The signature is computed over a subset of the TME object\'s binary data rather
        than all of its data, hence the existence of this method. Requires the algorithm that will be used for signing
        as an argument (as the data generated will contain the algorithm id in it).

        Note: The method will make sure that the algorithm id is a valid algorithm identifier. However, the method will
        not verify it against the Security Profile. Therefore, the desired algorithm id should always be selected from
        the algorithm ids provided by the plugin signer "sign" function\'s "allowed_algorithm_ids" parameter.
        '''
        pass

    get_signable_data = None(get_signable_data)
    
    def get_signable_hash(self = None, algorithm_id = None):
        '''
        Returns the hash computed over the binary data to sign. Requires the algorithm that will be used for signing as
        an argument (as the data generated will contain the algorithm id in it, and the corresponding hash function
        will be used).

        Note: The method will make sure that the algorithm id is a valid algorithm identifier. However, the method will
        not verify it against the Security Profile. Therefore, the desired algorithm id should always be selected from
        the algorithm ids provided by the plugin signer "sign" function\'s "allowed_algorithm_ids" parameter.
        '''
        pass

    get_signable_hash = None(get_signable_hash)
    
    def describe(self = None):
        '''Returns a string describing the TME object.'''
        pass

    describe = None(describe)
    
    def get_item(self = None, json_pointer = None):
        '''
        Convenience method. Returns a TME item from TME object using JSON pointer string.
        Example: dpr.get_item("SvcDebugPolicy/DebugPolicyData/DebugOptions")
        '''
        pass

    get_item = None(get_item)
    
    def __repr__(self = None):
        '''The object is printable.'''
        pass

    __repr__ = None(__repr__)

