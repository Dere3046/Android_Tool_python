
from abc import ABC, abstractmethod
from common.parser.hash_segment.defines import AUTHORITY_OEM
from profile.schema import ELFProperties, FuseBlowing, HashTableSegmentProperties, ImageFormat, LegacyDebugging, LicenseManagerSegmentProperties, MBNProperties, SecDatProperties, SecELFProperties, VouchSegmentProperties
ELF_PROPERTIES = 'elf_properties'
HASH_TABLE_SEGMENT_PROPERTIES = 'hash_table_segment_properties'
MBN_PROPERTIES = 'mbn_properties'
VOUCH_SEGMENT_PROPERTIES = 'vouch_segment_properties'
SEC_ELF_PROPERTIES = 'sec_elf_properties'
SEC_DAT_PROPERTIES = 'sec_dat_properties'
LICENSE_MANAGER_SEGMENT_PROPERTIES = 'license_manager_segment_properties'
ImageProperties = dict[(str, ELFProperties | HashTableSegmentProperties | LicenseManagerSegmentProperties | MBNProperties | VouchSegmentProperties | SecELFProperties | SecDatProperties)]
ImageFormatType = list[ImageFormat | FuseBlowing | LegacyDebugging]

class ImageInfoInterface(ABC):
    
    def get_image_format(self = None, authority = None):
        pass

    get_image_format = None(get_image_format)

