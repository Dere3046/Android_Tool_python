
from pathlib import Path
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import GENERATE_OP, OUTFILE, SUBFEATURE
from cmd_line_interface.sectools.elf_tool.common.defines import DATA
from cmd_line_interface.sectools.mbn_tool.defines import BOOT_IMAGE_ID, DATA_SIZE_ALIGNMENT, IMAGE_DEST_PTR, MBN_VERSION
from common.data.data import ceil_to_multiple
from common.data.defines import PAD_BYTE_0
from common.logging.logger import log_debug, log_info
from common.parser.mbn.mbn import MBN
from common.utils import write_cmdline_file
from core.core_interface import CoreInterface

class MBNToolCore(CoreInterface):
    
    def run(self = None, parsed_args = None):
        if parsed_args.get(SUBFEATURE) == GENERATE_OP:
            log_info(f'''Performing {GENERATE_OP} operation.''')
            log_debug(f'''Ensuring {DATA} is not already an MBN.''')
            if MBN.is_type(parsed_args.get(DATA)):
                raise RuntimeError(f'''{DATA} is already an MBN.''')
            None(f'''Constructing a v{parsed_args.get(MBN_VERSION)} MBN.''')
            data = parsed_args.get(DATA)
            if alignment = int(parsed_args.get(DATA_SIZE_ALIGNMENT), 16) and len(data) % alignment:
                data = data.ljust(ceil_to_multiple(len(data), alignment), PAD_BYTE_0)
            if not parsed_args.get(BOOT_IMAGE_ID):
                pass
            if not parsed_args.get(IMAGE_DEST_PTR):
                pass
            mbn = MBN(parsed_args.get(MBN_VERSION), data, int('0x0', 16), int('0x0', 16), **('mbn_version', 'code', 'boot_image_id', 'image_dest_ptr'))
            log_info(f'''Completed {GENERATE_OP} operation.''')
            log_debug('Packing generated image.')
            mbn_data = mbn.pack()
            log_info(f'''Writing image to: {Path(parsed_args.get(OUTFILE))}''')
            write_cmdline_file(Path(parsed_args.get(OUTFILE)), mbn_data, OUTFILE)
            return None
        raise None(f'''{parsed_args.get(SUBFEATURE)} operation is unsupported.''')


