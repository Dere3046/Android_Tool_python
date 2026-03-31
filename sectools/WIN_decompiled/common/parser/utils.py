
from lzma import LZMADecompressor, LZMAError, compress as lzma_compress
from typing import Type, cast
from cmd_line_interface.sectools.cmd_line_common.defines import INFILE
from common.compression.xz_utils import compress as xz_compress
from common.data.base_parser import BaseParser
from common.data.binary_struct import StructBase
from common.data.defines import PAD_BYTE_1
from common.logging.logger import log_debug, log_warning
from common.parser.debug_policy_elf.debug_policy_elf import DebugPolicyELF
from common.parser.debug_policy_elf_with_hash_segment.debug_policy_elf_with_hash_segment import DebugPolicyELFWithHashTableSegment
from common.parser.defines import COMPRESSION_FORMATS, COMPRESSION_FORMAT_DESCRIPTION_TO_INT, LZMA, LZMA_HEADER_SIZE, LZMA_UNCOMPRESSED_DATA_SIZE_OFFSET, LZMA_UNCOMPRESSED_DATA_SIZE_SIZE, XZ
from common.parser.elf.elf import ELF
from common.parser.elf_preamble.elf_preamble import ELFWithPreamble
from common.parser.elf_preamble_with_hash_segment.elf_preamble_with_hash_segment import ELFPreambleWithHashTableSegment
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.fuse_validator_payload.payload_request.payload_request import FuseValidatorPayloadRequest
from common.parser.fuse_validator_payload.payload_response.payload_reponse import FuseValidatorPayloadResponse
from common.parser.license_manager.license_manager import LicenseManager
from common.parser.mbn.mbn import MBN
from common.parser.mdt.mdt import MDT
from common.parser.mdt_with_hash_segment.mdt_with_hash_segment import MDTWithHashTableSegment
from common.parser.multi_image.multi_image import MultiImage
from common.parser.sec_dat.sec_dat import SecDat
from common.parser.sec_elf.sec_elf import SecELF
from common.parser.sec_elf_with_hash_segment.sec_elf_with_hash_segment import SecELFWithHashTableSegment
from common.parser.tme.base_tme import BaseTME
from common.parser.tme.dpr.dpr import DPR
from common.parser.tme_elf.tme_elf import TMEELF
from common.parser.tme_elf_with_hash_segment.tme_elf_with_hash_segment import TMEELFWithHashTableSegment

class UnrecognizedImageFormat(RuntimeError):
    '''Custom exception class for image parsing errors.'''
    pass


def get_parser_classes():
    return [
        MDTWithHashTableSegment,
        MDT,
        LicenseManager,
        MultiImage,
        SecDat,
        SecELFWithHashTableSegment,
        SecELF,
        DebugPolicyELFWithHashTableSegment,
        DebugPolicyELF,
        TMEELFWithHashTableSegment,
        TMEELF,
        ELFWithHashTableSegment,
        ELF,
        ELFPreambleWithHashTableSegment,
        ELFWithPreamble,
        DPR,
        BaseTME,
        FuseValidatorPayloadRequest,
        FuseValidatorPayloadResponse,
        MBN]


def _parse_data(data = None):
    for parser_class in get_parser_classes():
        log_debug(f'''Checking if image is {parser_class.__name__} image.''')
        if cast(StructBase, parser_class).is_type(data):
            log_debug(f'''Image was detected as {parser_class.__name__} image.''')
            parsed_data = parser_class(data)
            return parsed_data
        raise UnrecognizedImageFormat('Image is of unrecognized format.')


def get_parsed_image(data = None, profile_compression_format = None, data_source = None):
    if not isinstance(data, memoryview):
        data = memoryview(bytearray(data))
# WARNING: Decompyle incomplete


def get_compressed_data(data = None, compression_format = None):
    data_in_bytes = bytes(data)
    if compression_format == XZ:
        compressed_data = xz_compress(data_in_bytes)
        return compressed_data
    compressed_data = None(data_in_bytes, COMPRESSION_FORMAT_DESCRIPTION_TO_INT[LZMA], **('format',))
    if len(compressed_data) <= LZMA_HEADER_SIZE:
        raise RuntimeError('Compressed data is shorter than expected.')
    compressed_data = None[:LZMA_UNCOMPRESSED_DATA_SIZE_OFFSET] + len(data_in_bytes).to_bytes(LZMA_UNCOMPRESSED_DATA_SIZE_SIZE, 'little') + compressed_data[LZMA_HEADER_SIZE:]
    return compressed_data


def get_decompressed_data(data = None, compression_format = None):
    data_in_bytes = bytes(data)
    if compression_format == LZMA:
        if len(data_in_bytes) <= LZMA_HEADER_SIZE:
            raise RuntimeError('Compressed data is shorter than expected.')
        data_in_bytes = None[:LZMA_UNCOMPRESSED_DATA_SIZE_OFFSET] + PAD_BYTE_1 * LZMA_UNCOMPRESSED_DATA_SIZE_SIZE + data_in_bytes[LZMA_HEADER_SIZE:]
    obj = LZMADecompressor(COMPRESSION_FORMAT_DESCRIPTION_TO_INT[compression_format], **('format',))
    return obj.decompress(data_in_bytes)

