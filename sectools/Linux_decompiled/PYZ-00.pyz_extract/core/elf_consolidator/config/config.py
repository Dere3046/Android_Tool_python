
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional
from lxml.etree import Element, XMLParser, XMLSchema, XMLSyntaxError, parse
from cmd_line_interface.sectools.elf_consolidator.defines import CONFIG
from common.data.data import tuple_to_version_string, version_string_to_tuple
from common.logging.logger import log_info
from common.parser.elf.bit32.program_header import ProgramHeader32
from core.elf_consolidator.utils import get_loadable_phdrs

def mem_align(address = None, alignment = None):
    '''Given an address and an alignment boundary, return the address aligned to the next boundary.'''
    if not alignment:
        pass
    alignment = 1
    if address % alignment == 0:
        return address
    return None + (alignment - address % alignment)


class TranslationTableEntry(NamedTuple):
    collapse_segments: bool = 'TranslationTableEntry'
    
    def from_dict(cls = None, what = None):
        
        def _converter(field_type = None, v = None):
            '''Somewhat a generic converter. Could be reused.'''
            if field_type is int:
                if isinstance(v, str):
                    ret = int(v, 0, **('base',))
                    return ret
                ret = None
                return ret
            if None is bool:
                if isinstance(v, str):
                    ret = v in ('true', '1')
                    return ret
                ret = None
                return ret
            raise None

    # WARNING: Decompyle incomplete

    from_dict = None(from_dict)
    
    def translate_and_update_phdrs(self = None, phdrs = None):
        '''
        Perform address translation on phdrs as per the translation strategy.
        Supports only two strategies selectable by the "collapse_segments" attribute in the schema:
        - true: Will collapse the segments VirtAddr together to save space in RAM.
        - false: Will rebase the segments to a new base address preserving their offsets to it.
        @param phdrs - list of ELF program headers to translate.
        Returns nothing - translates in place.
        '''
        new_addr = self.translated_addr
        for phdr in get_loadable_phdrs(phdrs):
            if phdr.p_paddr <= phdr.p_paddr or phdr.p_paddr < self.phy_addr + self.length:
                pass
            else:
                self.phy_addr
            old = phdr.p_paddr
            log_info(f'''Translated address {old:#08x} to {phdr.p_paddr:#08x} for image with Software ID {self.sw_id:#x}.''')



class Config(NamedTuple):
    skipped_sw_ids: List[int] = 'Config'
    entry_point_sw_id: Optional[int] = None


def xml2dict(element = None):
    '''Generic XML to dict converter.'''
    
    def attribute_converter(obj = None, root = None):
        for child in obj:
            if len(child):
                ret = attribute_converter(child, { })
            elif hasattr(child, 'text'):
                ret = child.text
            
            if child.tag in root:
                if not isinstance(root[child.tag], list):
                    root[child.tag] = [
                        root[child.tag]]
                root[child.tag].append(ret)
                continue
            root[child.tag] = ret
        return root

    return attribute_converter(element, { })


def parse_config_file(config_file_path = None):
    '''
    Relies on the XML schema for config file validation.
    Members:
    - ledger_load_addr: required - Memory address where the concatenated MDT data of all images will be loaded.
    - qti_dpr_load_addr: required - Memory address where the QTI DPR binary will be loaded.
    - translation_table entries: required - Address translations to be applied to segments of each ELF.
    - skipped_sw_ids: required - List of SWIDs whose loadable segments should not be packed into the Consolidated ELF.
    '''
    xsd_path = Path(__file__).parent.absolute() / 'config.xsd'
# WARNING: Decompyle incomplete

