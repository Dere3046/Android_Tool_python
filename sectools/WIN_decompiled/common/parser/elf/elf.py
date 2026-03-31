
import operator
from glob import glob
from math import gcd
from operator import methodcaller
from pathlib import Path
from typing import Any, NamedTuple, Sequence
from common.data.base_parser import DumpDict
from common.data.data import ceil_to_multiple, extract_data_or_fail, is_congruent, properties_repr, wrap_text
from common.data.defines import PAD_BYTE_0
from common.logging.logger import log_debug, log_info
from common.parser.elf.bit32.elf_header import ELFHeader32
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit32.section_header import SectionHeader32
from common.parser.elf.bit64.elf_header import ELFHeader64
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.bit64.section_header import SectionHeader64
from common.parser.elf.defines import ALIGN_1, ALIGN_4, ELFCLASS32, ELFCLASS64, ELF_HEADER, PADDING, PHDR_TABLE, PT_INTERP, PT_LOAD, PT_ONE_SHOT_HASH, PT_PHDR, SHDR_TABLE, SHN_UNDEF, SHT_DYNAMIC, SHT_DYNSYM, SHT_HASH, SHT_NOBITS, SHT_NULL, SHT_STRTAB, SH_FLAGS, UNALIGNED
from common.parser.elf.elf_header import ELFHeaderCommon
from common.parser.elf.positional_data import AbstractPositionalData, PositionalData
from common.parser.elf.section_header import SECTION_HEADER_CLASSES
from common.parser.hash_segment.defines import AUTHORITY_OEM
from common.parser.mdt.mdt import MDT
from common.parser.parser_image_info_interface import ELF_PROPERTIES, ImageFormatType, ImageInfoInterface, ImageProperties
from common.utils import delete_file, write_cmdline_file
from profile.schema import ELFProperties, ImageFormat
ELF_HEADER_CLASSES = {
    ELFCLASS64: ELFHeader64,
    ELFCLASS32: ELFHeader32 }

class ClusterLimits(NamedTuple):
    end: int = 'ClusterLimits'


class PILSplitImage(NamedTuple):
    b_files: list[memoryview | bytearray] = 'PILSplitImage'


class ELF(ImageInfoInterface, MDT):
    
    def __init__(self = None, data = None, **kwargs):
        self.shdrs = []
        self.segments = { }
        self.sections = { }
        self.paddings = { }
    # WARNING: Decompyle incomplete

    
    def phdr_table_offset(self = None):
        pass
    # WARNING: Decompyle incomplete

    phdr_table_offset = None(phdr_table_offset)
    
    def unpack(self = None, data = None):
        ''' Parse the data of an ELF image. '''
        super().unpack(data)
    # WARNING: Decompyle incomplete

    
    def validate_before_operation(self = None, validate_sections = None, is_second_authority = None, **_):
        pass
    # WARNING: Decompyle incomplete

    
    def flatten_segment(self = None, phdr = None):
        phdr_idx = self.phdrs.index(phdr)
        data = self.segments[phdr]
        self.remove_segment(phdr)
        self.add_segment(phdr, data, phdr_idx, **('phdr_idx',))

    
    def remove_elf_hdr_phdr_table_overlaps(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def set_section_names(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_shdr_table_positional_entry(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_shdr_positional_entries(self = None):
        shdr_positional_entries = []
        if self.shdrs:
            shdr_positional_entries.append(self.get_shdr_table_positional_entry())
            shdr_positional_entries += (lambda .0: [ shdr for shdr in .0 if shdr.ignore ])(self.shdrs)
        return shdr_positional_entries

    
    def get_paddings_entries(self = None):
        return list(self.paddings.keys())

    
    def get_greatest_offset(self = None):
        return self.get_positional_entries()[-1].end + 1

    
    def get_data_to_pack(self = None, positional_entry = None):
        data_to_pack = bytearray()
        if isinstance(positional_entry, (ELFHeader32, ELFHeader64)):
            data_to_pack = positional_entry.pack()
            return memoryview(data_to_pack)
        if None.data_name == PHDR_TABLE:
            for phdr in self.phdrs:
                data_to_pack += phdr.pack()
            return memoryview(data_to_pack)
        if None.data_name == SHDR_TABLE:
            for shdr in self.shdrs:
                data_to_pack += shdr.pack()
            return memoryview(data_to_pack)
        if None(positional_entry, (ProgramHeader32, ProgramHeader64)):
            data_to_pack = self.segments[positional_entry]
            return memoryview(data_to_pack)
        if None(positional_entry, (SectionHeader32, SectionHeader64)):
            data_to_pack = self.sections[positional_entry]
            return memoryview(data_to_pack)
    # WARNING: Decompyle incomplete

    
    def get_data_from_entries(self = None, entries = None):
        data = bytearray()
        shift = entries[0].offset
        for positional_entry in entries:
            offset = positional_entry.offset - shift
            end = positional_entry.end - shift
            data_to_pack = self.get_data_to_pack(positional_entry)
            if data_to_pack:
                if len(data_to_pack) != positional_entry.size:
                    raise RuntimeError(f'''Size of data to pack, {len(data_to_pack)} bytes, does not match size declared by entry:\n{positional_entry}.''')
                if None > len(data):
                    raise RuntimeError(f'''There is a gap of {offset - len(data)} bytes before entry:\n{positional_entry}.''')
                if None < len(data):
                    if data_to_pack != memoryview(data)[offset:end + 1]:
                        raise RuntimeError(f'''Encapsulated data mismatches already packed data for entry:\n{positional_entry}.''')
                if end >= len(data):
                    if data_to_pack[:len(data) - offset] != memoryview(data)[offset:]:
                        raise RuntimeError(f'''Overlapping data mismatches already packed data for entry:\n{positional_entry}.''')
                    data_to_pack = None[len(data) - offset:]
                data += data_to_pack
        return data

    
    def pack(self = None):
        return memoryview(self.get_data_from_entries(self.get_positional_entries()))

    
    def is_type(cls = None, data = None):
        ''' Detect whether the data is of an ELF image. '''
        return ELFHeaderCommon.is_type(data)

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        dump_files = super().get_dump_files(directory)
        if self.phdrs:
            for i, phdr in enumerate(self.phdrs):
                dump_files[f'''{directory}/segments/segment_{i}.bin'''] = self.segments[phdr]
        if self.shdrs:
            dump_files[f'''{directory}/section_headers.bin'''] = b''.join((lambda .0: [ shdr.pack() for shdr in .0 ])(self.shdrs))
            for i, shdr in enumerate(self.shdrs):
                dump_files[f'''{directory}/sections/section_{i}.bin'''] = self.sections[shdr]
        return dump_files

    
    def _repr_elf(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        return self._repr_compression_format() + self._repr_elf()

    
    def _repr_flags_key(line_width = None):
        flag_keys = []
        for _, flag, key in SH_FLAGS:
            flag_keys.append(f'''{flag} ({key})''')
        return '\nKey to Flags:\n' + wrap_text(', '.join(flag_keys), ',', line_width)

    _repr_flags_key = None(_repr_flags_key)
    
    def _repr_shdrs(self = None):
        properties = [
            ('Index', 'Name', 'Type', 'Address', 'Offset', 'Size', 'EntSize', 'Flags', 'Link', 'Info', 'Align')]
        for idx, shdr in enumerate(self.shdrs):
            properties.append((idx,) + shdr.get_properties()[0])
        shdrs_string = properties_repr(properties, [
            0], **('sep_rows',))
        return shdrs_string + self._repr_flags_key(len(shdrs_string.split('\n', 1, **('maxsplit',))[0]))

    
    def update_phdr_segments(self = None):
        phdr_table_positional_entry = self.get_phdr_table_positional_entry()
        for phdr in self.phdrs:
            if phdr.p_type == PT_PHDR:
                phdr.p_offset = phdr_table_positional_entry.offset
                phdr.p_filesz = phdr_table_positional_entry.size
            if phdr.is_os_segment_phdr():
                phdr.p_offset = 0
                phdr.p_filesz = phdr_table_positional_entry.end + 1
        for phdr in self.phdrs:
            if phdr.p_type == PT_PHDR:
                data = bytearray()
                for phdr_other in self.phdrs:
                    data += phdr_other.pack()
                self.segments[phdr] = memoryview(data)
            if phdr.is_os_segment_phdr():
                sorted_positional_entries = self.get_positional_entries()
                data = bytearray()
                for positional_entry in sorted_positional_entries:
                    if positional_entry.end <= phdr_table_positional_entry.end:
                        data += self.get_data_to_pack(positional_entry)
                self.segments[phdr] = memoryview(data)

    
    def include_padding_in_cluster(self = None, positional_entry = None):
        return False

    
    def entry_should_go_into_existing_cluster(self = None, cluster_limit = None, cluster = None, positional_entry = ('cluster_limit', ClusterLimits, 'cluster', list[AbstractPositionalData | PositionalData], 'positional_entry', AbstractPositionalData, 'return', bool)):
        if positional_entry.offset <= positional_entry.offset:
            return positional_entry.offset <= cluster_limit.end
        positional_entry.offset <= positional_entry.offset
        return positional_entry.offset

    
    def construct_clusters(self = None, include_phdr_table = None):
        positional_entries = self.get_positional_entries(include_phdr_table, False, True, **('include_phdr_table', 'include_elf_header', 'ignore_voids'))
        start_idx = 1 if positional_entries[0].data_name == PADDING else 0
        clusters = [
            [
                positional_entries[start_idx]]]
        cluster_limits = [
            ClusterLimits(positional_entries[start_idx].offset, positional_entries[start_idx].end)]
        for positional_entry in positional_entries[start_idx + 1:]:
            if not positional_entry.data_name == PADDING and self.include_padding_in_cluster(positional_entry):
                continue
            if self.entry_should_go_into_existing_cluster(cluster_limits[-1], clusters[-1], positional_entry):
                clusters[-1].append(positional_entry)
                if positional_entry.end > cluster_limits[-1].end:
                    cluster_limits[-1] = ClusterLimits(cluster_limits[-1].start, positional_entry.end)
                continue
            cluster_limits.append(ClusterLimits(positional_entry.offset, positional_entry.end))
            clusters.append([
                positional_entry])
        return (clusters, cluster_limits)

    
    def wipe_paddings(self):
        self.paddings = { }

    
    def update_offsets(self = None, positional_entry = None, min_shift_amount = None, include_phdr_table = (True,)):
        (clusters, cluster_limits) = self.construct_clusters(include_phdr_table, **('include_phdr_table',))
        self.wipe_paddings()
        for cluster_idx, cluster in enumerate(clusters):
            for cluster_entry in cluster:
                if (positional_entry.offset, positional_entry.size, positional_entry.data_name) == (cluster_entry.offset, cluster_entry.size, cluster_entry.data_name):
                    self.shift_cluster(cluster_idx, cluster, cluster_limits, min_shift_amount)
                
                if cluster_idx < len(clusters) - 1 and cluster_limits[cluster_idx].end >= cluster_limits[cluster_idx + 1].start:
                    shift_amount = (cluster_limits[cluster_idx].end - cluster_limits[cluster_idx + 1].start) + 1
                    self.shift_cluster(cluster_idx + 1, clusters[cluster_idx + 1], cluster_limits, shift_amount)
        self.fill_voids_with_paddings()

    
    def shift_cluster(self, cluster_idx = None, cluster = None, cluster_limits = None, min_shift_amount = ('cluster_idx', int, 'cluster', list[AbstractPositionalData | PositionalData], 'cluster_limits', list[ClusterLimits], 'min_shift_amount', int, 'return', None)):
        least_common_alignment_multiple = ALIGN_1
        greatest_alignment = ALIGN_1
        for current_entry in cluster:
            current_alignment = current_entry.alignment
            if current_alignment:
                least_common_alignment_multiple = least_common_alignment_multiple * current_alignment // gcd(least_common_alignment_multiple, current_alignment)
            else:
                least_common_alignment_multiple //= gcd(least_common_alignment_multiple, current_alignment)
            if current_alignment and current_entry.offset % current_alignment and current_alignment > greatest_alignment:
                greatest_alignment = current_alignment
        aligned_shift_amount = ceil_to_multiple(min_shift_amount, least_common_alignment_multiple)
    # WARNING: Decompyle incomplete

    
    def align_positional_entry_offset(positional_entry = None):
        pass
    # WARNING: Decompyle incomplete

    align_positional_entry_offset = None(align_positional_entry_offset)
    
    def align_positional_entries(self = None, new_positional_entry = None, idx = None, sorted_positional_entries = ('new_positional_entry', AbstractPositionalData, 'idx', int, 'sorted_positional_entries', list[AbstractPositionalData | PositionalData], 'return', None)):
        self.align_positional_entry_offset(new_positional_entry)
        if new_positional_entry.end >= sorted_positional_entries[idx].offset:
            self.update_offsets(sorted_positional_entries[idx], new_positional_entry.offset + new_positional_entry.size - sorted_positional_entries[idx].offset)
            return None

    
    def insert_positional_entry_into_padding(self = None, idx = None, sorted_positional_entries = None, new_positional_entry = (True,), include_phdr_table = ('idx', int, 'sorted_positional_entries', list[AbstractPositionalData | PositionalData], 'new_positional_entry', AbstractPositionalData, 'include_phdr_table', bool, 'return', None)):
        padding_positional_entry = sorted_positional_entries[idx]
    # WARNING: Decompyle incomplete

    
    def shift_positional_entries(self = None, new_positional_entry = None, include_phdr_table = None):
        greatest_end = 0
        positional_entries = self.get_positional_entries(include_phdr_table, **('include_phdr_table',))
    # WARNING: Decompyle incomplete

    
    def merge_paddings(self = None):
        padding_entries = sorted(list(self.paddings.keys()), operator.attrgetter('offset', 'size'), **('key',))
        if len(padding_entries) > 1:
            current_padding = padding_entries[0]
            for idx in range(len(padding_entries)):
                if idx != len(padding_entries) - 1:
                    next_padding = padding_entries[idx + 1]
                    if next_padding.offset == current_padding.end + 1:
                        current_padding.size += next_padding.size
                        self.paddings[current_padding] = bytearray(self.paddings[current_padding]).ljust(current_padding.size, PAD_BYTE_0)
                        del self.paddings[next_padding]
                        continue
                    if next_padding.offset < next_padding.offset or next_padding.offset < current_padding.end:
                        pass
                    else:
                        current_padding.offset
                elif not next_padding.end < current_padding.end:
                    current_padding.size += next_padding.end - current_padding.end
                    self.paddings[current_padding] = bytearray(self.paddings[current_padding]).ljust(next_padding.end - current_padding.end, PAD_BYTE_0)
                del self.paddings[next_padding]
            if next_padding.offset == current_padding.offset:
                del self.paddings[current_padding if current_padding.size < next_padding.size else next_padding]
                continue
            current_padding = next_padding
            continue
        return None

    
    def add_padding_entry(self = None, offset = None, size = None, data = (None,)):
        if size > 0:
            self.paddings[PositionalData(offset, size, ALIGN_1, PADDING)] = PAD_BYTE_0 * size if not data else data
        self.merge_paddings()

    
    def fill_voids_with_paddings(self = None):
        greatest_end = 0
        sorted_positional_entries = self.get_positional_entries(True, **('ignore_voids',))
        for idx, positional_entry in enumerate(sorted_positional_entries):
            if idx != len(sorted_positional_entries) - 1:
                next_entry = sorted_positional_entries[idx + 1]
                if positional_entry.end > greatest_end and positional_entry.size:
                    greatest_end = positional_entry.end
                if next_entry.offset > greatest_end + 1:
                    self.add_padding_entry(greatest_end + 1, next_entry.offset - greatest_end - 1)
        last_entry = self.get_positional_entries()[-1]
    # WARNING: Decompyle incomplete

    
    def remove_segment(self = None, phdr = None):
        pass
    # WARNING: Decompyle incomplete

    
    def add_segment(self = None, phdr = None, data = None, phdr_idx = (0,)):
        pass
    # WARNING: Decompyle incomplete

    
    def remove_sections(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_image_properties(self = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_image_format(self = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    
    def pil_split(self = None):
        if len(self.phdrs) > 100:
            raise RuntimeError(f'''Cannot PIL split an {self.class_type_string()} image containing more than 100 segments.''')
    # WARNING: Decompyle incomplete

    
    def write_pil_split_image(self = None, stem = None, outdir = None, cmd_line_arg = ('stem', str, 'outdir', Path, 'cmd_line_arg', str, 'return', None)):
        old_b_files = sorted(glob(f'''{outdir}/{stem}.b**'''))
        for old_b_file in old_b_files:
            log_info(f'''Deleting {old_b_file} file.''')
            delete_file(old_b_file)
        pil_image = self.pil_split()
        mdt_file = outdir / f'''{stem}.mdt'''
        log_info(f'''Writing .mdt file: {mdt_file}.''')
        write_cmdline_file(mdt_file, pil_image.mdt, cmd_line_arg)
        for idx, b_file in enumerate(pil_image.b_files):
            b_file_name = outdir / f'''{stem}.b{idx:02}'''
            log_info(f'''Writing {b_file_name} file.''')
            write_cmdline_file(b_file_name, b_file, cmd_line_arg)

    __classcell__ = None

