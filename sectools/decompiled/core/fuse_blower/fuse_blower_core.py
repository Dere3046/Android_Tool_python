
from pathlib import Path
from typing import Any, NamedTuple, Type
import profile
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools import fuseblower
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE
from cmd_line_interface.sectools.cmd_line_common.defines import GENERATE, HASH, INFILE, OUTFILE, SIGN, SIGNATURE_FORMAT
from cmd_line_interface.sectools.fuseblower.defines import FUSE_BLOWER_NAME, FUSE_GROUP, RANDOM, RECOMMENDED_FUSES
from common.data.data import comma_separated_string
from common.logging.logger import log_debug, log_info, log_warning
from common.parser.elf.defines import INT_TO_ELFCLASS
from common.parser.hash_segment.defines import AUTHORITY_OEM
from common.parser.sec_dat.defines import BLOW_OPERATION, BLOW_RANDOM_OPERATION, SEGMENT_EFUSE, SEGMENT_TYPE_DESCRIPTION_TO_INT
from common.parser.sec_dat.sec_dat import SecDat
from common.parser.sec_elf.sec_elf import SecELF
from common.utils import get_num_bits_from_range, get_start_and_end_indices, is_multi_bit, write_cmdline_file
from core.base_device_restrictions import BaseDeviceRestrictions
from core.core_interfaces.core_security_profile_validator_interface import CoreSecurityProfileValidatorInterface
from core.core_interfaces.core_specific_profile_consumer_interface import CoreSpecificProfileConsumerInterface
from core.core_interfaces.device_restrictions_consumer import DeviceRestrictions, DeviceRestrictionsConsumer
from core.fuse_blower.utils import compute_fec, contains_fec_fuses, fuse_cmd_line_arg_string, fuse_parsed_arg_string, get_bit_mask, is_fec_fuse, is_lsb
from core.hash_sign_core import HashSignCore, log_info_wrap
from core.profile_validator.validate import validate_authentication
from profile.profile_core import SecurityProfile
from profile.schema import Profile, ProfileParser
FuseInfo = NamedTuple('FuseInfo', [
    ('region_type', str),
    ('lsb', int),
    ('msb', int),
    ('operation', str)])

class FuseBlowerCore(HashSignCore, CoreSpecificProfileConsumerInterface, DeviceRestrictionsConsumer, CoreSecurityProfileValidatorInterface):
    
    def run(self = None, parsed_args = None):
        log_debug(f'''Entering {FUSE_BLOWER_NAME} core.''')
        super().run(parsed_args)
    # WARNING: Decompyle incomplete

    
    def codependent_operations(self = None):
        return [
            HASH,
            SIGN]

    codependent_operations = None(codependent_operations)
    
    def device_restrictions_class(self = None):
        return BaseDeviceRestrictions

    device_restrictions_class = None(device_restrictions_class)
    
    def validate_mandatory_security_profile_attributes(parsed_profiles = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    validate_mandatory_security_profile_attributes = None(validate_mandatory_security_profile_attributes)
    
    def set_core_specific_profile_attributes(cls = None, security_profile = None, parsed_args = classmethod):
        security_profile.set_fuse_blowing_features()
        if security_profile.authenticators:
            security_profile.set_signing_features_and_signature_format(AUTHORITY_OEM, parsed_args.get(SIGNATURE_FORMAT))
            return None

    set_core_specific_profile_attributes = None(set_core_specific_profile_attributes)
    
    def get_image_ids(security_profile = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    get_image_ids = None(get_image_ids)
    
    def generate_operation(self = None, parsed_args = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_fuse_entries(self = None, parsed_args = None):
        log_debug('Computing fuse entries to be added to Sec Dat segment.')
        fuse_entry_info = { }
        processed_multi_row_full_region_fuses = []
        processed_multi_row_partial_region_fuses = []
        blow_random_fuse_rows = self.get_blow_random_fuses(parsed_args)
        fuse_group_args = self.get_fuse_group_flag_args(parsed_args.get(FUSE_GROUP))
    # WARNING: Decompyle incomplete

    
    def get_fuse_group_flag_args(provided_fuse_groups = None):
        flag_args = []
        if provided_fuse_groups:
            for provided_group in provided_fuse_groups:
                flag_args += (lambda .0: [ fuse_arg.argument for fuse_arg in .0 if fuse_arg.multi_bit ])(fuseblower.fuse_groups[provided_group])
        return flag_args

    get_fuse_group_flag_args = None(get_fuse_group_flag_args)
    
    def get_blow_random_fuses(parsed_args = None):
        log_debug(f'''Fetching addresses of fuse rows whose operation needs to be set to {BLOW_RANDOM_OPERATION}.''')
    # WARNING: Decompyle incomplete

    get_blow_random_fuses = None(get_blow_random_fuses)
    
    def set_fec_bits(fuse_entry_info = None, fuse_row = None, region_id = staticmethod, segment_type = ('fuse_entry_info', dict, 'fuse_row', ProfileParser.fuse_row, 'region_id', str, 'segment_type', int, 'return', None)):
        for fuse in fuse_row.fuse:
            if is_fec_fuse(fuse.name) and is_multi_bit(fuse.bits) and fuse_entry_info.get((segment_type, fuse_row.address)):
                lsb = fuse_entry_info[(segment_type, fuse_row.address)].lsb
                msb = fuse_entry_info[(segment_type, fuse_row.address)].msb
                fec_val = compute_fec(msb << 32 | lsb)
                log_debug(f'''Setting computed FEC value, {fec_val}, for row {fuse_row.address} with MSB {msb} and LSB {lsb}.''')
                FuseBlowerCore.set_fuse_value(fuse_entry_info, fuse_row.address, fuse.bits, region_id, fec_val)

    set_fec_bits = None(set_fec_bits)
    
    def set_fuse_bit(fuse_entry_info, address, segment_type = None, bit_number = None, region_id = staticmethod, operation = (True,), set_bit = ('fuse_entry_info', dict, 'address', int, 'segment_type', int, 'bit_number', int, 'region_id', str, 'operation', str, 'set_bit', bool, 'return', None)):
        if (segment_type, address) in fuse_entry_info:
            lsb = fuse_entry_info[(segment_type, address)].lsb
            msb = fuse_entry_info[(segment_type, address)].msb
            log_debug(f'''Updating fuse entry at address {address} with MSB {msb} and LSB {lsb}.''')
            if set_bit:
                if is_lsb(bit_number):
                    lsb = 1 << bit_number | fuse_entry_info[(segment_type, address)].lsb
                else:
                    msb = 1 << bit_number - 32 | fuse_entry_info[(segment_type, address)].msb
            log_debug(f'''Setting fuse entry at address {address} with new MSB {msb} and new LSB {lsb}.''')
            fuse_entry_info[(segment_type, address)] = fuse_entry_info[(segment_type, address)]._replace(lsb, msb, **('lsb', 'msb'))
            return None
        (lsb, msb) = None
        if set_bit:
            if is_lsb(bit_number):
                lsb = 1 << bit_number
            else:
                msb = 1 << bit_number - 32
        log_debug(f'''Creating new fuse entry at address {address} with MSB {msb} and LSB {lsb}.''')
        fuse_entry_info[(segment_type, address)] = FuseInfo(region_id, lsb, msb, operation)

    set_fuse_bit = None(set_fuse_bit)
    
    def set_fuse_value(fuse_entry_info, address, fuse_bits = None, region_id = None, value = staticmethod, segment_type = (SEGMENT_EFUSE, BLOW_OPERATION), operation = ('fuse_entry_info', dict, 'address', int, 'fuse_bits', str, 'region_id', str, 'value', int, 'segment_type', int, 'operation', str, 'return', None)):
        if is_multi_bit(fuse_bits):
            log_debug('Multi bit fuse detected.')
            (start, end) = get_start_and_end_indices(fuse_bits)
            for bit_number in range((end - start) + 1):
                log_debug(f'''Setting multi bit fuse value at address {address} and bits {fuse_bits} to user requested value {value}.''')
                if not value:
                    FuseBlowerCore.set_fuse_bit(fuse_entry_info, address, segment_type, start + bit_number, region_id, operation, False, **('set_bit',))
                    continue
                if 1 << bit_number & value:
                    FuseBlowerCore.set_fuse_bit(fuse_entry_info, address, segment_type, start + bit_number, region_id, operation)
            return None
        None(f'''Setting single bit fuse value at address {address} and bit {fuse_bits}.''')
        FuseBlowerCore.set_fuse_bit(fuse_entry_info, address, segment_type, int(fuse_bits), region_id, operation)

    set_fuse_value = None(set_fuse_value)
    
    def set_combined_region_or_fuse_value(fuse_entry_info, region, value, segment_type = None, fuse_name = None, look_up = staticmethod, formatted_value = ('fuse_entry_info', dict, 'region', ProfileParser.fuse_region, 'value', str | int, 'segment_type', int, 'fuse_name', str, 'look_up', dict, 'formatted_value', int, 'return', None)):
        for fuse_row in look_up[fuse_name]:
            for fuse in fuse_row.fuse:
                if fuse_cmd_line_arg_string(fuse.name) != fuse_name:
                    continue
                if not is_multi_bit(fuse.bits) and is_fec_fuse(fuse.name):
                    number_of_bits = get_num_bits_from_range(fuse.bits)
                    log_debug(f'''Setting multi row fuse value starting at address {fuse_row.address} to user requested value {value}.''')
                    FuseBlowerCore.set_fuse_value(fuse_entry_info, fuse_row.address, fuse.bits, region.id, formatted_value & get_bit_mask(number_of_bits), segment_type)
                    formatted_value >>= number_of_bits

    set_combined_region_or_fuse_value = None(set_combined_region_or_fuse_value)
    
    def get_int_formatted_value_for_full_region_fuse(value = None, fuse_name = None):
        log_debug(f'''Performing byte-reversal for full region fuse {fuse_name}.''')
        value = value.removeprefix('0x')
        return None(None(None((lambda .0 = None: [ value[i:i + 2] for i in .0 ])(range(0, len(value), 2)))), 16)

    get_int_formatted_value_for_full_region_fuse = None(get_int_formatted_value_for_full_region_fuse)
    __classcell__ = None

