"""ELF with hash table segment implementation."""

import struct
from typing import Any, Optional, Union

from common.parser.elf.elf import ELF
from common.parser.elf.defines import (
    ELFCLASS64, PT_LOAD, PT_ONE_SHOT_HASH,
    SHT_NOBITS, SHT_NULL,
)
from common.parser.elf_with_hash_segment.hash_table_segment_header import HashTableSegmentHeaderCommon
from common.parser.hash_segment.defines import AUTHORITY_OEM
from common.parser.parser_image_info_interface import ImageFormatType, ImageProperties
from profile.schema import ImageFormat


class HashTableSegmentCommon:
    """Hash table segment common base."""

    def __init__(self, data=None, **kwargs):
        self.header = None
        self.common_metadata = memoryview(b'')
        self.qti_metadata = memoryview(b'')
        self.oem_metadata = memoryview(b'')
        self.hash_table = memoryview(b'')

    def pack(self):
        if self.header:
            header_data = self.header.pack()
        else:
            header_data = b''
        return header_data + bytes(self.common_metadata) + bytes(self.qti_metadata) + bytes(self.oem_metadata) + bytes(self.hash_table)


class ELFWithHashTableSegment(ELF, HashTableSegmentCommon):
    """ELF with hash table segment."""

    def __init__(self, data=None, **kwargs):
        self.hash_table_segment_phdr = None
        self.hash_table_segment_idx = None
        ELF.__init__(self, data, **kwargs)
        HashTableSegmentCommon.__init__(self, data, **kwargs)

    @classmethod
    def hash_segment_type(cls):
        return "ELF"

    def image_type_string(self):
        if self.elf_header is None:
            raise AssertionError("ELF header not loaded")
        elf_class = "64" if self.elf_header.e_ident_class == ELFCLASS64 else "32"
        return f"{elf_class}-bit {self.hash_segment_type()}"

    def unpack(self, data):
        ELF.unpack(self, data)
        self._parse_hash_table_segment(data)

    def _parse_hash_table_segment(self, data):
        hash_phdr = None
        for phdr in self.phdrs:
            os_type = (phdr.p_flags & 0x07000000) >> 24
            if os_type == 2:
                hash_phdr = phdr
                break

        if hash_phdr is None:
            for phdr in self.phdrs:
                if phdr.p_type == PT_ONE_SHOT_HASH:
                    hash_phdr = phdr
                    break

        if hash_phdr is None:
            return

        self.hash_table_segment_phdr = hash_phdr

        hash_offset = hash_phdr.p_offset
        hash_size = hash_phdr.p_filesz

        if hash_offset + hash_size > len(data):
            return

        hash_data = data[hash_offset:hash_offset + hash_size]

        if len(hash_data) >= 40:
            self.header = HashTableSegmentHeaderCommon()
            self.header.reserved = struct.unpack('<I', hash_data[0:4])[0]
            self.header.version = struct.unpack('<I', hash_data[4:8])[0]
            self.header.common_metadata_size = struct.unpack('<I', hash_data[8:12])[0]
            self.header.qti_metadata_size = struct.unpack('<I', hash_data[12:16])[0]
            self.header.oem_metadata_size = struct.unpack('<I', hash_data[16:20])[0]
            self.header.hash_table_size = struct.unpack('<I', hash_data[20:24])[0]
            self.header.qti_sig_size = struct.unpack('<I', hash_data[24:28])[0]
            self.header.qti_cert_chain_size = struct.unpack('<I', hash_data[28:32])[0]
            self.header.oem_sig_size = struct.unpack('<I', hash_data[32:36])[0]
            self.header.oem_cert_chain_size = struct.unpack('<I', hash_data[36:40])[0]

            header_size = 40
            offset = header_size

            if self.header.common_metadata_size > 0 and offset + self.header.common_metadata_size <= len(hash_data):
                self.common_metadata = hash_data[offset:offset + self.header.common_metadata_size]
                offset += self.header.common_metadata_size

            if self.header.qti_metadata_size > 0 and offset + self.header.qti_metadata_size <= len(hash_data):
                self.qti_metadata = hash_data[offset:offset + self.header.qti_metadata_size]
                offset += self.header.qti_metadata_size

            if self.header.oem_metadata_size > 0 and offset + self.header.oem_metadata_size <= len(hash_data):
                self.oem_metadata = hash_data[offset:offset + self.header.oem_metadata_size]
                offset += self.header.oem_metadata_size

            if self.header.hash_table_size > 0 and offset + self.header.hash_table_size <= len(hash_data):
                self.hash_table = hash_data[offset:offset + self.header.hash_table_size]

    def __repr__(self):
        lines = []
        lines.append("ELF Header:")
        if self.elf_header:
            data_str = "2's complement, little endian" if self.elf_header.e_ident[5] == 1 else "2's complement, big endian"
            version_str = "1 (current)" if self.elf_header.e_version == 1 else str(self.elf_header.e_version)
            osabi_str = "UNIX - System V" if self.elf_header.e_ident[7] == 0 else "Other"
            type_str = "EXEC (Executable file)" if self.elf_header.e_type == 2 else str(self.elf_header.e_type)
            class_str = "ELF64" if self.elf_header.e_ident_class == ELFCLASS64 else "ELF32"

            lines.append(f"| Magic:                              | {' '.join(f'{b:02x}' for b in self.elf_header.e_ident[:16])}  |")
            lines.append(f"| Class:                              | {class_str:<42}  |")
            lines.append(f"| Data:                               | {data_str:<42}  |")
            lines.append(f"| Version:                            | {version_str:<42}  |")
            lines.append(f"| OS/ABI:                             | {osabi_str:<42}  |")
            lines.append(f"| ABI Version:                        | {self.elf_header.e_ident[8]:<42}  |")
            lines.append(f"| Type:                               | {type_str:<42}  |")
            lines.append(f"| Machine:                            | {self._get_machine_string(self.elf_header.e_machine):<42}  |")
            lines.append(f"| Version:                            | 0x{self.elf_header.e_version:<41x}  |")
            lines.append(f"| Entry point address:                | 0x{self.elf_header.e_entry:016x}  |")
            lines.append(f"| Start of program headers:           | {self.elf_header.e_phoff} (bytes into file)  |")
            lines.append(f"| Start of section headers:           | {self.elf_header.e_shoff} (bytes into file)  |")
            lines.append(f"| Flags:                              | 0x{self.elf_header.e_flags:08x}  |")
            lines.append(f"| Size of this header:                | {self.elf_header.e_ehsize} (bytes)  |")
            lines.append(f"| Size of program headers:            | {self.elf_header.e_phentsize} (bytes)  |")
            lines.append(f"| Number of program headers:          | {self.elf_header.e_phnum}  |")
            lines.append(f"| Size of section headers:            | {self.elf_header.e_shentsize} (bytes)  |")
            lines.append(f"| Number of section headers:          | {self.elf_header.e_shnum}  |")
            lines.append(f"| Section header string table index:  | {self.elf_header.e_shstrndx}  |")

        lines.append("")
        if self.elf_header and self.elf_header.e_shnum == 0:
            lines.append("There are no sections in this file.")

        lines.append("")
        lines.append("Program Headers:")
        lines.append(self._repr_program_headers())

        if self.header:
            lines.append("")
            lines.append("Hash Table Segment Header:")
            lines.append(self._repr_hash_table_header())

            if self.common_metadata and len(self.common_metadata) >= 24:
                lines.append("")
                lines.append("Common Metadata:")
                lines.append(self._repr_common_metadata())

            if self.oem_metadata and len(self.oem_metadata) >= 48:
                lines.append("")
                lines.append("OEM Metadata:")
                lines.append(self._repr_oem_metadata())

            if self.hash_table and len(self.hash_table) > 0:
                lines.append("")
                lines.append("Hash Table Entries:")
                lines.append(self._repr_hash_table())

        return "\n".join(lines)

    def _get_machine_string(self, machine):
        machine_strings = {
            0: "None", 1: "AT&T WE 32100", 2: "SPARC", 3: "Intel 80386",
            40: "ARM", 62: "AMD x86-64", 183: "AArch64",
        }
        return machine_strings.get(machine, f"Unknown ({machine})")

    def _repr_program_headers(self):
        lines = []
        lines.append("| Index  | Type  | Offset             | VirtAddr           | PhysAddr           | FileSize           | MemSize            | Flags  | Align              | OS Segment Type                                          | Encrypted  |")
        lines.append("|--------|-------|--------------------|--------------------|--------------------|--------------------|--------------------|--------|--------------------|----------------------------------------------------------|------------|")

        for idx, phdr in enumerate(self.phdrs):
            p_type = phdr.p_type
            type_str = "NULL" if p_type == 0 else "LOAD" if p_type == 1 else f"0x{p_type:x}"
            flags_str = self._get_flags_string(phdr.p_flags)
            os_type = (phdr.p_flags & 0x07000000) >> 24
            os_segment_type = "PHDR (Encapsulates ELF Header and Program Header Table)" if os_type == 7 else "HASH (Hash Table Segment)" if os_type == 2 else f"0x{os_type:x} (Meaning is OS specific)"

            lines.append(
                f"| {idx:<6} | {type_str:<5} | 0x{phdr.p_offset:<18x} | 0x{phdr.p_vaddr:<18x} | 0x{phdr.p_paddr:<18x} | 0x{phdr.p_filesz:<18x} | 0x{phdr.p_memsz:<18x} | {flags_str:<6} | 0x{phdr.p_align:<18x} | {os_segment_type:<56} | False      |"
            )

        return "\n".join(lines)

    def _get_flags_string(self, p_flags):
        flags = []
        if p_flags & 0x1:
            flags.append("E")
        if p_flags & 0x2:
            flags.append("W")
        if p_flags & 0x4:
            flags.append("R")
        return "".join(flags) if flags else "     "

    def _repr_hash_table_header(self):
        if not self.header:
            return ""
        lines = []
        lines.append(f"| Version:                     | {self.header.version:<11}  |")
        lines.append(f"| Common Metadata Size:        | {self.header.common_metadata_size} (bytes)  |")
        lines.append(f"| QTI Metadata Size:           | {self.header.qti_metadata_size} (bytes)   |")
        lines.append(f"| OEM Metadata Size:           | {self.header.oem_metadata_size} (bytes) |")
        lines.append(f"| Hash Table Size:             | {self.header.hash_table_size} (bytes) |")
        lines.append(f"| QTI Signature Size:          | {self.header.qti_sig_size} (bytes)   |")
        lines.append(f"| QTI Certificate Chain Size:  | {self.header.qti_cert_chain_size} (bytes)   |")
        lines.append(f"| OEM Signature Size:          | {self.header.oem_sig_size} (bytes) |")
        lines.append(f"| OEM Certificate Chain Size:  | {self.header.oem_cert_chain_size} (bytes)  |")
        return "\n".join(lines)

    def _repr_common_metadata(self):
        if not self.common_metadata or len(self.common_metadata) < 24:
            return ""
        lines = []
        major_version = struct.unpack('<I', self.common_metadata[0:4])[0]
        minor_version = struct.unpack('<I', self.common_metadata[4:8])[0]
        software_id = struct.unpack('<I', self.common_metadata[8:12])[0]
        sec_sw_id = struct.unpack('<I', self.common_metadata[12:16])[0]
        hash_algo = struct.unpack('<I', self.common_metadata[16:20])[0]
        meas_target = struct.unpack('<I', self.common_metadata[20:24])[0]

        algo_names = {1: 'SHA256', 2: 'SHA384', 3: 'SHA512', 4: 'SHA256-ONE-SHOT', 5: 'SHA384-ONE-SHOT', 6: 'SHA512-ONE-SHOT'}

        lines.append(f"| Major Version:                | {major_version:<31}  |")
        lines.append(f"| Minor Version:                | {minor_version:<31}  |")
        lines.append(f"| Software ID:                  | 0x{software_id:<29x}  |")
        lines.append(f"| Secondary Software ID:        | 0x{sec_sw_id:<29x}  |")
        lines.append(f"| Hash Table Algorithm          | {algo_names.get(hash_algo, f'Unknown ({hash_algo})'):<31}  |")
        lines.append(f"| Measurement Register Target:  | {'Measurement not to be recorded' if meas_target == 0 else f'Measurement {meas_target}':<31}  |")
        return "\n".join(lines)

    def _repr_oem_metadata(self):
        if not self.oem_metadata or len(self.oem_metadata) < 48:
            return ""
        lines = []
        oem_major = struct.unpack('<I', self.oem_metadata[0:4])[0]
        oem_minor = struct.unpack('<I', self.oem_metadata[4:8])[0]
        arb = struct.unpack('<I', self.oem_metadata[8:12])[0]
        root_cert_idx = struct.unpack('<I', self.oem_metadata[12:16])[0]
        soc_hw_ver = struct.unpack('<H', self.oem_metadata[16:18])[0]
        prod_seg_id = struct.unpack('<H', self.oem_metadata[18:20])[0]
        jtag_id = struct.unpack('<Q', self.oem_metadata[20:28])[0]
        oem_id = struct.unpack('<H', self.oem_metadata[28:30])[0]
        oem_prod_id = struct.unpack('<H', self.oem_metadata[30:32])[0]
        oem_lifecycle = self.oem_metadata[32]
        feature_flags = struct.unpack('<I', self.oem_metadata[36:40])[0]
        jtag_debug = self.oem_metadata[40]

        lines.append(f"| Major Version:                        | {oem_major:<5}  |")
        lines.append(f"| Minor Version:                        | {oem_minor:<5}  |")
        lines.append(f"| Anti-Rollback Version:                | 0x{arb:x:<5}  |")
        lines.append(f"| Root Certificate Index:               | {root_cert_idx:<5}  |")
        lines.append(f"| SoC Hardware Version:                 | 0x{soc_hw_ver:<4x}  |")
        lines.append(f"| Product Segment ID:                   | 0x{prod_seg_id:<4x}  |")
        lines.append(f"| JTAG ID:                              | 0x{jtag_id:<4x}  |")
        lines.append(f"| OEM ID:                               | 0x{oem_id:<4x}  |")
        lines.append(f"| OEM Product ID:                       | 0x{oem_prod_id:<4x}  |")
        lines.append(f"| OEM Lifecycle State:                  | {oem_lifecycle:<5}  |")
        lines.append(f"| Bound to SoC Hardware Versions:       | {'True' if feature_flags & 0x1 else 'False':<5}  |")
        lines.append(f"| Bound to OEM ID:                      | {'True' if feature_flags & 0x10 else 'False':<5}  |")
        lines.append(f"| Bound to OEM Product ID:              | {'True' if feature_flags & 0x20 else 'False':<5}  |")
        lines.append(f"| JTAG Debug:                           | {'Nop' if jtag_debug == 0 else 'Enable' if jtag_debug == 1 else 'Disable':<5}  |")
        return "\n".join(lines)

    def _repr_hash_table(self):
        if not self.hash_table or len(self.hash_table) == 0:
            return ""
        lines = []
        lines.append("| Index  | Hash                                                                                                |")
        lines.append("|--------|-----------------------------------------------------------------------------------------------------|")
        hash_size = 48
        for i in range(0, len(self.hash_table), hash_size):
            if i + hash_size <= len(self.hash_table):
                hash_entry = self.hash_table[i:i + hash_size]
                hash_hex = "0x" + hash_entry.hex()
                lines.append(f"| {i // hash_size:<6} | {hash_hex:<99}  |")
        return "\n".join(lines)

    def get_image_properties(self, authority=AUTHORITY_OEM):
        props = {
            'elf_class': self.elf_header.e_ident_class if self.elf_header else None,
            'machine_type': self.elf_header.e_machine if self.elf_header else None,
            'entry_point': self.elf_header.e_entry if self.elf_header else None,
            'num_segments': len(self.phdrs),
            'num_sections': len(self.shdrs),
        }
        if self.header:
            props['hash_table_version'] = self.header.version
            if self.common_metadata and len(self.common_metadata) >= 12:
                props['software_id'] = struct.unpack('<I', self.common_metadata[8:12])[0]
        return ImageProperties(image_type=ImageFormatType.ELF, properties=props)

    def get_image_format(self, authority=AUTHORITY_OEM):
        return [ImageFormat(format_type=ImageFormatType.ELF)]
