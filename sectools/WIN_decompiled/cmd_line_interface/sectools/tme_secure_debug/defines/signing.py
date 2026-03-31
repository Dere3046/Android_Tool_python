
from typing import Any
from cmd_line_interface.base_defines import AutoCloseFileType, COMPATIBLE, KWARGS_CHOICES, KWARGS_HELP, KWARGS_NARGS, KWARGS_READ_BINARY, KWARGS_TYPE, LimitedRangeInt, OPTIONAL
from cmd_line_interface.basecmdline import CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.base_defines import LOCAL, PLUGIN, SIGNATURE_FORMAT, SIGNATURE_FORMAT_GROUP, SIGNING_MODE, SIGNING_MODE_GROUP, TEST
from cmd_line_interface.sectools.cmd_line_common.defines import ATTEST_CERTIFICATE_SUBJECT, ATTEST_CERTIFICATE_SUBJECT_HELP, CA_CERTIFICATE, CA_CERTIFICATE_HELP, CA_KEY, CA_KEY_HELP, CERTIFICATE_CHAIN_DEPTH, CERTIFICATE_CHAIN_DEPTH_HELP, LOCAL_SIGNING_GROUP, LOCAL_SIGNING_GROUP_DESCRIPTION, PLUGIN_SIGNER, PLUGIN_SIGNER_ARGS, PLUGIN_SIGNER_ARGS_HELP, PLUGIN_SIGNER_HELP, PLUGIN_SIGNING_GROUP, ROOT_CERTIFICATE, ROOT_CERTIFICATE_COUNT, ROOT_CERTIFICATE_COUNT_HELP, ROOT_CERTIFICATE_HELP, ROOT_KEY, SIGN, SIGNATURE_FORMAT_HELP, SIGNING_MODE_COMMON_HELP_EXTENDED, TEST_SIGNING_GROUP, TEST_SIGNING_GROUP_DESCRIPTION
from cmd_line_interface.sectools.metadata import CONSUMES, DEPENDS_ON, DEPENDS_ON_VALUE, INCOMPATIBLE_WITH_VALUE, VALUE_DEPENDS_ON, VALUE_DEPENDS_ON_ANY_OF
from common.crypto.openssl.defines import CERTIFICATE_CHAIN_DEPTHS
from common.parser.tme.tme_parser.defines import SIGNATURE_PATH
from common.utils import is_public_distro
if is_public_distro():
    NONPUBLIC_TME_SIGNING_MODES: list[str] = []
    NONPUBLIC_OEM_ELF_ONLY_SIGNING_GLOBAL_CLUSTER_ARGS: dict[(Any, Any)] = { }
    NONPUBLIC_TME_SECURE_DEBUG_SIGNING: CMDLineArgs = { }
    NONPUBLIC_COMMON_SIGNING_DEPENDENCIES_VALUE_DEPENDS_ON: list[tuple[(str, list[str])]] = []
    NONPUBLIC_COMMON_SIGNING_DEPENDENCIES_VALUE_DEPENDS_ON_ANY_OF: list[tuple[(str, list[str])]] = []
else:
    from cmd_line_interface.sectools.tme_secure_debug.nonpublic.nonpublic_defines import NONPUBLIC_TME_SIGNING_MODES, NONPUBLIC_OEM_ELF_ONLY_SIGNING_GLOBAL_CLUSTER_ARGS, NONPUBLIC_TME_SECURE_DEBUG_SIGNING
    from cmd_line_interface.sectools.nonpublic.nonpublic_defines import NONPUBLIC_COMMON_SIGNING_DEPENDENCIES_VALUE_DEPENDS_ON, NONPUBLIC_COMMON_SIGNING_DEPENDENCIES_VALUE_DEPENDS_ON_ANY_OF
TME_LOCAL_SIGNING_GROUP_DESCRIPTION = f'''When signing an OEM Debug Policy ELF, {LOCAL_SIGNING_GROUP_DESCRIPTION}'''
TME_ROOT_KEY_HELP = f'''File path of root key. Required when signing an OEM Debug Policy ELF and {CA_CERTIFICATE} is not provided. Always required when signing an OEM or QTI DPR.'''
OEM_ELF_USE_CASE_NOTE = ' Only applicable for an OEM Debug Policy ELF.'
OEM_ELF_ONLY_SIGNING_GLOBAL_CLUSTER_ARGS = {
    SIGNATURE_FORMAT: None,
    ATTEST_CERTIFICATE_SUBJECT: None,
    CERTIFICATE_CHAIN_DEPTH: None,
    ROOT_CERTIFICATE_COUNT: None,
    CA_KEY: None,
    CA_CERTIFICATE: None,
    ROOT_CERTIFICATE: None }
TME_SIGNING_MODES = [
    LOCAL,
    TEST,
    PLUGIN] + NONPUBLIC_TME_SIGNING_MODES
TME_SECURE_DEBUG_SIGNING: CMDLineArgs = {
    PLUGIN_SIGNING_GROUP: [
        ([
            PLUGIN_SIGNER], {
            KWARGS_HELP: PLUGIN_SIGNER_HELP,
            KWARGS_TYPE: AutoCloseFileType(True, 'utf-8', **('return_path', 'encoding')) }),
        ([
            PLUGIN_SIGNER_ARGS], {
            KWARGS_HELP: PLUGIN_SIGNER_ARGS_HELP }),
        ([
            ATTEST_CERTIFICATE_SUBJECT], {
            KWARGS_HELP: ATTEST_CERTIFICATE_SUBJECT_HELP + OEM_ELF_USE_CASE_NOTE,
            KWARGS_TYPE: str }, {
            DEPENDS_ON: [
                SIGN] })],
    (TEST_SIGNING_GROUP, TEST_SIGNING_GROUP_DESCRIPTION, COMPATIBLE, OPTIONAL): [
        ([
            ROOT_CERTIFICATE_COUNT], {
            KWARGS_HELP: ROOT_CERTIFICATE_COUNT_HELP + OEM_ELF_USE_CASE_NOTE,
            KWARGS_TYPE: LimitedRangeInt(1, **('lower_limit',)) }),
        ([
            CERTIFICATE_CHAIN_DEPTH], {
            KWARGS_HELP: CERTIFICATE_CHAIN_DEPTH_HELP + OEM_ELF_USE_CASE_NOTE,
            KWARGS_CHOICES: range(min(CERTIFICATE_CHAIN_DEPTHS), max(CERTIFICATE_CHAIN_DEPTHS) + 1),
            KWARGS_TYPE: int }, {
            DEPENDS_ON_VALUE: [
                (SIGNING_MODE, [
                    TEST])] }),
        ([
            ATTEST_CERTIFICATE_SUBJECT], {
            KWARGS_HELP: ATTEST_CERTIFICATE_SUBJECT_HELP + OEM_ELF_USE_CASE_NOTE,
            KWARGS_TYPE: str }, {
            DEPENDS_ON: [
                SIGN] })],
    (LOCAL_SIGNING_GROUP, TME_LOCAL_SIGNING_GROUP_DESCRIPTION, COMPATIBLE, OPTIONAL): [
        ([
            ROOT_KEY], {
            KWARGS_HELP: TME_ROOT_KEY_HELP,
            KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) }, {
            DEPENDS_ON: [
                SIGN,
                SIGNING_MODE],
            CONSUMES: [
                SIGNATURE_PATH] }),
        ([
            ROOT_CERTIFICATE], {
            KWARGS_HELP: ROOT_CERTIFICATE_HELP + OEM_ELF_USE_CASE_NOTE,
            KWARGS_NARGS: '+',
            KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) }),
        ([
            CA_CERTIFICATE], {
            KWARGS_HELP: CA_CERTIFICATE_HELP + OEM_ELF_USE_CASE_NOTE,
            KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) }),
        ([
            CA_KEY], {
            KWARGS_HELP: CA_KEY_HELP + OEM_ELF_USE_CASE_NOTE,
            KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) }),
        ([
            ATTEST_CERTIFICATE_SUBJECT], {
            KWARGS_HELP: ATTEST_CERTIFICATE_SUBJECT_HELP + OEM_ELF_USE_CASE_NOTE,
            KWARGS_TYPE: str }, {
            DEPENDS_ON: [
                SIGN] })],
    [
        ([
            SIGNATURE_FORMAT], {
            KWARGS_HELP: SIGNATURE_FORMAT_HELP + OEM_ELF_USE_CASE_NOTE }, {
            INCOMPATIBLE_WITH_VALUE: [
                (SIGNING_MODE, [
                    LOCAL,
                    PLUGIN])],
            DEPENDS_ON: [
                SIGN] })]: [
        (SIGNING_MODE_GROUP, [
            SIGNING_MODE], {
            VALUE_DEPENDS_ON_ANY_OF: NONPUBLIC_COMMON_SIGNING_DEPENDENCIES_VALUE_DEPENDS_ON_ANY_OF,
            [
                SIGN]: VALUE_DEPENDS_ON,
            {
                KWARGS_HELP: SIGNING_MODE_COMMON_HELP_EXTENDED,
                KWARGS_CHOICES: TME_SIGNING_MODES }: DEPENDS_ON })],
    None: SIGNATURE_FORMAT_GROUP }
OEM_ELF_ONLY_SIGNING_GLOBAL_CLUSTER_ARGS.update(NONPUBLIC_OEM_ELF_ONLY_SIGNING_GLOBAL_CLUSTER_ARGS)
TME_SECURE_DEBUG_SIGNING.update(NONPUBLIC_TME_SECURE_DEBUG_SIGNING)
