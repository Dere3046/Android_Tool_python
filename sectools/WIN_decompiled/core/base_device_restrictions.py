
from typing import Any, Dict, List, Optional
import profile
from cmd_line_interface.base_defines import get_cmd_member
from cmd_line_interface.sectools.cmd_line_common.defines import ANTI_ROLLBACK_VERSION, INDEPENDENT, MEASUREMENT_REGISTER_TARGET, OEM_ID, OEM_LIFECYCLE_STATE, OEM_PRODUCT_ID, PLATFORM_BINDING, SECURITY_PROFILE, SEGMENT_HASH_ALGORITHM, SERIAL_NUMBER, SOC_LIFECYCLE_STATE, TRANSFER_ROOT
from cmd_line_interface.sectools.secure_image.defines import CLIENT_ID, FEATURE_ID, LIBRARY_ID, NOP, SECONDARY_SOFTWARE_ID, TRANSFER_UIE_KEY
from common.data.data import and_separated, comma_separated_string
from common.parser.hash_segment.defines import DEVICE_RESTRICTIONS, PLATFORM_BINDING_DEVICE_RESTRICTIONS
from core.platform_binding_utilities import PLATFORM_BINDINGS_MAPPING

class BaseDeviceRestrictions:
    INT_MEMBERS = list(map(get_cmd_member, [
        SECONDARY_SOFTWARE_ID,
        FEATURE_ID,
        CLIENT_ID,
        LIBRARY_ID,
        OEM_ID,
        OEM_PRODUCT_ID,
        ANTI_ROLLBACK_VERSION]))
    
    def __init__(self, jtag_debug, oem_root_certificate_hash, secondary_software_id, feature_id, client_id, library_id, transfer_uie_key, soc_lifecycle_state, crash_dump, serial_number, oem_id, oem_product_id, anti_rollback_version, root_certificate_index, transfer_root, measurement_register_target, oem_lifecycle_state, serial_numbers_fatal, soc_hw_versions, jtag_ids, soc_feature_ids = None, product_segment_ids = None, segment_hash_algorithm = None, platform_binding_provided = (None, None, None, None, None, None, False, None, False, None, None, None, None, 0, False, None, None, True, None, None, None, None, None, False, None), encryption_format = ('jtag_debug', Optional[str], 'oem_root_certificate_hash', Optional[str], 'secondary_software_id', Optional[int], 'feature_id', Optional[int], 'client_id', Optional[int], 'library_id', Optional[int], 'transfer_uie_key', bool, 'soc_lifecycle_state', Optional[List[str]], 'crash_dump', bool, 'serial_number', Optional[List[int]], 'oem_id', Optional[int], 'oem_product_id', Optional[int], 'anti_rollback_version', Optional[int], 'root_certificate_index', int, 'transfer_root', bool, 'measurement_register_target', Optional[str], 'oem_lifecycle_state', Optional[str], 'serial_numbers_fatal', bool, 'soc_hw_versions', Optional[List[int]], 'jtag_ids', Optional[List[int]], 'soc_feature_ids', Optional[List[int]], 'product_segment_ids', Optional[List[int]], 'segment_hash_algorithm', Optional[str], 'platform_binding_provided', bool, 'encryption_format', Optional[str], 'return', None)):
        self.jtag_debug = jtag_debug
        self.oem_root_certificate_hash = oem_root_certificate_hash
        self.secondary_software_id = secondary_software_id
        self.feature_id = feature_id
        self.client_id = client_id
        self.library_id = library_id
        self.transfer_uie_key = transfer_uie_key
        self.soc_lifecycle_state = sorted(set(soc_lifecycle_state)) if soc_lifecycle_state else soc_lifecycle_state
        self.crash_dump = crash_dump
        self.serial_number = sorted(set(serial_number)) if serial_number else serial_number
        self.oem_id = oem_id
        self.oem_product_id = oem_product_id
        self.anti_rollback_version = anti_rollback_version
        self.root_certificate_index = root_certificate_index
        self.transfer_root = transfer_root
        self.measurement_register_target = measurement_register_target
        self.oem_lifecycle_state = oem_lifecycle_state
        self.serial_numbers_fatal = serial_numbers_fatal
        self.soc_hw_versions = sorted(set(soc_hw_versions)) if soc_hw_versions else soc_hw_versions
        self.jtag_ids = sorted(set(jtag_ids)) if jtag_ids else jtag_ids
        self.soc_feature_ids = sorted(set(soc_feature_ids)) if soc_feature_ids else soc_feature_ids
        self.product_segment_ids = sorted(set(product_segment_ids)) if product_segment_ids else product_segment_ids
        self.segment_hash_algorithm = segment_hash_algorithm
        self.platform_binding_provided = platform_binding_provided
        self.encryption_format = encryption_format

    
    def from_parsed_args(cls = None, cmdline_args = None, security_profile_args = classmethod):
        ret = cls()
        ret.update(cmdline_args, security_profile_args)
        return ret

    from_parsed_args = None(from_parsed_args)
    
    def update(self = None, cmdline_args = None, security_profile_args = None):
        constructor_args = cmdline_args | security_profile_args if security_profile_args else cmdline_args
        for attr, val in vars(self).items():
            if attr in self.INT_MEMBERS and cmd_line_val = constructor_args.get(attr):
                vars(self)[attr] = int(cmd_line_val, 16)
                continue
            if attr == get_cmd_member(SERIAL_NUMBER) and cmd_line_val = constructor_args.get(attr):
                vars(self)[attr] = (lambda .0: [ int(sn, 16) for sn in .0 ])(cmd_line_val[0])
                continue
            vars(self)[attr] = constructor_args.get(attr) if attr in constructor_args and constructor_args.get(attr) is not None else val
        if get_cmd_member(PLATFORM_BINDING) in cmdline_args:
            pass
        vars(self)['platform_binding_provided'] = cmdline_args.get(get_cmd_member(PLATFORM_BINDING))

    
    def validate_allowed_device_restrictions(self = None, serial_bound_features = None, independent_platform_binding_non_fatal = None):
        security_profile = profile.SECURITY_PROFILE
    # WARNING: Decompyle incomplete

    
    def device_restrictions_provided(self = None, ignore_default_platform_bindings = None):
        pass
    # WARNING: Decompyle incomplete


