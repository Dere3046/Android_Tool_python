"""ELF Image Parser - Full implementation based on decompiled analysis."""

import operator
import struct
from math import gcd
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Sequence, Tuple, Union

from common.data.base_parser import DumpDict
from common.data.data import (
    ceil_to_multiple, extract_data_or_fail, is_congruent,
    properties_repr, wrap_text
)
from common.data.defines import PAD_BYTE_0
from common.logging.logger import log_debug, log_info
from common.parser.elf.bit32.elf_header import ELFHeader32
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit32.section_header import SectionHeader32
from common.parser.elf.bit64.elf_header import ELFHeader64
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.bit64.section_header import SectionHeader64
from common.parser.elf.defines import (
    ALIGN_1, ALIGN_4, ELFCLASS32, ELFCLASS64, ELF_HEADER, ELF32_PHDR_SIZE, ELF64_PHDR_SIZE,
    PADDING, PHDR_TABLE, PT_INTERP, PT_LOAD, PT_ONE_SHOT_HASH,
    PT_PHDR, SHDR_TABLE, SHN_UNDEF, SHT_DYNAMIC, SHT_DYNSYM,
    SHT_HASH, SHT_NOBITS, SHT_NULL, SHT_STRTAB, SH_FLAGS, UNALIGNED,
)
from common.parser.elf.elf_header import ELFHeaderCommon
from common.parser.elf.positional_data import AbstractPositionalData, PositionalData
from common.parser.elf.section_header import SECTION_HEADER_CLASSES
from common.parser.hash_segment.defines import AUTHORITY_OEM
from common.parser.parser_image_info_interface import (
    ELF_PROPERTIES, ImageFormatType, ImageInfoInterface, ImageProperties
)
from common.utils import delete_file, write_cmdline_file
from profile.schema import ELFProperties, ImageFormat


class ClusterLimits(NamedTuple):
    """Cluster limits definition."""
    start: int
    end: int


class PILSplitImage(NamedTuple):
    """PIL split image definition."""
    mdt: bytearray
    b_files: List[Union[memoryview, bytearray]]


ELF_HEADER_CLASSES = {
    ELFCLASS32: ELFHeader32,
    ELFCLASS64: ELFHeader64
}


class ELF(ImageInfoInterface):
    """ELF image parser."""

    def __init__(self, data: Optional[Union[memoryview, bytearray]] = None, **kwargs):
        """Initialize ELF object."""
        self.elf_header: Optional[Union[ELFHeader32, ELFHeader64]] = None
        self.phdrs: List[Union[ProgramHeader32, ProgramHeader64]] = []
        self.shdrs: List[Union[SectionHeader32, SectionHeader64]] = []
        self.segments: Dict[Union[ProgramHeader32, ProgramHeader64], memoryview] = {}
        self.sections: Dict[Union[SectionHeader32, SectionHeader64], memoryview] = {}
        self.paddings: Dict[PositionalData, bytes] = {}

        self.data = data

        if data is not None:
            self._parse_elf_header_and_phdrs(data)

    def _parse_elf_header_and_phdrs(self, data: Union[memoryview, bytearray]) -> None:
        """Parse ELF header and program header table."""
        if len(data) < 16:
            raise ValueError("Data too small for ELF header")

        if data[:4] != b'\x7fELF':
            raise ValueError("Invalid ELF magic number")

        elf_class = data[4]

        if elf_class == ELFCLASS32:
            self.elf_header = ELFHeader32(data[:52])
            phdr_class = ProgramHeader32
            phdr_size = ELF32_PHDR_SIZE
        elif elf_class == ELFCLASS64:
            self.elf_header = ELFHeader64(data[:64])
            phdr_class = ProgramHeader64
            phdr_size = ELF64_PHDR_SIZE
        else:
            raise ValueError(f"Unsupported ELF class: {elf_class}")

        e_phoff = self.elf_header.e_phoff
        e_phnum = self.elf_header.e_phnum
        e_phentsize = self.elf_header.e_phentsize

        for i in range(e_phnum):
            phdr_offset = e_phoff + i * e_phentsize
            phdr_data = data[phdr_offset:phdr_offset + phdr_size]
            if len(phdr_data) == phdr_size:
                phdr = phdr_class(phdr_data)
                self.phdrs.append(phdr)

    @property
    def phdr_table_offset(self) -> int:
        """Get program header table offset."""
        if self.elf_header is None:
            raise AssertionError("ELF header not loaded")
        return self.elf_header.e_phoff

    def unpack(self, data: Union[memoryview, bytearray]) -> None:
        """Unpack ELF image data."""
        self._parse_elf_header_and_phdrs(data)

        if self.elf_header is None:
            raise AssertionError("ELF header not loaded")

        shdr_class = SECTION_HEADER_CLASSES[self.elf_header.e_ident_class]

        for shdr_index in range(self.elf_header.e_shnum):
            if self.elf_header.e_shentsize < shdr_class.get_size():
                raise RuntimeError(
                    f"{self.class_type_string()} has invalid Section Header entry size"
                )

            shdr_offset = (self.elf_header.e_shoff +
                          shdr_index * self.elf_header.e_shentsize)
            shdr_data = data[shdr_offset:shdr_offset + shdr_class.get_size()]
            shdr = shdr_class(shdr_data)
            self.shdrs.append(shdr)

        sorted_phdrs = sorted(
            self.phdrs,
            key=operator.attrgetter('p_offset', 'p_filesz')
        )

        for idx, phdr in enumerate(sorted_phdrs):
            try:
                if phdr.p_filesz:
                    segment_data = extract_data_or_fail(
                        data, phdr.p_filesz, phdr.p_offset
                    )
                else:
                    segment_data = memoryview(b'')
                self.segments[phdr] = segment_data
            except RuntimeError:
                raise RuntimeError(
                    f"Data of segment is beyond end of {self.class_type_string()}"
                )

        for shdr in self.shdrs:
            try:
                if shdr.sh_size and shdr.sh_type not in (SHT_NOBITS, SHT_NULL):
                    section_data = extract_data_or_fail(
                        data, shdr.sh_size, shdr.sh_offset
                    )
                else:
                    section_data = memoryview(b'')
                self.sections[shdr] = section_data
            except RuntimeError:
                raise RuntimeError(
                    f"Data of section is beyond end of {self.class_type_string()}"
                )

        self.set_section_names()

        sorted_positional_entries = self.get_positional_entries(ignore_voids=True)
        greatest_unpacked_offset = 0

        for idx, positional_entry in enumerate(sorted_positional_entries):
            has_data = True

            if isinstance(positional_entry, (ProgramHeader32, ProgramHeader64)):
                has_data = bool(self.segments.get(positional_entry))
            elif isinstance(positional_entry, (SectionHeader32, SectionHeader64)):
                has_data = bool(self.sections.get(positional_entry))

            if greatest_unpacked_offset < positional_entry.offset():
                padding_size = positional_entry.offset() - greatest_unpacked_offset
                padding_data = bytes(data[greatest_unpacked_offset:positional_entry.offset()])
                self.add_padding_entry(
                    greatest_unpacked_offset, padding_size, padding_data
                )

            if positional_entry.end() >= greatest_unpacked_offset and has_data:
                greatest_unpacked_offset = positional_entry.end()

            if idx == len(sorted_positional_entries) - 1:
                if len(data) > greatest_unpacked_offset:
                    padding_size = len(data) - greatest_unpacked_offset
                    padding_data = bytes(data[greatest_unpacked_offset:])
                    self.add_padding_entry(
                        greatest_unpacked_offset, padding_size, padding_data
                    )

        return None

    def validate_before_operation(self, validate_sections: bool = True,
                                 is_second_authority: bool = False) -> None:
        """Validate ELF structure integrity."""
        if self.elf_header is None:
            raise AssertionError("ELF header not loaded")

        self.elf_header.validate_before_operation()

        for phdr in self.phdrs:
            phdr.validate_before_operation()

            if is_second_authority:
                if phdr.p_type != PT_PHDR and phdr.is_os_segment_phdr():
                    if phdr.overlaps_with(self.elf_header):
                        raise RuntimeError(f"{phdr} overlaps with ELF Header.")
                    if phdr.overlaps_with(self.get_phdr_table_positional_entry()):
                        raise RuntimeError(f"{phdr} overlaps with Program Header Table.")

        load_phdr = None
        interp_phdr = None
        phdr_phdr = None

        for phdr in self.phdrs:
            if phdr.p_type == PT_LOAD:
                load_phdr = phdr
            elif phdr.p_type == PT_INTERP:
                if load_phdr is not None:
                    raise RuntimeError(
                        "PT_LOAD Program Header must not appear before PT_INTERP Program Header."
                    )
                if interp_phdr is not None:
                    raise RuntimeError(
                        f"PT_INTERP Program Header must not appear multiple times in {self.class_type_string()}."
                    )
                interp_phdr = phdr
            elif phdr.p_type == PT_PHDR:
                if load_phdr is not None:
                    raise RuntimeError(
                        "PT_LOAD Program Header must not appear before PT_PHDR Program Header."
                    )
                if phdr_phdr is not None:
                    raise RuntimeError(
                        f"PT_PHDR Program Header must not appear multiple times in {self.class_type_string()}."
                    )
                phdr_phdr = phdr

        if phdr_phdr is not None:
            if phdr_phdr.p_offset != self.elf_header.e_phoff:
                raise RuntimeError(
                    "Offset of Program Header Table defined in ELF Header and "
                    "Program Header of type PT_PHDR do not match."
                )
            if phdr_phdr.p_filesz != self.elf_header.e_phnum * self.elf_header.e_phentsize:
                raise RuntimeError(
                    "Size of Program Header Table defined in ELF Header and "
                    "Program Header of type PT_PHDR do not match."
                )

        if validate_sections:
            hash_shdr = None
            dynamic_shdr = None
            dynsym_shdr = None

            sorted_shdrs = sorted(
                self.shdrs,
                key=operator.attrgetter('sh_offset', 'sh_size')
            )

            for idx, shdr in enumerate(sorted_shdrs):
                shdr.validate_before_operation()

                if shdr.sh_type == SHT_HASH:
                    if hash_shdr is not None:
                        raise RuntimeError(
                            f"SHT_HASH Section Header must not appear multiple times in {self.class_type_string()}."
                        )
                    hash_shdr = shdr
                elif shdr.sh_type == SHT_DYNAMIC:
                    if dynamic_shdr is not None:
                        raise RuntimeError(
                            f"SHT_DYNAMIC Section Header must not appear multiple times in {self.class_type_string()}."
                        )
                    dynamic_shdr = shdr
                elif shdr.sh_type == SHT_DYNSYM:
                    if dynsym_shdr is not None:
                        raise RuntimeError(
                            f"SHT_DYNSYM Section Header must not appear multiple times in {self.class_type_string()}."
                        )
                    dynsym_shdr = shdr

                if idx > 0:
                    prev_shdr = sorted_shdrs[idx - 1]
                    if prev_shdr.sh_offset + prev_shdr.sh_size > shdr.sh_offset:
                        raise RuntimeError(
                            f"Sections must not overlap in {self.class_type_string()}"
                        )

        return None

    def pack(self) -> memoryview:
        """Pack ELF image data."""
        return memoryview(self.get_data_from_entries(self.get_positional_entries()))

    def get_data_from_entries(self, entries: List[PositionalData]) -> bytearray:
        """Merge data from multiple positional entries."""
        data = bytearray()
        if not entries:
            return data

        shift = entries[0].offset()

        for positional_entry in entries:
            offset = positional_entry.offset() - shift
            end = positional_entry.end() - shift
            data_to_pack = self.get_data_to_pack(positional_entry)

            if data_to_pack:
                if len(data_to_pack) != positional_entry.size():
                    raise RuntimeError(
                        f"Size of data to pack, {len(data_to_pack)} bytes, "
                        f"does not match size declared by entry:\n{positional_entry}."
                    )

                if offset > len(data):
                    raise RuntimeError(
                        f"There is a gap of {offset - len(data)} bytes before entry:\n"
                        f"{positional_entry}."
                    )

                if end < len(data):
                    if data_to_pack != memoryview(data)[offset:end + 1]:
                        raise RuntimeError(
                            f"Encapsulated data mismatches already packed data for entry:\n"
                            f"{positional_entry}."
                        )
                elif end >= len(data):
                    if offset < len(data):
                        if data_to_pack[:len(data) - offset] != memoryview(data)[offset:]:
                            raise RuntimeError(
                                f"Overlapping data mismatches already packed data for entry:\n"
                                f"{positional_entry}."
                            )
                        data_to_pack = data_to_pack[len(data) - offset:]

                    data.extend(data_to_pack)

        return data

    def get_data_to_pack(self, positional_entry: PositionalData) -> Union[memoryview, bytes]:
        """Get data to pack for a positional entry."""
        if positional_entry is self.elf_header:
            return self.elf_header.pack()

        if self.elf_header is not None and self.elf_header.e_phnum > 0:
            phdr_table_offset = self.elf_header.e_phoff
            phdr_table_size = self.elf_header.e_phnum * self.elf_header.e_phentsize
            if (positional_entry.offset() == phdr_table_offset and
                positional_entry.size() == phdr_table_size):
                data = bytearray()
                for phdr in self.phdrs:
                    data.extend(phdr.pack())
                return memoryview(data)

        for phdr in self.phdrs:
            if (phdr.p_filesz > 0 and
                positional_entry.offset() == phdr.p_offset and
                positional_entry.size() == phdr.p_filesz):
                return self.segments.get(phdr, memoryview(b''))

        if self.elf_header is not None and self.elf_header.e_shnum > 0:
            shdr_table_offset = self.elf_header.e_shoff
            shdr_table_size = self.elf_header.e_shnum * self.elf_header.e_shentsize
            if (positional_entry.offset() == shdr_table_offset and
                positional_entry.size() == shdr_table_size):
                data = bytearray()
                for shdr in self.shdrs:
                    data.extend(shdr.pack())
                return memoryview(data)

        for shdr in self.shdrs:
            if (shdr.sh_size > 0 and shdr.sh_type not in (SHT_NOBITS, SHT_NULL) and
                positional_entry.offset() == shdr.sh_offset and
                positional_entry.size() == shdr.sh_size):
                return self.sections.get(shdr, memoryview(b''))

        for padding_entry, padding_data in self.paddings.items():
            if (positional_entry.offset() == padding_entry.offset() and
                positional_entry.size() == padding_entry.size()):
                return padding_data

        return b''

    def get_positional_entries(self, ignore_voids: bool = False) -> List[PositionalData]:
        """Get all positional entries."""
        entries = []

        if self.elf_header is not None:
            entries.append(self.elf_header)

        if self.elf_header is not None and self.elf_header.e_phnum > 0:
            phdr_table_entry = PositionalData()
            phdr_table_entry._offset = self.elf_header.e_phoff
            phdr_table_entry._size = self.elf_header.e_phnum * self.elf_header.e_phentsize
            phdr_table_entry._alignment = 1
            phdr_table_entry._address = 0
            phdr_table_entry._mem_size = phdr_table_entry._size
            entries.append(phdr_table_entry)

        for phdr in self.phdrs:
            if phdr.p_filesz > 0:
                segment_entry = PositionalData()
                segment_entry._offset = phdr.p_offset
                segment_entry._size = phdr.p_filesz
                segment_entry._alignment = phdr.p_align if phdr.p_align > 0 else 1
                segment_entry._address = phdr.p_paddr
                segment_entry._mem_size = phdr.p_memsz
                entries.append(segment_entry)

        if self.elf_header is not None and self.elf_header.e_shnum > 0:
            shdr_table_entry = PositionalData()
            shdr_table_entry._offset = self.elf_header.e_shoff
            shdr_table_entry._size = self.elf_header.e_shnum * self.elf_header.e_shentsize
            shdr_table_entry._alignment = 1
            shdr_table_entry._address = 0
            shdr_table_entry._mem_size = shdr_table_entry._size
            entries.append(shdr_table_entry)

        for shdr in self.shdrs:
            if shdr.sh_size > 0 and shdr.sh_type not in (SHT_NOBITS, SHT_NULL):
                section_entry = PositionalData()
                section_entry._offset = shdr.sh_offset
                section_entry._size = shdr.sh_size
                section_entry._alignment = shdr.sh_addralign if shdr.sh_addralign > 0 else 1
                section_entry._address = shdr.sh_addr
                section_entry._mem_size = shdr.sh_size
                entries.append(section_entry)

        entries.extend(self.paddings.keys())

        sorted_entries = sorted(
            entries,
            key=lambda e: (e.offset(), e.size())
        )

        if ignore_voids:
            sorted_entries = [
                e for e in sorted_entries
                if not (isinstance(e, PositionalData) and e.data_name() == PADDING and e.size() == 0)
            ]

        return sorted_entries

    def add_padding_entry(self, offset: int, size: int, data: bytes) -> None:
        """Add padding entry."""
        if size <= 0:
            return

        padding_entry = PositionalData()
        padding_entry._offset = offset
        padding_entry._size = size
        padding_entry._alignment = ALIGN_1
        padding_entry._address = 0
        padding_entry._mem_size = size

        self.paddings[padding_entry] = bytes(data)

    def fill_voids_with_paddings(self) -> None:
        """Fill voids with padding."""
        self.paddings.clear()

        entries = self.get_positional_entries()
        if not entries:
            return

        sorted_entries = sorted(entries, key=lambda e: e.offset())

        for i in range(1, len(sorted_entries)):
            prev_entry = sorted_entries[i - 1]
            curr_entry = sorted_entries[i]

            gap_start = prev_entry.offset() + prev_entry.size()
            gap_end = curr_entry.offset()

            if gap_end > gap_start:
                gap_size = gap_end - gap_start
                self.add_padding_entry(gap_start, gap_size, b'\x00' * gap_size)

    def add_segment(self, phdr: Union[ProgramHeader32, ProgramHeader64],
                   data: Union[memoryview, bytearray, bytes]) -> None:
        """Add new program segment."""
        phdr.validate_before_operation()

        for entry in self.get_positional_entries():
            if self._entries_overlap(phdr, entry):
                raise RuntimeError(f"New segment overlaps with existing entry: {entry}")

        self.phdrs.append(phdr)
        self.segments[phdr] = memoryview(data)
        self.fill_voids_with_paddings()
        self.update_phdr_segments()

    def remove_segment(self, phdr: Union[ProgramHeader32, ProgramHeader64]) -> None:
        """Remove program segment."""
        if phdr not in self.phdrs:
            raise ValueError(f"Program header not found: {phdr}")

        self.phdrs.remove(phdr)

        if phdr in self.segments:
            del self.segments[phdr]

        self.fill_voids_with_paddings()
        self.update_phdr_segments()

    def _entries_overlap(self, entry1: PositionalData, entry2: PositionalData) -> bool:
        """Check if two entries overlap."""
        start1 = entry1.offset()
        end1 = start1 + entry1.size()
        start2 = entry2.offset()
        end2 = start2 + entry2.size()

        return not (end1 <= start2 or end2 <= start1)

    def update_phdr_segments(self) -> None:
        """Update program header table segment."""
        pass

    def set_section_names(self) -> None:
        """Set section names from string table."""
        if self.elf_header is None:
            return

        shstrndx = self.elf_header.e_shstrndx
        if shstrndx == SHN_UNDEF or shstrndx >= len(self.shdrs):
            return

        shstrtab_hdr = self.shdrs[shstrndx]
        if shstrtab_hdr.sh_type != SHT_STRTAB:
            return

        strtab_data = self.sections.get(shstrtab_hdr, b'')

        for shdr in self.shdrs:
            if shdr.sh_name < len(strtab_data):
                end_idx = strtab_data.find(b'\x00', shdr.sh_name)
                if end_idx == -1:
                    end_idx = len(strtab_data)
                name = strtab_data[shdr.sh_name:end_idx].decode('utf-8', errors='replace')
                shdr._name = name

    def get_phdr_table_positional_entry(self) -> PositionalData:
        """Get program header table positional entry."""
        if self.elf_header is None:
            raise AssertionError("ELF header not loaded")

        entry = PositionalData()
        entry._offset = self.elf_header.e_phoff
        entry._size = self.elf_header.e_phnum * self.elf_header.e_phentsize
        entry._alignment = ALIGN_1
        entry._address = 0
        entry._mem_size = entry._size

        return entry

    def get_shdr_table_positional_entry(self) -> PositionalData:
        """Get section header table positional entry."""
        if self.elf_header is None:
            raise AssertionError("ELF header not loaded")

        entry = PositionalData()
        entry._offset = self.elf_header.e_shoff
        entry._size = self.elf_header.e_shnum * self.elf_header.e_shentsize
        entry._alignment = ALIGN_1
        entry._address = 0
        entry._mem_size = entry._size

        return entry

    def get_shdr_positional_entries(self) -> List[PositionalData]:
        """Get section header positional entries."""
        return list(self.shdrs)

    def get_paddings_entries(self) -> List[PositionalData]:
        """Get padding entries."""
        return list(self.paddings.keys())

    def get_greatest_offset(self) -> int:
        """Get greatest offset from all entries."""
        entries = self.get_positional_entries()
        if not entries:
            return 0

        return max(e.offset() + e.size() for e in entries)

    def wipe_paddings(self) -> None:
        """Clear all padding entries."""
        self.paddings.clear()

    def update_offsets(self) -> None:
        """Update all positional entry offsets."""
        pass

    def shift_cluster(self, cluster: List[PositionalData], delta: int) -> None:
        """Shift cluster by delta."""
        for entry in cluster:
            if isinstance(entry, (ProgramHeader32, ProgramHeader64)):
                entry.p_offset += delta
            elif isinstance(entry, (SectionHeader32, SectionHeader64)):
                entry.sh_offset += delta
            elif isinstance(entry, PositionalData):
                entry._offset += delta

    def align_positional_entry_offset(self, positional_entry: PositionalData,
                                      alignment: int) -> None:
        """Align positional entry to boundary."""
        if alignment <= 0:
            return

        current_offset = positional_entry.offset()
        aligned_offset = ceil_to_multiple(current_offset, alignment)
        delta = aligned_offset - current_offset

        if isinstance(positional_entry, (ProgramHeader32, ProgramHeader64)):
            positional_entry.p_offset += delta
        elif isinstance(positional_entry, (SectionHeader32, SectionHeader64)):
            positional_entry.sh_offset += delta
        elif isinstance(positional_entry, PositionalData):
            positional_entry._offset += delta

    def align_positional_entries(self, alignment: int) -> None:
        """Align all positional entries."""
        for entry in self.get_positional_entries():
            self.align_positional_entry_offset(entry, alignment)

    def insert_positional_entry_into_padding(self, padding_entry: PositionalData,
                                             new_entry: PositionalData) -> bool:
        """Try to insert new entry into padding space."""
        padding_start = padding_entry.offset()
        new_entry_size = new_entry.size()

        if padding_entry.size() < new_entry_size:
            return False

        if isinstance(new_entry, (ProgramHeader32, ProgramHeader64)):
            new_entry.p_offset = padding_start
        elif isinstance(new_entry, (SectionHeader32, SectionHeader64)):
            new_entry.sh_offset = padding_start
        elif isinstance(new_entry, PositionalData):
            new_entry._offset = padding_start

        remaining_size = padding_entry.size() - new_entry_size
        if remaining_size > 0:
            padding_entry._offset += new_entry_size
            padding_entry._size = remaining_size
        else:
            if padding_entry in self.paddings:
                del self.paddings[padding_entry]

        return True

    def shift_positional_entries(self, start_offset: int, delta: int) -> None:
        """Shift positional entries from start offset."""
        for entry in self.get_positional_entries():
            if entry.offset() >= start_offset:
                if isinstance(entry, (ProgramHeader32, ProgramHeader64)):
                    entry.p_offset += delta
                elif isinstance(entry, (SectionHeader32, SectionHeader64)):
                    entry.sh_offset += delta
                elif isinstance(entry, PositionalData):
                    entry._offset += delta

    def merge_paddings(self) -> None:
        """Merge adjacent padding entries."""
        if not self.paddings:
            return

        padding_entries = sorted(
            self.paddings.keys(),
            key=lambda e: e.offset()
        )

        current_padding = None

        for entry in padding_entries:
            if current_padding is None:
                current_padding = entry
                continue

            if entry.offset() == current_padding.offset() + current_padding.size():
                merged_data = bytearray(
                    self.paddings[current_padding] + self.paddings[entry]
                )
                current_padding._size += entry.size()
                self.paddings[current_padding] = bytes(merged_data)
                del self.paddings[entry]
            else:
                current_padding = entry

    def remove_sections(self, sections_to_remove: List[Union[SectionHeader32, SectionHeader64]]) -> None:
        """Remove specified sections."""
        for shdr in sections_to_remove:
            if shdr in self.shdrs:
                self.shdrs.remove(shdr)
            if shdr in self.sections:
                del self.sections[shdr]

        self.fill_voids_with_paddings()

    def flatten_segment(self, phdr: Union[ProgramHeader32, ProgramHeader64]) -> memoryview:
        """Flatten program segment data."""
        segment_data = self.segments.get(phdr, memoryview(b''))
        return memoryview(segment_data)

    def remove_elf_hdr_phdr_table_overlaps(self) -> None:
        """Remove ELF header and program header table overlaps."""
        pass

    def construct_clusters(self, include_phdr_table: bool = False) -> Tuple[List[List[PositionalData]], List[ClusterLimits]]:
        """Group positional entries into clusters."""
        clusters = []
        cluster_limits = []

        entries = self.get_positional_entries()
        if not entries:
            return clusters, cluster_limits

        non_padding_entries = [
            e for e in entries
            if e.data_name() != PADDING
        ]

        if not non_padding_entries:
            return clusters, cluster_limits

        current_cluster = [non_padding_entries[0]]
        current_limit = ClusterLimits(
            start=non_padding_entries[0].offset(),
            end=non_padding_entries[0].offset() + non_padding_entries[0].size()
        )

        for entry in non_padding_entries[1:]:
            if self.entry_should_go_into_existing_cluster(current_limit, current_cluster, entry):
                current_cluster.append(entry)
                current_limit = ClusterLimits(
                    start=current_limit.start,
                    end=max(current_limit.end, entry.offset() + entry.size())
                )
            else:
                clusters.append(current_cluster)
                cluster_limits.append(current_limit)
                current_cluster = [entry]
                current_limit = ClusterLimits(
                    start=entry.offset(),
                    end=entry.offset() + entry.size()
                )

        if current_cluster:
            clusters.append(current_cluster)
            cluster_limits.append(current_limit)

        return clusters, cluster_limits

    def entry_should_go_into_existing_cluster(self, cluster_limit: ClusterLimits,
                                              cluster: List[PositionalData],
                                              positional_entry: PositionalData) -> bool:
        """Check if entry should go into existing cluster."""
        entry_start = positional_entry.offset()
        return entry_start <= cluster_limit.end

    def include_padding_in_cluster(self, positional_entry: PositionalData) -> bool:
        """Check if padding should be included in cluster."""
        return False

    def get_dump_files(self, directory: str) -> DumpDict:
        """Get dump files dictionary."""
        dump_files = DumpDict()
        dump_files['segments'] = {}
        dump_files['sections'] = {}
        dump_files['shdr_table'] = {}

        return dump_files

    def _repr_elf(self) -> str:
        """Get ELF string representation."""
        lines = []
        lines.append("ELF Header:")
        if self.elf_header:
            lines.append(f"  Type: {self.elf_header.e_type}")
            lines.append(f"  Machine: {self.elf_header.e_machine}")
            lines.append(f"  Entry: 0x{self.elf_header.e_entry:x}")

        lines.append("\nProgram Headers:")
        for phdr in self.phdrs:
            props = phdr.get_properties()
            for prop in props:
                lines.append(f"  {prop}")

        lines.append("\nSection Headers:")
        lines.append(self._repr_shdrs())

        return '\n'.join(lines)

    def __repr__(self) -> str:
        """Get string representation."""
        return self._repr_elf()

    @staticmethod
    def _repr_flags_key(line_width: int = 80) -> str:
        """Get flags key string."""
        return "Flags: W=Write, A=Alloc, X=Execute, M=Merge, S=Strings, I=Info, L=Link Order, O=OS Nonconforming, G=Group, T=TLS"

    def _repr_shdrs(self) -> str:
        """Get section headers table string."""
        lines = []
        lines.append("  [Nr] Name              Type            Addr     Off    Size     ES Flg Lk Inf Al")

        for idx, shdr in enumerate(self.shdrs):
            name = getattr(shdr, '_name', '')
            if len(name) > 17:
                name = name[:14] + '...'

            type_str = f"0x{shdr.sh_type:08x}"
            addr = f"0x{shdr.sh_addr:08x}"
            off = f"0x{shdr.sh_offset:06x}"
            size = f"0x{shdr.sh_size:06x}"
            es = f"0x{shdr.sh_entsize:02x}"
            flags = shdr._repr_sh_flags() if hasattr(shdr, '_repr_sh_flags') else ''

            line = f"  [{idx:2d}] {name:<17} {type_str:<15} {addr} {off} {size} {es} {flags:<5}"
            lines.append(line)

        return '\n'.join(lines)

    def get_image_properties(self, authority: str = AUTHORITY_OEM) -> ImageProperties:
        """Get image properties."""
        props = {}
        props['elf_class'] = self.elf_header.e_ident_class if self.elf_header else None
        props['machine_type'] = self.elf_header.e_machine if self.elf_header else None
        props['entry_point'] = self.elf_header.e_entry if self.elf_header else None
        props['num_segments'] = len(self.phdrs)
        props['num_sections'] = len(self.shdrs)

        return ImageProperties(
            image_type=ImageFormatType.ELF,
            properties=props
        )

    def get_image_format(self, authority: str = AUTHORITY_OEM) -> List[ImageFormat]:
        """Get image format list."""
        return [ImageFormat(format_type=ImageFormatType.ELF)]

    def pil_split(self) -> PILSplitImage:
        """Perform PIL split."""
        mdt_data = bytearray()
        b_files = []

        for phdr, data in self.segments.items():
            if phdr.p_type == PT_LOAD and data:
                b_files.append(data)

        return PILSplitImage(mdt=mdt_data, b_files=b_files)

    def write_pil_split_image(self, path: Union[str, Path]) -> None:
        """Write PIL split files."""
        pil_image = self.pil_split()
        path = Path(path)

        mdt_path = path.with_suffix('.mdt')
        with open(mdt_path, 'wb') as f:
            f.write(pil_image.mdt)

        for i, b_file in enumerate(pil_image.b_files):
            b_path = path.with_suffix(f'.b{i:03d}')
            with open(b_path, 'wb') as f:
                f.write(bytes(b_file))

    @classmethod
    def is_type(cls, data: Union[memoryview, bytearray]) -> bool:
        """Check if data is ELF image."""
        if len(data) < 16:
            return False

        return data[:4] == b'\x7fELF'
