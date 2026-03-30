
from cmd_line_interface.sectools.cmd_line_common.defines import ANTI_ROLLBACK_VERSION, OEM_ID, OEM_PRODUCT_ID, SERIAL_NUMBER, SOC_LIFECYCLE_STATE, TRANSFER_ROOT
from cmd_line_interface.sectools.secure_image.defines import FEATURE_ID, JTAG_DEBUG, OEM_ROOT_CERTIFICATE_HASH, SECONDARY_SOFTWARE_ID, TRANSFER_UIE_KEY
from profile.defines import JTAG_IDS, PRODUCT_SEGMENT_IDS, SOC_FEATURE_IDS, SOC_HW_VERSIONS
HASH_SEGMENT_V3 = 3
HASH_SEGMENT_V5 = 5
HASH_SEGMENT_V6 = 6
HASH_SEGMENT_V7 = 7
HASH_SEGMENT_V8 = 8
ATTESTATION = 0
CA = 1
ROOT = 2
ATTESTATION_DESCRIPTION = 'Attest'
CA_DESCRIPTION = 'CA'
ROOT_DESCRIPTION = 'Root'
CERTIFICATE_LEVEL_DESCRIPTION = {
    ROOT: ROOT_DESCRIPTION,
    CA: CA_DESCRIPTION,
    ATTESTATION: ATTESTATION_DESCRIPTION }
MRC_1_0 = '1.0'
MRC_2_0 = '2.0'
MRC_3_0 = '3.0'
LEGACY_MRC_1_0_MAX_NUM_ROOT_CERTIFICATES = 16
LEGACY_MRC_2_0_MAX_NUM_ROOT_CERTIFICATES = 4
LEGACY_MRC_3_0_MAX_NUM_ROOT_CERTIFICATES = 6
MRC_SPEC_TO_LEGACY_MAX_ROOT_CERTIFICATE_COUNT = {
    MRC_3_0: LEGACY_MRC_3_0_MAX_NUM_ROOT_CERTIFICATES,
    MRC_2_0: LEGACY_MRC_2_0_MAX_NUM_ROOT_CERTIFICATES,
    MRC_1_0: LEGACY_MRC_1_0_MAX_NUM_ROOT_CERTIFICATES }
AUTHORITY_QTI = 'QTI'
AUTHORITY_OEM = 'OEM'
PLATFORM_BINDING_DEVICE_RESTRICTIONS = [
    SOC_HW_VERSIONS,
    JTAG_IDS,
    SOC_FEATURE_IDS,
    PRODUCT_SEGMENT_IDS]
DEVICE_RESTRICTIONS = PLATFORM_BINDING_DEVICE_RESTRICTIONS + [
    SERIAL_NUMBER,
    OEM_ID,
    OEM_PRODUCT_ID,
    ANTI_ROLLBACK_VERSION,
    TRANSFER_ROOT,
    JTAG_DEBUG,
    SECONDARY_SOFTWARE_ID,
    FEATURE_ID,
    TRANSFER_UIE_KEY,
    OEM_ROOT_CERTIFICATE_HASH,
    SOC_LIFECYCLE_STATE]
PRODUCTION_ROOT_HASHES = [
    ('69:ac:b5:6b:82:89:4b:9a:1e:b3:45:ae:4c:15:25:12:0a:68:96:da:d5:27:27:e8c6:a0:fc:a9:aa:05:55:37:8f:39:04:62:b4:20:76:1e:73:cd:7c:07:65:70:d9:bf', 'Feature License Attestation Root CA'),
    ('03:ca:19:20:14:ae:cf:f1:99:9d:ed:56:90:01:ca:4a:3d:4f:e5:6c:04:b5:b4:6252:11:29:d2:78:4c:1c:28:f5:f3:77:95:5e:26:60:d7:64:82:6a:1f:e9:54:64:d4', 'Feature License Communication Root CA'),
    ('72:af:ad:7b:a5:ac:6c:e9:c8:6e:74:fb:4f:53:52:8e:b9:22:a8:a2:d0:1e:0f:4fe0:eb:ca:2a:09:a4:2a:ea:89:43:0f:e6:2b:83:1a:b4:86:e9:c5:bb:1a:8a:7c:80', 'QMC Attestation Root CA 2'),
    ('0e:6b:4f:06:e0:fd:84:4e:e0:3a:f5:c5:43:d2:70:42:e7:75:7e:63:77:96:d6:a3c8:59:86:f5:b9:8d:45:62:d4:62:97:80:49:31:dc:87:0d:88:35:d2:3a:80:6d:b7', 'QSEE Application Attestation Root'),
    ('be:18:44:cc:d9:78:d6:b1:e8:e0:20:be:98:23:7b:c9:1f:94:43:37:f3:c7:af:f0c2:30:42:76:ba:b8:35:c7:55:eb:7f:54:fa:05:4c:50:7d:ed:ea:3b:4b:24:06:eb', 'QSEE Attestation Root CA'),
    ('a4:cd:9b:b6:f5:d6:57:f8:47:ec:32:36:4d:3d:fc:ce:0e:9c:34:98:67:7f:e6:7d32:86:80:18:f5:76:32:d5:75:9f:d0:50:e5:8f:75:40:e6:a2:0d:5f:fe:fb:5d:a0', 'QSEE Communication Root CA'),
    ('a9:70:38:aa:9d:b2:18:d8:dd:38:d3:9f:a6:46:8c:de:1b:be:9a:1a:45:65:01:7725:59:78:e3:aa:b5:09:fc:e2:38:19:10:e3:92:cb:59:3d:c5:ab:10:3b:bd:75:84', 'SPSS Attestation Root CA'),
    ('88:b0:12:4e:06:0e:98:15:06:9f:7e:e4:e8:99:0b:2a:86:4a:dc:df:ca:a4:fb:e55f:8d:e4:8f:99:8e:ca:98:a0:79:33:51:76:61:74:33:97:18:ef:e3:d1:80:ac:d1', 'XBL Sec Attestation Root CA'),
    ('d4:0e:ee:56:f3:19:46:65:57:41:09:a3:92:67:72:4a:e7:94:41:34:cd:53:cb:767e:29:3d:3c:40:49:79:55:bc:8a:45:19:ff:99:2b:03:1f:ad:c6:35:50:15:ac:87', 'QMC Attestation Root CA 3'),
    ('a6:41:fd:45:36:c5:90:94:52:7b:71:ab:7d:e1:f1:2b:50:2f:26:ae:ce:46:65:44cc:79:60:b9:3c:3c:db:3c:53:c4:96:ad:83:70:73:41:98:72:78:27:1f:ea:77:56', 'QSEE Attestation Root CA 2'),
    ('a2:51:4b:b8:51:11:bc:66:25:a1:89:44:8b:9d:46:0a:64:d3:3e:15:81:ba:d7:f348:d2:0b:5c:a5:97:f4:e7:80:66:87:06:c2:e7:93:70:3f:2a:3c:0a:5e:52:a4:97', 'XBL Sec Attestation Root CA 2'),
    ('98:c3:d8:11:8d:a7:3a:c9:f1:76:88:10:78:6f:74:20:97:8f:de:65:73:fb:a0:bd84:8a:67:5d:1e:7f:45:3a:50:bf:49:a3:2a:d9:e5:f0:56:22:71:34:af:6e:74:da', 'QMC Attestation Root CA 4'),
    ('7f:72:80:6b:6b:78:75:36:bd:f5:6b:25:1f:9f:fd:d4:81:88:6a:dc:a5:e4:f7:3eb9:19:62:3d:82:a3:d7:f1:43:24:de:12:59:2f:6e:85:a7:e6:4b:35:20:de:ed:3f', 'QSEE Attestation Root CA 4'),
    ('f5:fc:05:5b:82:b5:86:c4:b1:ee:c9:4b:00:dd:ab:e5:fb:3c:3d:a1:48:86:6c:b95b:9d:40:14:48:71:d9:ad:db:81:94:19:8f:13:24:dc:e0:3b:89:ea:07:01:33:37', 'SPSS Attestation Root CA 4'),
    ('e2:47:42:9c:fe:5d:f2:9c:77:b6:81:ee:48:aa:f7:c6:8c:b3:0e:ea:a1:fe:ca:7d6a:11:dd:1d:29:82:f1:e1:ed:85:a8:4d:45:48:c5:4a:16:78:53:ef:26:66:57:a9', 'XBL Sec Attestation Root CA 4'),
    ('ad:51:ef:28:50:24:7f:f0:bd:bc:c8:03:dd:0f:d0:cc:ac:78:51:9c:0d:91:56:165b:a5:73:4d:9f:89:99:90:4e:e3:bb:cb:5d:39:50:9e:9a:cb:c1:ad:00:87:4c:47', 'QMC Attestation Root CA 6'),
    ('20:31:aa:15:5f:ee:c9:ca:5d:8d:c3:fe:60:6a:7e:82:68:ff:4b:68:4c:34:c0:6099:ce:56:15:3f:e1:4c:7c:0c:ef:39:da:0e:f0:12:5d:9f:df:b8:bd:d8:fc:65:9f', 'SPU MBNv7 Image Signing Root CA 6'),
    ('46:7f:30:20:c4:cc:78:8d:2a:27:a6:e0:97:ff:a7:bf:c2:4e:82:c2:d5:69:53:d3b4:5b:49:4c:db:a5:c2:42:2a:94:7d:2c:81:b5:75:2b:8a:2a:c9:ea:c8:ac:df:34', 'SRoT MBNv7 Image Signing Root CA 6'),
    ('e5:a1:03:77:0e:c0:eb:88:54:cd:3f:71:9d:9e:65:8c:41:74:81:7f:63:0c:db:2c60:c8:1e:2a:61:6d:cd:58:10:5d:d8:58:d5:cd:c1:eb:8f:ca:60:2e:a9:60:12:ca', 'QMC Attestation Root CA 6 SubCA 1'),
    ('33:cd:98:26:69:b6:14:b4:f4:7e:3a:49:9b:ba:3a:b0:b5:31:40:86:d0:b3:ce:e157:a0:ed:7d:c8:f4:61:04:4a:97:22:f9:a1:3b:89:d5:1e:1a:12:6e:a0:47:d9:ff', 'SPU MBNv7 Image Signing Root CA 6 SubCA 1'),
    ('04:ef:ba:3b:19:f8:95:6d:1c:6f:73:a2:93:57:84:a8:31:2e:62:b1:ab:a8:ca:2ef2:ff:b7:2a:16:f4:86:6c:28:57:3e:53:12:27:07:73:ce:b3:8f:c3:ec:b5:bd:15', 'SRoT MBNv7 Image Signing Root CA 6 SubCA 1'),
    ('96:19:5a:df:e4:e2:8e:5c:8e:9b:b1:2d:0a:43:51:80:af:ad:54:22:b9:ad:b4:a546:9b:95:3c:a0:b7:76:df:4e:2c:42:18:d4:20:dc:00:07:6f:ac:7c:d6:a9:5d:0f', 'QMC Attestation Root CA 6 SubCA 1'),
    ('f3:53:6f:2e:ee:db:98:9f:63:e4:85:f1:a7:a6:a0:66:46:32:2c:f2:53:3e:af:8e53:0a:0c:9f:ae:d7:b8:7f:d6:67:67:e9:d7:d8:96:f8:a9:58:ad:24:13:df:6c:7d', 'SPU MBNv7 Image Signing Root CA 6 SubCA 1'),
    ('9e:1d:8d:6c:58:de:1c:7d:fb:2b:85:d5:05:fc:f4:d7:c1:13:d1:1b:ec:8b:5b:f70f:1f:22:92:e4:bb:fc:0b:c7:9a:c5:e1:ed:b3:ab:2d:4e:94:29:6b:36:bf:fa:20', 'SRoT MBNv7 Image Signing Root CA 6 SubCA 1'),
    ('5b:dd:4e:af:f8:61:68:7a:86:26:9b:e4:e7:e9:51:c9:5b:38:8c:36:58:82:ae:0229:fd:42:56:61:93:6f:92:81:d1:43:66:e1:a4:80:e7:37:1a:13:97:f9:c9:72:16', 'QCT Root CA 1'),
    ('00:99:c3:45:8b:25:dc:54:3b:62:db:85:1f:c5:be:db:41:24:82:64:bd:92:38:420b:ab:46:42:69:db:8c:d7:3a:5d:e8:21:79:da:61:7d:e5:f7:ec:ff:9f:20:a0:28', 'QDSR Root CA'),
    ('36:c8:86:06:8d:9a:66:34:e9:c5:51:85:04:43:44:e9:e7:56:dc:c3:b5:96:08:7494:2c:7a:1a:15:50:de:e0:d4:2c:db:c7:d1:92:3b:7f:01:23:42:0e:17:93:a0:10', 'QMC Attestation Root CA'),
    ('88:ff:f6:55:0f:14:dc:4e:98:c8:a8:45:c1:bd:b9:f4:2f:b3:7e:b6:c5:8a:cb:60c3:27:56:b0:c5:84a0:2e:a2:16:fa:45:3c:73:7f:e6:2a:54:78:d3:15:02:d6:e7', 'AOST Root CA'),
    ('99:75:8f:bc:00:da:25:a9:45:e3:d4:12:a1:20:8e:b5:f9:7d:a6:bc:fb:5e:69:d7dc:15:89:f9:6ae5:6e:00:5e:02:e2:69:88:29:3b:23:7d:99:b5:0b:c7:cd:fd:ac', 'QKPR Root CA'),
    ('30:da:04:2c:22:9d:b8:5a:17:e4:94:56:f5:c6:fa:52:a4:52:8e:a4:c2:f1:c9:43:ec:16:fe:57:d7:6a:d9:2f:38:fb:8d:1d:35:5e:91:5d:72:b0:28:58:3a:7a:93:96', 'QMC Attestation Root CA 7'),
    ('25:1a:52:b5:1a:19:ee:a7:95:e7:b2:44:f1:e2:44:2b:b0:be:87:bc:af:09:39:42:06:69:9c:a7:c4:f7:c3:13:ba:26:a7:cb:55:c4:a9:90:f7:a5:7e:41:52:91:f7:e1', 'SPU MBN8 Image Signing Root CA 7'),
    ('70:a7:ab:57:7e:f1:54:3e:6e:62:d4:c3:c8:ad:1d:57:e3:02:6f:df:33:d4:8a:7c:83:4f:24:6f:57:04:70:e6:04:e6:48:9f:da:e5:38:55:e3:e2:77:d2:29:4a:0d:f6', 'SRoT MBN8 Image Signing Root CA 7'),
    ('5b:77:a0:86:7a:00:d4:3b:63:88:3d:0e:d1:5e:88:9d:38:43:27:bb:c1:c1:49:1c:d0:60:4d:54:28:43:88:2a:ab:2a:02:df:fe:43:bc:d3:c4:65:75:a2:1f:8a:67:e0', 'QMC Attestation Root CA 7 SubCA 1'),
    ('95:64:97:d5:55:dc:83:e4:44:c9:ff:5d:b9:cb:40:d1:a8:0f:22:be:0a:53:78:20:aa:22:19:ce:5b:6a:c5:6f:b9:7b:e4:6c:9a:fb:14:71:d6:f5:e1:82:d1:4a:04:8a', 'SPU MBN8 Image Signing Root CA 7 SubCA 1'),
    ('2b:c1:f4:61:74:d8:ae:bf:5e:5c:4f:be:8c:1e:7c:8c:90:ad:b0:a5:9a:df:35:49:05:ac:a4:46:79:26:70:e3:7d:8d:a0:a1:20:d7:9b:c9:40:95:84:d6:32:90:43:a6', 'SRoT MBN8 Image Signing Root CA 7 SubCA 1'),
    ('50:e8:60:d9:21:78:b9:0f:73:e8:c2:58:64:07:22:1e:fa:7c:09:0b:68:07:af:0a:c7:dd:74:49:a2:95:d0:ab:8c:39:35:77:bf:36:2e:63:48:2d:46:e6:af:b6:81:db', 'QMC Attestation Root CA 7 SubCA 1'),
    ('92:7f:7a:5d:39:59:32:5b:fe:61:47:cc:32:0b:3c:62:44:c5:1d:7d:77:cb:ad:37:c1:69:88:90:ff:18:7d:13:f9:21:57:98:41:c5:b0:01:8e:7c:d0:b4:29:2f:2a:65', 'SPU MBN8 Image Signing Root CA 7 SubCA 1'),
    ('8f:34:ca:01:c1:20:94:98:db:dc:fe:24:47:31:47:c3:42:63:dd:b6:93:c6:07:9b:29:7a:c6:c3:c6:86:b6:0c:20:de:64:25:ba:d6:cb:b3:6d:23:17:68:be:fa:c0:bd', 'SRoT MBN8 Image Signing Root CA 7 SubCA 1')]
for rch, name in enumerate(PRODUCTION_ROOT_HASHES):
    parsed_rch = '0x' + rch.replace(':', '')
    PRODUCTION_ROOT_HASHES[i] = (parsed_rch, name)
TEST_ROOT_HASHES = [
    ('a0:30:7f:70:78:58:0f:47:dd:79:b0:21:2f:0d:e6:be:b2:73:18:4e:9c:5a:10:c134:58:7a:8d:b4:45:72:d1:85:42:c0:2a:11:b5:2c:cc:5b:69:ac:0e:d3:6f:7a:9a', 'QSEE Application Attestation Test Root'),
    ('06:7b:9e:4a:85:bb:ab:8e:e5:b9:3f:ea:3c:f5:8c:57:fc:8c:e7:99:58:8c:75:7855:b7:4f:2b:d7:53:8b:c7:02:0f:8e:d2:8b:77:11:5e:7a:a6:73:a4:b4:77:79:df', 'QSEE Attestation Test Root CA'),
    ('52:31:65:3e:c4:36:06:61:01:55:17:1f:1f:6a:85:ec:58:45:82:31:54:9a:7f:b22a:db:b7:11:cb:4e:a0:db:38:c9:37:e5:b8:a6:9d:f4:a3:7a:13:54:40:84:cd:05', 'QSEE Communication Test Root CA'),
    ('0d:b7:5e:87:b8:69:7b:14:51:2d:da:7f:f9:12:77:34:4e:0b:a1:37:ba:01:76:6a90:0e:cc:5e:30:c5:60:73:ef:b5:92:dc:5a:97:1d:e3:07:ac:bd:94:b0:ae:31:9b', 'SPSS Attestation Test Root CA'),
    ('a3:8e:b1:9e:30:a4:e0:73:b4:a5:93:60:55:17:b4:5c:61:39:f5:61:33:55:b9:1c96:38:3e:13:05:8c:74:76:6a:cb:a5:1a:d7:fd:a1:18:ab:ef:3d:43:9a:f4:1c:4f', 'QSEE Attestation Test Root CA 2'),
    ('ed:51:42:3a:8a:b2:db:b5:4f:8b:8d:8a:e0:51:e6:66:14:8b:06:02:a9:e5:c7:4c76:ce:1b:61:01:fb:e3:99:f4:4a:df:09:f3:04:16:f1:ae:e4:d1:60:dc:22:79:95', 'QSEE Attestation Test Root CA 4'),
    ('3a:fa:5c:8f:2f:47:ca:8a:fe:b7:85:ee:c1:df:6c:dc:c0:6a:4f:00:a7:e1:18:f465:fa:64:ff:17:77:17:ae:80:4e:f2:7f:ef:60:a6:7f:c2:bd:30:a7:5f:76:60:47', 'SPSS Attestation Test Root CA 4'),
    ('fe:20:4c:88:39:84:36:8f:ee:bf:cc:c5:e0:5c:98:f2:61:c9:06:c9:9c:e2:2c:7c91:01:e9:84:bf:03:22:7f:4a:d1:b7:a6:dc:ab:df:26:63:c6:dd:13:de:71:a1:77', 'SPU MBNv7 Image Signing Test Root CA 6'),
    ('79:34:b2:f6:51:10:70:d6:d3:85:a2:13:47:92:0e:b6:8d:b8:89:a9:fd:63:53:1672:9c:3a:cd:97:01:c7:23:4e:64:94:7a:99:46:78:dd:c1:a2:c4:a2:b5:88:15:52', 'SRoT MBNv7 Image Signing Test Root CA 6'),
    ('3d:b3:8a:09:e7:55:00:f9:6a:26:47:fc:99:d1:78:fb:2a:fa:2e:29:6a:f5:e1:39fe:f8:b4:ad:10:1d:40:56:a8:a6:1d:b0:c8:f8:1c:5c:c2:5e:27:55:d8:8c:f9:c3', 'SPU MBNv7 Image Signing Test Root CA 6 SubCA 1'),
    ('12:2d:ac:7d:6e:5c:02:49:d6:14:29:30:62:3e:f5:f4:de:31:ea:2a:ba:f1:fa:2496:03:ff:29:b8:b4:6c:4c:f3:e5:4a:89:ca:f3:53:14:55:23:bd:e5:49:17:b2:d2', 'SRoT MBNv7 Image Signing Test Root CA 6 SubCA 1'),
    ('d5:d4:5b:46:3a:27:e7:8b:2c:69:0e:78:11:d1:a3:81:01:2b:b3:09:30:c6:46:1029:1f:b6:63:7f:f9:b3:3f:34:e4:12:8d:f0:d4:55:54:71:a7:00:23:19:2e:ea:d7', 'SPU MBNv7 Image Signing Test Root CA 6 SubCA 1'),
    ('5a:c4:74:96:2e:1a:2b:b6:66:4f:2f:c1:33:f7:98:18:e9:14:8a:bb:2c:52:7a:88dd:e5:6b:6f:85:a0:f0:c7:9a:44:03:95:e3:ec:75:44:d4:a5:a9:8b:30:63:32:07', 'SRoT MBNv7 Image Signing Test Root CA 6 SubCA 1'),
    ('d8:fe:8a:63:00:29:17:92:05:a3:5a:18:90:d9:65:f7:ba:47:b9:85:8e:da:e5:fd:3a:8f:d9:34:49:02:5a:1e:f8:db:fc:f2:0e:de:5e:6a:41:98:69:25:18:c9:36:4f', 'SPU MBN8 Image Signing Test Root CA 7'),
    ('78:14:c1:3b:a3:6d:90:2c:0a:24:07:32:6e:24:17:8f:e7:ff:2c:4b:27:a4:1b:fd:eb:61:32:5d:cd:ba:17:f5:b3:8e:d7:dc:c4:37:5d:10:c5:1b:2d:4c:12:2d:a5:10', 'SRoT MBN8 Image Signing Test Root CA 7'),
    ('d9:c7:4a:b8:39:c8:3d:dc:0b:38:fa:53:f0:40:1e:fd:8c:16:ed:14:78:4e:41:bf:9c:ad:90:25:91:b5:8f:44:3b:e6:8b:2a:87:d3:6a:08:ad:bc:77:20:06:b8:0c:cf', 'SPU MBN8 Image Signing Test Root CA 7 SubCA 1'),
    ('f2:bc:17:08:b7:b9:47:a4:8e:d5:6b:bc:f6:be:e0:16:97:74:cb:8b:85:76:25:e6:c9:7a:8c:9e:a2:75:bd:ef:c7:42:e0:6a:35:c6:4e:57:5e:eb:22:57:72:66:7b:d9', 'SRoT MBN8 Image Signing Test Root CA 7 SubCA 1'),
    ('97:c4:b7:a4:0b:78:c3:71:7b:6b:be:d0:54:60:9f:3d:99:7d:27:b5:10:2d:d6:dd:98:3c:94:6c:d7:d9:d7:d8:3e:82:6a:95:73:9a:f5:48:1e:ce:a2:6d:83:9d:6e:de', 'SPU MBN8 Image Signing Test Root CA 7 SubCA 1'),
    ('fc:d0:5b:9a:40:ce:c1:21:f8:9e:86:a8:2d:60:fc:68:ca:b9:51:6b:e6:b6:49:b3:d0:83:53:50:58:92:e9:ff:0a:4f:7c:d7:cc:2f:a4:e0:9a:30:8e:47:10:ef:47:b8', 'SRoT MBN8 Image Signing Test Root CA 7 SubCA 1')]
for rch, name in enumerate(TEST_ROOT_HASHES):
    parsed_rch = '0x' + rch.replace(':', '')
    TEST_ROOT_HASHES[i] = (parsed_rch, name)
