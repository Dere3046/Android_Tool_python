
from profile.schema.v1_0.profile_parser import profile as ProfileV10
from profile.schema.v1_1.profile_parser import profile as ProfileV11
from profile.schema.v1_2.profile_parser import profile as ProfileV12
from profile.schema.v1_3.profile_parser import profile as ProfileV13
from profile.schema.v1_4.profile_parser import profile as ProfileV14
from profile.schema.v1_5.profile_parser import profile as ProfileV15
from profile.schema.v1_6.profile_parser import profile as ProfileV16
from profile.schema.v1_7.profile_parser import profile as ProfileV17
from profile.schema.v1_8 import profile_parser
from profile.schema.v1_8.profile_parser import authenticator, elf_properties, encryption_features, encryption_format, fuse_blowing, fuse_region, fuse_row, hash_table_segment_metadata_versions, hash_table_segment_placements, hash_table_segment_properties, image, image_format, image_formats, jtag_id, jtag_ids, legacy, license_manager_segment_placements, license_manager_segment_properties, mbn_metadata_versions, mbn_properties, mrc_specs, platform_binding_values, product_segment_id, product_segment_ids, profile as ProfileV18, sec_dat_properties, sec_elf_properties, segment_hash_algorithms, serial_bound_feature, signature_format, signature_formats, signing_features, soc_feature_id, soc_feature_ids, soc_hw_version, soc_hw_versions, supported_encryption_formats, tme, tme_elf_properties, vouch_segment_placements, vouch_segment_properties
Profile = ProfileV10 | ProfileV11 | ProfileV12 | ProfileV13 | ProfileV14 | ProfileV15 | ProfileV16 | ProfileV17 | ProfileV18
ProcessedProfile = ProfileV18
ProfileParser = profile_parser
Authenticator = authenticator
ELFProperties = elf_properties
EncryptionFeatures = encryption_features
EncryptionFormat = encryption_format
FuseBlowing = fuse_blowing
FuseRegion = fuse_region
FuseRow = fuse_row
HashTableSegmentMetadataVersions = hash_table_segment_metadata_versions
HashTableSegmentPlacements = hash_table_segment_placements
HashTableSegmentProperties = hash_table_segment_properties
Image = image
ImageFormat = image_format
ImageFormats = image_formats
JtagID = jtag_id
JtagIDs = jtag_ids
LegacyDebugging = legacy
licenseManagerSegmentPlacements = license_manager_segment_placements
LicenseManagerSegmentProperties = license_manager_segment_properties
MBNMetadataVersions = mbn_metadata_versions
MBNProperties = mbn_properties
MRCSpecs = mrc_specs
PlatformBindings = platform_binding_values
ProductSegmentID = product_segment_id
ProductSegmentIDs = product_segment_ids
SecDatProperties = sec_dat_properties
SecELFProperties = sec_elf_properties
SegmentHashAlgorithms = segment_hash_algorithms
SerialBoundFeature = serial_bound_feature
SignatureFormat = signature_format
SignatureFormats = signature_formats
SigningFeatures = signing_features
SocFeatureID = soc_feature_id
SocFeatureIDs = soc_feature_ids
SocHWVersion = soc_hw_version
SocHWVersions = soc_hw_versions
SupportedEncryptionFormats = supported_encryption_formats
TMEDebugging = tme
TMEELFProperties = tme_elf_properties
VouchSegmentPlacements = vouch_segment_placements
VouchSegmentProperties = vouch_segment_properties
