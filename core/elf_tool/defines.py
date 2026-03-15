"""ELF tool defines."""

from typing import Dict, List, Any, Optional

from cmd_line_interface.base_defines import (
    HELP, HELP_ABBREV, HELP_GROUP, HELP_HELP,
    KWARGS_ACTION, KWARGS_HELP, KWARGS_CHOICES,
    KWARGS_DEFAULT, KWARGS_REQUIRED, KWARGS_TYPE,
    KWARGS_WRITE_BINARY, KWARGS_READ_BINARY, KWARGS_STORE_TRUE,
    KWARGS_COUNT, KWARGS_NARGS, AutoCloseFileType, COMPATIBLE, OPTIONAL
)
from cmd_line_interface.basecmdline import CMDLineArgs, CMDLineGroup, update_cmdline_arg
from cmd_line_interface.sectools.cmd_line_common.defines import (
    OPERATION, INFILE, INFILE_COMMON_HELP, OUTFILE, OUTFILE_COMMON_HELP,
    VERBOSE, VERBOSE_ABBREV, VERBOSE_HELP, eight_byte_hex, four_byte_hex
)
from cmd_line_interface.sectools.cmd_line_common.auto_close_image_type import AutoCloseImageType
from common.parser.elf.defines import (
    PT_DESCRIPTION, PT_LOAD, PT_NOTE, PT_NULL,
    ELFCLASS32, ELFCLASS64,
    EM_ARM, EM_INT_TO_DESCRIPTION, EM_INT_TO_STRING,
    EM_STRING_TO_INT
)
from common.parser.elf.elf import ELF

ELF_TOOL_NAME = 'elf-tool'
ELF_TOOL_DESCRIPTION = 'Tool for generating, adding segments to, removing sections from, and combining ELF software images.'
ELF_TOOL_EPILOG = f'For help menu of a specific {OPERATION}: sectools {ELF_TOOL_NAME} <{OPERATION}> {HELP_ABBREV}'

GENERATE_OP = 'generate'
INSERT = 'insert'
COMBINE = 'combine'
REMOVE_SECTIONS = 'remove-sections'

DATA = '--data'
DATA_HELP = 'File path of segment data.'
INFILE_HELP = f'{INFILE_COMMON_HELP} ELF image'
OUTFILE_HELP = f'{OUTFILE_COMMON_HELP} ELF image.'
DEFAULT_0 = '0x0'
DEFAULTS_TO_0 = f'Defaults to {DEFAULT_0}.'

ELF_CONFIGURATION_GROUP = 'ELF Configuration'
ELF_ENTRY = '--elf-entry'
ELF_ENTRY_COMMON_HELP = 'Entry point address.'
SEGMENT_CONFIGURATION_GROUP = 'Segment Configuration'
SEGMENT_CONFIGURATION_DESCRIPTION = f'Program Header values of segment containing {DATA}.'

TYPE = '--type'
TYPE_HELP = 'Defaults to LOAD.'
OFFSET = '--offset'
OFFSET_HELP = 'Defaults to the lowest available offset following the ELF Header and Program Header Table.'
VADDR = '--vaddr'
PADDR = '--paddr'
MEMSZ = '--memsz'
MEMSZ_HELP = f'Defaults to size of {DATA}.'
FLAGS = '--flags'
ALIGN = '--align'

ELF_CLASS = '--elf-class'
ELF_MACHINE_TYPE = '--elf-machine-type'
AVAILABLE_ELF_MACHINE_TYPES = '--available-elf-machine-types'
ELF_CLASS_HELP = 'Defaults to 64.'
ELF_ENTRY_HELP = f'{ELF_ENTRY_COMMON_HELP} {DEFAULTS_TO_0}'
AVAILABLE_ELF_MACHINE_TYPES_HELP = f'Show available {ELF_MACHINE_TYPE} values and exit.'
DEFAULT_ELF_MACHINE_TYPE = EM_INT_TO_STRING.get(EM_ARM, 'ARM')
ELF_MACHINE_TYPE_HELP = f'Architecture of output ELF image. Defaults to {DEFAULT_ELF_MACHINE_TYPE}.'


def get_common_help() -> CMDLineGroup:
    """Get common help."""
    return [
        ([HELP_ABBREV, HELP], {
            KWARGS_HELP: HELP_HELP,
            KWARGS_ACTION: KWARGS_ACTION
        }),
        ([VERBOSE_ABBREV, VERBOSE], {
            KWARGS_HELP: VERBOSE_HELP,
            KWARGS_DEFAULT: 0,
            KWARGS_ACTION: KWARGS_COUNT
        })
    ]


def get_common_segment_configuration() -> CMDLineGroup:
    """Get common segment configuration."""
    return [
        ([TYPE], {
            KWARGS_DEFAULT: PT_DESCRIPTION.get(PT_LOAD, 'LOAD'),
            KWARGS_HELP: TYPE_HELP,
            KWARGS_CHOICES: [
                PT_DESCRIPTION.get(PT_NULL, 'NULL'),
                PT_DESCRIPTION.get(PT_LOAD, 'LOAD'),
                PT_DESCRIPTION.get(PT_NOTE, 'NOTE')
            ]
        }),
        ([OFFSET], {
            KWARGS_DEFAULT: DEFAULT_0,
            KWARGS_HELP: OFFSET_HELP,
            KWARGS_TYPE: eight_byte_hex
        }),
        ([VADDR], {
            KWARGS_DEFAULT: DEFAULT_0,
            KWARGS_HELP: DEFAULTS_TO_0,
            KWARGS_TYPE: eight_byte_hex
        }),
        ([PADDR], {
            KWARGS_DEFAULT: DEFAULT_0,
            KWARGS_HELP: DEFAULTS_TO_0,
            KWARGS_TYPE: eight_byte_hex
        }),
        ([MEMSZ], {
            KWARGS_HELP: MEMSZ_HELP,
            KWARGS_TYPE: eight_byte_hex
        }),
        ([FLAGS], {
            KWARGS_DEFAULT: DEFAULT_0,
            KWARGS_HELP: DEFAULTS_TO_0,
            KWARGS_TYPE: four_byte_hex
        }),
        ([ALIGN], {
            KWARGS_DEFAULT: DEFAULT_0,
            KWARGS_HELP: DEFAULTS_TO_0,
            KWARGS_TYPE: eight_byte_hex
        })
    ]


def get_common_image_inputs() -> CMDLineGroup:
    """Get common image inputs."""
    return [
        ([INFILE], {
            KWARGS_HELP: f'{INFILE_HELP}.',
            KWARGS_TYPE: AutoCloseImageType((ELF,), return_path=True)
        })
    ]


def get_common_image_outputs() -> CMDLineGroup:
    """Get common image outputs."""
    return [
        ([OUTFILE], {
            KWARGS_HELP: OUTFILE_HELP,
            KWARGS_REQUIRED: True,
            KWARGS_TYPE: AutoCloseFileType(KWARGS_WRITE_BINARY)
        })
    ]


ELF_TOOL: CMDLineArgs = {
    HELP_GROUP: [
        ([HELP_ABBREV, HELP], {
            KWARGS_HELP: HELP_HELP,
            KWARGS_ACTION: KWARGS_ACTION
        })
    ]
}

GENERATE_DESCRIPTION = 'Generate a new ELF software image containing a segment as specified via Segment Configuration arguments.'

GENERATE_HELP = list(get_common_help())
GENERATE_HELP.append(([AVAILABLE_ELF_MACHINE_TYPES], {
    KWARGS_HELP: AVAILABLE_ELF_MACHINE_TYPES_HELP,
    KWARGS_ACTION: KWARGS_STORE_TRUE
}))

GENERATE_IMAGE_INPUTS: CMDLineGroup = [
    ([DATA], {
        KWARGS_HELP: DATA_HELP,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY)
    })
]

GENERATE_IMAGE_OUTPUTS: CMDLineGroup = [
    ([OUTFILE], {
        KWARGS_HELP: OUTFILE_HELP,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_WRITE_BINARY)
    })
]

GENERATE_ELF_CONFIGURATION: CMDLineGroup = [
    ([ELF_CLASS], {
        KWARGS_HELP: ELF_CLASS_HELP,
        KWARGS_DEFAULT: ELFCLASS64,
        KWARGS_CHOICES: [ELFCLASS32, ELFCLASS64],
        KWARGS_TYPE: int
    }),
    ([ELF_ENTRY], {
        KWARGS_DEFAULT: DEFAULT_0,
        KWARGS_HELP: ELF_ENTRY_HELP,
        KWARGS_TYPE: eight_byte_hex
    }),
    ([ELF_MACHINE_TYPE], {
        KWARGS_DEFAULT: DEFAULT_ELF_MACHINE_TYPE,
        KWARGS_HELP: ELF_MACHINE_TYPE_HELP,
        KWARGS_TYPE: str
    })
]

ELF_TOOL_GENERATE: CMDLineArgs = {
    (SEGMENT_CONFIGURATION_GROUP, SEGMENT_CONFIGURATION_DESCRIPTION, COMPATIBLE, OPTIONAL): get_common_segment_configuration(),
    ELF_CONFIGURATION_GROUP: GENERATE_ELF_CONFIGURATION,
    'Image Outputs': GENERATE_IMAGE_OUTPUTS,
    'Image Inputs': GENERATE_IMAGE_INPUTS,
    HELP_GROUP: GENERATE_HELP
}

INSERT_DESCRIPTION = 'Add a segment specified via Segment Configuration arguments to an existing ELF software image.'
INSERT_OFFSET_HELP = f'Defaults to the lowest available offset following the ELF Header, Program Header Table, and existing segments.'

INSERT_IMAGE_INPUTS = list(get_common_image_inputs())
INSERT_IMAGE_INPUTS.append(([DATA], {
    KWARGS_HELP: DATA_HELP,
    KWARGS_REQUIRED: True,
    KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY)
}))

INSERT_SEGMENT_CONFIGURATION = get_common_segment_configuration()

ELF_TOOL_INSERT: CMDLineArgs = {
    (SEGMENT_CONFIGURATION_GROUP, SEGMENT_CONFIGURATION_DESCRIPTION, COMPATIBLE, OPTIONAL): INSERT_SEGMENT_CONFIGURATION,
    'Image Outputs': get_common_image_outputs(),
    'Image Inputs': INSERT_IMAGE_INPUTS,
    HELP_GROUP: get_common_help()
}

COMBINE_DESCRIPTION = 'Combine multiple ELFs into a single ELF. Data contained within ELF sections will not be persisted unless they are encapsulated within segments.'
INFILE_HELP_COMBINE = f'{INFILE_COMMON_HELP}s.'
COMBINE_ELF_ENTRY_HELP = f'{ELF_ENTRY_COMMON_HELP} Defaults to entry point address of first {INFILE}.'

COMBINE_IMAGE_INPUTS: CMDLineGroup = [
    ([INFILE], {
        KWARGS_ACTION: 'append',
        KWARGS_NARGS: '+',
        KWARGS_HELP: INFILE_HELP_COMBINE,
        KWARGS_TYPE: AutoCloseImageType((ELF,), return_path=True)
    })
]

COMBINE_ELF_CONFIGURATION: CMDLineGroup = [
    ([ELF_ENTRY], {
        KWARGS_HELP: COMBINE_ELF_ENTRY_HELP,
        KWARGS_TYPE: eight_byte_hex
    })
]

ELF_TOOL_COMBINE: CMDLineArgs = {
    ELF_CONFIGURATION_GROUP: COMBINE_ELF_CONFIGURATION,
    'Image Outputs': get_common_image_outputs(),
    'Image Inputs': COMBINE_IMAGE_INPUTS,
    HELP_GROUP: get_common_help()
}

REMOVE_SECTIONS_DESCRIPTION = 'Remove Sections from an existing ELF software image.'

ELF_TOOL_REMOVE_SECTIONS: CMDLineArgs = {
    'Image Outputs': get_common_image_outputs(),
    'Image Inputs': get_common_image_inputs(),
    HELP_GROUP: get_common_help()
}
