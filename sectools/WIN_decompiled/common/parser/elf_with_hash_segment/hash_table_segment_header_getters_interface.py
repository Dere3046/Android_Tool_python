
from abc import ABC, abstractmethod

class HashTableSegmentHeaderGettersInterface(ABC):
    
    def get_software_id(self = None, authority = None):
        '''Returns the Software ID from either Metadata or OU fields. Returns None if the field does not exist.'''
        pass

    get_software_id = None(get_software_id)
    
    def get_secondary_software_id(self = None, authority = None):
        '''
        Returns the Secondary Software ID from either Metadata or OU fields. Returns None if the field does not exist.
        '''
        pass

    get_secondary_software_id = None(get_secondary_software_id)
    
    def get_mrc_index(self = None, authority = None, root_certificates = abstractmethod):
        '''
        Returns the MRC index from either Metadata, OU fields or active root certificate. Returns None if the field
        does not exist.
        '''
        pass

    get_mrc_index = None(get_mrc_index)
    
    def get_root_revoke_activate_enable(self = None, authority = None):
        '''
        Returns Root Revoke Activate Enable value from either Metadata or OU fields. Returns False if the field does
        not exist.
        '''
        pass

    get_root_revoke_activate_enable = None(get_root_revoke_activate_enable)
    
    def get_hash_table_algorithm(self = None):
        '''
        Returns the int value describing the Hash Table algorithm used to generate the Hash Table Segment. Returns None
        if the field does not exist.
        '''
        pass

    get_hash_table_algorithm = None(get_hash_table_algorithm)
    
    def get_oem_id(self = None, authority = None):
        '''
        Returns the OEM ID from either Metadata or OU fields. Returns None if the field does not exist or if
        the image is not bound to the OEM ID.
        '''
        pass

    get_oem_id = None(get_oem_id)
    
    def get_oem_product_id(self = None, authority = None):
        '''
        Returns the OEM Product ID from either Metadata or OU fields. Returns None if the field does not exist or if
        the image is not bound to the OEM Product ID.
        '''
        pass

    get_oem_product_id = None(get_oem_product_id)
    
    def get_soc_hw_versions(self = None, authority = None):
        '''
        Returns the SoC HW Versions from either Metadata or OU fields. Returns None if the field does not exist or if
        the image is not bound to any SoC HW Versions.
        '''
        pass

    get_soc_hw_versions = None(get_soc_hw_versions)

