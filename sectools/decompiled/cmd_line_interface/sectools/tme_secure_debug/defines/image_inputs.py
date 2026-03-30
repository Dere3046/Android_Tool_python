
'''
This file contains the changes and new arguments for the "Image Inputs" and "Image Outputs" groups as they differ from
the cmd_line_interface.sectools.cmd_line_common.defines.
'''
from cmd_line_interface.base_defines import AutoCloseFileType, KWARGS_HELP, KWARGS_NARGS, KWARGS_READ_BINARY, KWARGS_TYPE, KWARGS_WRITE_BINARY
from cmd_line_interface.basecmdline import CMDLineGroup
from cmd_line_interface.sectools.cmd_line_common.defines import DUMP, GENERATE, HASH, INFILE, INFILE_HELP, INSPECT, OUTFILE, OUTFILE_HELP, QTI, QTI_DPR, SIGN, VERIFY_ROOT
from cmd_line_interface.sectools.metadata import CONSUMES, DEPENDS_ON, DEPENDS_ON_ANY_OF, INCOMPATIBLE_WITH, NA
DEC = '--dec'
SLC = '--slc'
QTI_DPR_HELP = f'''File path of a QTI Debug Policy Request (DPR) to be packaged within OEM Debug Policy ELF. Can only be used during OEM Debug Policy generation. Cannot be used with {QTI}.'''
SLC_HELP = f'''File path of one or more Service Layer Commands (SLC) to be packaged within OEM Debug Policy ELF. Can only be used during OEM Debug Policy generation. Cannot be used with {QTI}.'''
DEC_HELP = 'File path of Debug Entitlement Certificate (DEC) to use for TME Debug Policy generation. If creating multiple TME Debug Policies, a separate DEC must be provided for each TME Debug Policy being created.'
TME_IMAGE_INPUTS_GROUP: CMDLineGroup = [
    ([
        INFILE], {
        KWARGS_HELP: INFILE_HELP,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY, True, **('return_path',)),
        KWARGS_NARGS: '?' }, {
        DEPENDS_ON_ANY_OF: [
            INSPECT,
            SIGN,
            HASH,
            DUMP,
            VERIFY_ROOT],
        INCOMPATIBLE_WITH: [
            GENERATE] }),
    ([
        DEC], {
        KWARGS_HELP: DEC_HELP,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) }, {
        CONSUMES: [
            NA] }),
    ([
        QTI_DPR], {
        KWARGS_HELP: QTI_DPR_HELP,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) }, {
        CONSUMES: [
            NA],
        INCOMPATIBLE_WITH: [
            QTI],
        DEPENDS_ON: [
            GENERATE] }),
    ([
        SLC], {
        KWARGS_HELP: SLC_HELP,
        KWARGS_NARGS: '+',
        KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) }, {
        CONSUMES: [
            NA],
        INCOMPATIBLE_WITH: [
            QTI],
        DEPENDS_ON: [
            GENERATE] })]
TME_IMAGE_OUTPUTS_GROUP: CMDLineGroup = [
    ([
        OUTFILE], {
        KWARGS_HELP: OUTFILE_HELP,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_WRITE_BINARY) })]
