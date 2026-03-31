
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import INFILE, OUTFILE, SUBFEATURE
from cmd_line_interface.sectools.fuse_validator.cmd_line_common.defines import COMPARE_NAME, GENERATE_PAYLOAD_NAME, SHOW_ON_TARGET_RESULTS_NAME
from cmd_line_interface.sectools.fuse_validator.compare.defines import PAYLOAD
from cmd_line_interface.sectools.fuse_validator.generate_payload.defines import ON_TARGET
from common.data.data import comma_separated_string, hex_val, plural_s, properties_repr
from common.logging.logger import QuietError, log_debug, log_info
from common.parser.fuse_validator_payload.defines import OFF_TARGET_FEATURE_ID, ON_TARGET_FEATURE_ID
from common.parser.fuse_validator_payload.fuse_list.defines import FuseEntryUnion
from common.parser.fuse_validator_payload.fuse_list.fuse_list_header import FuseListHeader
from common.parser.fuse_validator_payload.payload_request.payload_request import FuseValidatorPayloadRequest
from common.parser.fuse_validator_payload.payload_response.payload_reponse import FuseValidatorPayloadResponse
from common.parser.fuse_validator_payload.payload_response.payload_response_header import FuseValidatorPayloadResponseHeader
from common.parser.sec_dat.defines import BLOW_RANDOM_OPERATION
from common.parser.sec_dat.fuse_entry import FuseEntry
from common.parser.sec_dat.sec_dat import SecDat
from common.parser.sec_elf.sec_elf import SecELF
from common.parser.utils import get_parsed_image
from common.utils import write_cmdline_file
from core.core_interface import CoreInterface
from core.hash_sign_core import log_info_wrap
MISSING = 'MISSING'

class FuseValidatorCore(CoreInterface):
    
    def run(self = None, parsed_args = None):
        pass
    # WARNING: Decompyle incomplete

    
    def generate_payload(infiles = None, outfile = None, on_target = staticmethod):
        log_debug(f'''Collecting all fuses from infile{plural_s(infiles)}.''')
        fuses = list(FuseValidatorCore.combine_infiles(infiles).values())
        if not on_target:
            for fuse in fuses:
                (fuse.region_type, fuse.msb, fuse.lsb, fuse.operation) = (0, 0, 0, 0)
        log_debug('Creating a payload request.')
        request = FuseValidatorPayloadRequest(ON_TARGET_FEATURE_ID if on_target else OFF_TARGET_FEATURE_ID, fuses, **('feature_id', 'fuses'))
        log_info(f'''Writing payload request to: {Path(outfile)}''')
        write_cmdline_file(Path(outfile), request.pack(), OUTFILE)

    generate_payload = None(generate_payload)
    
    def compare_payload(infiles = None, payload = None):
        if not FuseValidatorPayloadResponse.is_type(payload):
            raise RuntimeError(f'''{PAYLOAD} is not a Fuse Validator Payload Response.''')
        payload_response = None(payload)
    # WARNING: Decompyle incomplete

    compare_payload = None(compare_payload)
    
    def show_on_target_results(infile = None):
        log_debug('Parsing infile Payload Response.')
        payload_response = FuseValidatorPayloadResponse(infile)
    # WARNING: Decompyle incomplete

    show_on_target_results = None(show_on_target_results)
    
    def combine_fuse_values(fuse_entry1 = None, fuse_entry2 = None):
        fuse_entry1.lsb |= fuse_entry2.lsb
        fuse_entry1.msb |= fuse_entry2.msb
        return fuse_entry1

    combine_fuse_values = None(combine_fuse_values)
    
    def combine_infiles(infiles = None):
        fuse_entries = { }
        log_debug(f'''Parsing infile Fuse Blower Image{plural_s(infiles)}.''')
        infile_versions = []
    # WARNING: Decompyle incomplete

    combine_infiles = None(combine_infiles)
    
    def display_mismatched_fuses(response_header = None, fuse_list_header = None, mismatched_fuses = staticmethod, missing_on_target_fuses = (None, None), missing_secdat_fuses = ('response_header', FuseValidatorPayloadResponseHeader, 'fuse_list_header', FuseListHeader, 'mismatched_fuses', List[Tuple[(FuseEntryUnion, FuseEntryUnion)]], 'missing_on_target_fuses', Optional[List[FuseEntry]], 'missing_secdat_fuses', Optional[List[FuseEntry]], 'return', None)):
        table = [
            ('Index', 'Address', 'Region Type', 'Operation', 'Infile MSB', 'Infile LSB', 'Device MSB', 'Device LSB')]
        all_fuses = list(map((lambda fuse_tuple: FuseValidatorCore.get_row_from_fuses(fuse_tuple[1], fuse_tuple[0])), mismatched_fuses))
        if missing_on_target_fuses:
            all_fuses += list(map((lambda infile_fuse: FuseValidatorCore.get_row_from_fuses(infile_fuse, **('fuse_1',))), missing_on_target_fuses))
        if missing_secdat_fuses:
            all_fuses += list(map((lambda device_fuse: FuseValidatorCore.get_row_from_fuses(device_fuse, **('fuse_2',))), missing_secdat_fuses))
        for idx, fuse_row in enumerate(sorted(all_fuses, (lambda x: x[0]), **('key',))):
            table.append((str(idx),) + fuse_row)
        raise QuietError('Fuse Validator Payload Response Header:\n' + properties_repr(response_header.get_properties()) + '\n\n' + 'Fuse List Header:\n' + properties_repr(fuse_list_header.get_properties()) + '\n\n' + 'The following fuses mismatched:\n' + properties_repr(table, [
            0], **('sep_rows',)))

    display_mismatched_fuses = None(display_mismatched_fuses)
    
    def get_row_from_fuses(fuse_1 = None, fuse_2 = None):
        row_label_fuse = fuse_1 if fuse_1 else fuse_2
    # WARNING: Decompyle incomplete

    get_row_from_fuses = None(get_row_from_fuses)

