
from typing import NamedTuple
from profile.schema.v1_3.profile_parser import fuse_region as FuseRegionV13, sec_dat_properties as SecDatPropertiesV13, sec_elf_properties as SecELFPropertiesV13
from profile.schema.v1_4.profile_parser import fuse_region as FuseRegionV14, sec_dat_properties as SecDatPropertiesV14, sec_elf_properties as SecELFPropertiesV14
from profile.schema.v1_5.profile_parser import fuse_region as FuseRegionV15, sec_dat_properties as SecDatPropertiesV15, sec_elf_properties as SecELFPropertiesV15
from profile.schema.v1_6.profile_parser import fuse_region as FuseRegionV16, sec_dat_properties as SecDatPropertiesV16, sec_elf_properties as SecELFPropertiesV16
IGNORED_FUSE = [
    'reserved for qti use. do not blow.',
    'reserved',
    'do not blow',
    'unused']
SecELFProperties = SecELFPropertiesV13 | SecELFPropertiesV14 | SecELFPropertiesV15 | SecELFPropertiesV16
SecDatProperties = SecDatPropertiesV13 | SecDatPropertiesV14 | SecDatPropertiesV15 | SecDatPropertiesV16
FuseRegion = FuseRegionV13 | FuseRegionV14 | FuseRegionV15 | FuseRegionV16
FUSE_NAME = 'FUSE NAME'
FUSE_ADDRESS = 'FUSE ADDRESS'
FUSE_BIT_NUMBER = 'FUSE BIT NUMBER'
FUSE_BLOW_VALUE = 'FUSE BLOW VALUE'
QUALCOMM_RECOMMENDATION_VS_OEM_CHOICE = 'QUALCOMM RECOMMENDATION VS OEM CHOICE'
FUSE_COMMENTS = 'FUSE COMMENTS'
FUSE_GROUPS = 'FUSE GROUPS'
QUALCOMM_RECOMMENDATION = 'QUALCOMM RECOMMENDATION'
OEM_VALUE_QFPROM = 'OEM VALUE'
OEM_VALUE_XML = 'OEM_VALUE'
ColumnNames = NamedTuple('ColumnNames', [
    ('fuse_name', str),
    ('fuse_address', str),
    ('fuse_comments', str),
    ('fuse_blow_value', str),
    ('qualcomm_recommendation_vs_oem_choice', str),
    ('groups', str)])
