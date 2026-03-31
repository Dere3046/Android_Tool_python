
from pathlib import Path
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import OUTFILE, QTI_DPR
from cmd_line_interface.sectools.elf_consolidator.defines import CONFIG, ELF_CONSOLIDATOR_NAME, IMAGES, PIL_SPLIT_OUTDIR
from cmd_line_interface.sectools.secure_image.defines import PIL_SPLIT
from common.logging.logger import log_debug, log_info
from common.utils import write_cmdline_file
from core.core_interface import CoreInterface
from core.elf_consolidator.config.config import parse_config_file
from core.elf_consolidator.elf_consolidator import generate_consolidated_elf

class ELFConsolidatorCore(CoreInterface):
    
    def run(self = None, parsed_args = None):
        log_info(f'''Running {ELF_CONSOLIDATOR_NAME}.''')
        config = parse_config_file(parsed_args.get(CONFIG).path)
        log_debug(f'''Parsed config file: {config}''')
        consolidated_elf = generate_consolidated_elf(parsed_args.get(IMAGES), config, parsed_args.get(QTI_DPR))
        outfile = Path(parsed_args.get(OUTFILE))
        log_info(f'''Writing Consolidated ELF image to: {outfile}''')
        write_cmdline_file(outfile, consolidated_elf.pack(), OUTFILE)
        if parsed_args.get(PIL_SPLIT):
            outdir = Path(parsed_args.get(PIL_SPLIT_OUTDIR)) if parsed_args.get(PIL_SPLIT_OUTDIR) else outfile.parent
            consolidated_elf.write_pil_split_image(outfile.stem, outdir, PIL_SPLIT_OUTDIR if parsed_args.get(PIL_SPLIT_OUTDIR) else f'''{PIL_SPLIT} {OUTFILE}''')
            return None


