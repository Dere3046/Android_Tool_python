
from argparse import ArgumentParser, Namespace
from functools import partial
from itertools import groupby
from operator import contains
from cmd_line_interface.base_defines import HELP, HELP_ABBREV, HELP_HELP, KWARGS_ACTION, KWARGS_HELP, KWARGS_STORE_TRUE, KWARGS_VERSION, get_cmd_member
from cmd_line_interface.basecmdline import BaseCMDLine, CMDLineArgs, HelpFormatterHideSuppressedOptions
from cmd_line_interface.sectools import metabuild_secure_image
from cmd_line_interface.sectools.argument_clustering_interface import ArgumentClusteringInterface
from cmd_line_interface.sectools.cmd_line_common.defines import FEATURE, GENERATE_OP, OPEN_SOURCE_LICENSES, OPEN_SOURCE_LICENSES_HELP, OPERATION, OPTIONAL_ARGUMENTS, REQUIRED_ARGUMENTS, SECURITY_PROFILE, SUBFEATURE, VERSION, VERSION_HELP
from cmd_line_interface.sectools.defines import SECTOOLS_DESCRIPTION, SECTOOLS_VERSION
from cmd_line_interface.sectools.dynamic_arguments_interface import DynamicArgumentsInterface
from cmd_line_interface.sectools.elf_consolidator.defines import ELF_CONSOLIDATOR, ELF_CONSOLIDATOR_DESCRIPTION, ELF_CONSOLIDATOR_NAME
from cmd_line_interface.sectools.elf_tool.combine.defines import COMBINE, COMBINE_DESCRIPTION, ELF_TOOL_COMBINE
from cmd_line_interface.sectools.elf_tool.defines import ELF_TOOL, ELF_TOOL_DESCRIPTION, ELF_TOOL_EPILOG, ELF_TOOL_NAME
from cmd_line_interface.sectools.elf_tool.generate.defines import ELF_TOOL_GENERATE, GENERATE_DESCRIPTION
from cmd_line_interface.sectools.elf_tool.generate.handler import ELFToolGenerateCMDLineHandler
from cmd_line_interface.sectools.elf_tool.insert.defines import ELF_TOOL_INSERT, INSERT, INSERT_DESCRIPTION
from cmd_line_interface.sectools.elf_tool.remove_sections.defines import ELF_TOOL_REMOVE_SECTIONS, REMOVE_SECTIONS, REMOVE_SECTIONS_DESCRIPTION
from cmd_line_interface.sectools.fuse_validator.cmd_line_common.defines import COMPARE_NAME, GENERATE_PAYLOAD_NAME, SHOW_ON_TARGET_RESULTS_NAME
from cmd_line_interface.sectools.fuse_validator.compare.defines import COMPARE, COMPARE_DESCRIPTION
from cmd_line_interface.sectools.fuse_validator.defines import FUSE_VALIDATOR, FUSE_VALIDATOR_DESCRIPTION, FUSE_VALIDATOR_EPILOG, FUSE_VALIDATOR_NAME
from cmd_line_interface.sectools.fuse_validator.generate_payload.defines import GENERATE_PAYLOAD, GENERATE_PAYLOAD_DESCRIPTION
from cmd_line_interface.sectools.fuse_validator.show_on_target_results.defines import SHOW_ON_TARGET_RESULTS, SHOW_ON_TARGET_RESULTS_DESCRIPTION
from cmd_line_interface.sectools.fuseblower.defines import FUSE_BLOWER, FUSE_BLOWER_DESCRIPTION, FUSE_BLOWER_DEVICE_RESTRICTIONS, FUSE_BLOWER_EPILOG, FUSE_BLOWER_NAME, FUSE_BLOWER_SIGNING
from cmd_line_interface.sectools.fuseblower.handler import FuseBlowerCMDLineHandler
from cmd_line_interface.sectools.mbn_tool.defines import MBN_GENERATE_DESCRIPTION, MBN_TOOL, MBN_TOOL_DESCRIPTION, MBN_TOOL_EPILOG, MBN_TOOL_GENERATE, MBN_TOOL_NAME
from cmd_line_interface.sectools.metabuild_secure_image.defines import METABUILD_SECURE_IMAGE_DESCRIPTION, METABUILD_SECURE_IMAGE_EPILOG, METABUILD_SECURE_IMAGE_NAME, SECURE_IMAGE_OPTIONS
from cmd_line_interface.sectools.metabuild_secure_image.handler import MetabuildSecureImageCMDLineHandler
from cmd_line_interface.sectools.secure_debug.defines import DEBUG_OPTION_EXTENDED_HELP, SECURE_DEBUG, SECURE_DEBUG_DESCRIPTION, SECURE_DEBUG_DEVICE_RESTRICTIONS, SECURE_DEBUG_NAME, SECURE_DEBUG_SIGNING
from cmd_line_interface.sectools.secure_debug.handler import SecureDebugCMDLineHandler
from cmd_line_interface.sectools.secure_image.cmdline_dict import SECURE_IMAGE, SECURE_IMAGE_DEVICE_RESTRICTIONS, SECURE_IMAGE_ENCRYPTION, SECURE_IMAGE_SIGNING
from cmd_line_interface.sectools.secure_image.defines import SECURE_IMAGE_DESCRIPTION, SECURE_IMAGE_NAME
from cmd_line_interface.sectools.secure_image.handler import SecureImageCMDLineHandler
from cmd_line_interface.sectools.tme_command.defines import TME_COMMAND, TME_COMMAND_DESCRIPTION, TME_COMMAND_EPILOG, TME_COMMAND_NAME
from cmd_line_interface.sectools.tme_command.soc_terminate.defines import SOC_TERMINATE, SOC_TERMINATE_ARGS, SOC_TERMINATE_DESCRIPTION, SOC_TERMINATE_EPILOG, SOC_TERMINATE_GENERATE, SOC_TERMINATE_GENERATE_DESCRIPTION
from cmd_line_interface.sectools.tme_command.soc_terminate.handler import SocTerminateCMDLineHandler
from cmd_line_interface.sectools.tme_secure_debug.defines import TME_SECURE_DEBUG_NAME, defines
from cmd_line_interface.sectools.tme_secure_debug.defines.defines import TME_SECURE_DEBUG_DESCRIPTION
from cmd_line_interface.sectools.tme_secure_debug.defines.device_restrictions import TME_DEVICE_RESTRICTIONS
from cmd_line_interface.sectools.tme_secure_debug.defines.help import TME_EPILOG
from cmd_line_interface.sectools.tme_secure_debug.defines.signing import TME_SECURE_DEBUG_SIGNING
from cmd_line_interface.sectools.tme_secure_debug.handler import TMESecureDebugCMDLineHandler
from common.data.data import comma_separated_string, tuple_to_version_string

class SectoolsCMDLine(BaseCMDLine):
    EPILOG = f'''For help menu of a specific feature: {BaseCMDLine.TOOL_NAME} <{FEATURE}> {HELP_ABBREV}'''
    ENTRY_ARGUMENTS: CMDLineArgs = {
        OPTIONAL_ARGUMENTS: [
            ([
                HELP_ABBREV,
                HELP], {
                KWARGS_HELP: HELP_HELP,
                KWARGS_ACTION: KWARGS_STORE_TRUE }),
            ([
                VERSION], {
                KWARGS_VERSION: tuple_to_version_string(SECTOOLS_VERSION),
                KWARGS_HELP: VERSION_HELP,
                KWARGS_ACTION: KWARGS_VERSION }),
            ([
                OPEN_SOURCE_LICENSES], {
                KWARGS_HELP: OPEN_SOURCE_LICENSES_HELP,
                KWARGS_ACTION: KWARGS_STORE_TRUE })] }
    
    def __init__(self = None):
        self.parsers = {
            None: self }
        super().__init__(self.ENTRY_ARGUMENTS, SECTOOLS_DESCRIPTION, self.EPILOG, **('arguments', 'description', 'epilog'))
        feature_subparsers = self.add_subparsers(ArgumentParser, comma_separated_string([
            SECURE_IMAGE_NAME,
            METABUILD_SECURE_IMAGE_NAME,
            SECURE_DEBUG_NAME,
            TME_SECURE_DEBUG_NAME,
            FUSE_BLOWER_NAME,
            FUSE_VALIDATOR_NAME,
            ELF_TOOL_NAME,
            ELF_CONSOLIDATOR_NAME,
            MBN_TOOL_NAME,
            TME_COMMAND_NAME]), FEATURE, FEATURE, REQUIRED_ARGUMENTS, **('parser_class', 'help', 'dest', 'metavar', 'title'))
        self.parsers[SECURE_IMAGE_NAME] = self.add_subparser(feature_subparsers, SECURE_IMAGE_NAME, SECURE_IMAGE_DESCRIPTION, SECURE_IMAGE, [
            SECURE_IMAGE_SIGNING,
            SECURE_IMAGE_ENCRYPTION,
            SECURE_IMAGE_DEVICE_RESTRICTIONS], SecureImageCMDLineHandler(), **('handler',))
        self.parsers[METABUILD_SECURE_IMAGE_NAME] = self.add_subparser(feature_subparsers, METABUILD_SECURE_IMAGE_NAME, METABUILD_SECURE_IMAGE_DESCRIPTION, metabuild_secure_image.defines.METABUILD_SECURE_IMAGE, [
            SECURE_IMAGE_OPTIONS], MetabuildSecureImageCMDLineHandler(), HelpFormatterHideSuppressedOptions, METABUILD_SECURE_IMAGE_EPILOG, **('handler', 'formatter_class', 'epilog'))
        self.parsers[SECURE_DEBUG_NAME] = self.add_subparser(feature_subparsers, SECURE_DEBUG_NAME, SECURE_DEBUG_DESCRIPTION, SECURE_DEBUG, [
            SECURE_DEBUG_SIGNING,
            SECURE_DEBUG_DEVICE_RESTRICTIONS], SecureDebugCMDLineHandler(), DEBUG_OPTION_EXTENDED_HELP, **('handler', 'epilog'))
        self.parsers[TME_SECURE_DEBUG_NAME] = self.add_subparser(feature_subparsers, TME_SECURE_DEBUG_NAME, TME_SECURE_DEBUG_DESCRIPTION, defines.TME_SECURE_DEBUG, [
            TME_SECURE_DEBUG_SIGNING,
            TME_DEVICE_RESTRICTIONS], TMESecureDebugCMDLineHandler(), TME_EPILOG, **('suppress_groups', 'handler', 'epilog'))
        self.parsers[FUSE_BLOWER_NAME] = self.add_subparser(feature_subparsers, FUSE_BLOWER_NAME, FUSE_BLOWER_DESCRIPTION, FUSE_BLOWER, [
            FUSE_BLOWER_SIGNING,
            FUSE_BLOWER_DEVICE_RESTRICTIONS], FuseBlowerCMDLineHandler(), FUSE_BLOWER_EPILOG, **('handler', 'epilog'))
        fuse_validator_parser = self.add_subparser(feature_subparsers, FUSE_VALIDATOR_NAME, FUSE_VALIDATOR_DESCRIPTION, FUSE_VALIDATOR, FUSE_VALIDATOR_EPILOG, **('epilog',))
        fuse_validator_parser.parsers = { }
        self.parsers[FUSE_VALIDATOR_NAME] = fuse_validator_parser
        fuse_validator_subparser = fuse_validator_parser.add_subparsers(comma_separated_string([
            GENERATE_PAYLOAD_NAME,
            COMPARE_NAME,
            SHOW_ON_TARGET_RESULTS_NAME]), SUBFEATURE, OPERATION, REQUIRED_ARGUMENTS, **('help', 'dest', 'metavar', 'title'))
        fuse_validator_parser.parsers[GENERATE_PAYLOAD_NAME] = self.add_subparser(fuse_validator_subparser, GENERATE_PAYLOAD_NAME, GENERATE_PAYLOAD_DESCRIPTION, GENERATE_PAYLOAD)
        fuse_validator_parser.parsers[COMPARE_NAME] = self.add_subparser(fuse_validator_subparser, COMPARE_NAME, COMPARE_DESCRIPTION, COMPARE)
        fuse_validator_parser.parsers[SHOW_ON_TARGET_RESULTS_NAME] = self.add_subparser(fuse_validator_subparser, SHOW_ON_TARGET_RESULTS_NAME, SHOW_ON_TARGET_RESULTS_DESCRIPTION, SHOW_ON_TARGET_RESULTS)
        elf_tool_parser = self.add_subparser(feature_subparsers, ELF_TOOL_NAME, ELF_TOOL_DESCRIPTION, ELF_TOOL, ELF_TOOL_EPILOG, **('epilog',))
        elf_tool_parser.parsers = { }
        self.parsers[ELF_TOOL_NAME] = elf_tool_parser
        elf_parser_subparser = elf_tool_parser.add_subparsers(comma_separated_string([
            GENERATE_OP,
            INSERT,
            REMOVE_SECTIONS,
            COMBINE]), SUBFEATURE, OPERATION, REQUIRED_ARGUMENTS, **('help', 'dest', 'metavar', 'title'))
        elf_tool_parser.parsers[GENERATE_OP] = self.add_subparser(elf_parser_subparser, GENERATE_OP, GENERATE_DESCRIPTION, ELF_TOOL_GENERATE, ELFToolGenerateCMDLineHandler(), **('handler',))
        elf_tool_parser.parsers[INSERT] = self.add_subparser(elf_parser_subparser, INSERT, INSERT_DESCRIPTION, ELF_TOOL_INSERT)
        elf_tool_parser.parsers[REMOVE_SECTIONS] = self.add_subparser(elf_parser_subparser, REMOVE_SECTIONS, REMOVE_SECTIONS_DESCRIPTION, ELF_TOOL_REMOVE_SECTIONS)
        elf_tool_parser.parsers[COMBINE] = self.add_subparser(elf_parser_subparser, COMBINE, COMBINE_DESCRIPTION, ELF_TOOL_COMBINE)
        self.parsers[ELF_CONSOLIDATOR_NAME] = self.add_subparser(feature_subparsers, ELF_CONSOLIDATOR_NAME, ELF_CONSOLIDATOR_DESCRIPTION, ELF_CONSOLIDATOR)
        mbn_tool_parser = self.add_subparser(feature_subparsers, MBN_TOOL_NAME, MBN_TOOL_DESCRIPTION, MBN_TOOL, MBN_TOOL_EPILOG, **('epilog',))
        mbn_tool_parser.parsers = { }
        self.parsers[MBN_TOOL_NAME] = mbn_tool_parser
        mbn_parser_subparser = mbn_tool_parser.add_subparsers(GENERATE_OP, SUBFEATURE, OPERATION, REQUIRED_ARGUMENTS, **('help', 'dest', 'metavar', 'title'))
        mbn_tool_parser.parsers[GENERATE_OP] = self.add_subparser(mbn_parser_subparser, GENERATE_OP, MBN_GENERATE_DESCRIPTION, MBN_TOOL_GENERATE)
        tme_command_parser = self.add_subparser(feature_subparsers, TME_COMMAND_NAME, TME_COMMAND_DESCRIPTION, TME_COMMAND, TME_COMMAND_EPILOG, **('epilog',))
        tme_command_parser.parsers = { }
        self.parsers[TME_COMMAND_NAME] = tme_command_parser
        tme_command_parser_subparser = tme_command_parser.add_subparsers(SOC_TERMINATE, SUBFEATURE, SUBFEATURE, REQUIRED_ARGUMENTS, **('help', 'dest', 'metavar', 'title'))
        soc_terminate_parser = self.add_subparser(tme_command_parser_subparser, SOC_TERMINATE, SOC_TERMINATE_DESCRIPTION, SOC_TERMINATE_ARGS, SOC_TERMINATE_EPILOG, SocTerminateCMDLineHandler(), **('epilog', 'handler'))
        tme_command_parser.parsers[SOC_TERMINATE] = soc_terminate_parser
        soc_terminate_parser_subparser = soc_terminate_parser.add_subparsers(GENERATE_OP, OPERATION, OPERATION, REQUIRED_ARGUMENTS, **('help', 'dest', 'metavar', 'title'))
        soc_terminate_parser.parsers = { }
        soc_terminate_parser.parsers[GENERATE_OP] = self.add_subparser(soc_terminate_parser_subparser, GENERATE_OP, SOC_TERMINATE_GENERATE_DESCRIPTION, SOC_TERMINATE_GENERATE)

    
    def parse_args(self = None, args = None, namespace = None):
        '''Allow dynamic arguments. Pre-process command line before supplying it to a parent for arg parsing.'''
        clusters = [
            args]
        if args and args[0] in self.parsers and isinstance(self.parsers[args[0]].handler, ArgumentClusteringInterface):
            if not None(None(None, (lambda x = None: x == self.parsers[args[0]].handler.ARG_CLUSTER_SEPARATOR))):
                pass
            clusters = [
                []]
        parsed_clusters = []
        for i, cluster in enumerate(clusters):
            if i:
                cluster = [
                    self.parsers[args[0]].handler.TOOL_NAME] + cluster
            preserved_actions = { }
            for parser_name, parser in self.parsers.items():
                for action in parser._actions:
                    if SECURITY_PROFILE in action.option_strings:
                        preserved_actions[parser_name] = parser._actions
                        parser._actions = [
                            action]
            (tmp_parsed, _) = self.parse_known_args(cluster)
            for parser_name, actions in preserved_actions.items():
                self.parsers[parser_name]._actions = actions
            security_profile = get_cmd_member(SECURITY_PROFILE)
            if all(map(partial(contains, vars(tmp_parsed)), [
                security_profile,
                FEATURE])) and vars(tmp_parsed)[security_profile] and isinstance(self.parsers[tmp_parsed.feature].handler, DynamicArgumentsInterface):
                self.parsers[tmp_parsed.feature].handler.add_dynamic_arguments(vars(tmp_parsed))
            self.__init__()
            parsed_cluster = super().parse_args(cluster, namespace)
            parsed_clusters.append(parsed_cluster)
        parsed_args = parsed_clusters[0]
        parsed_args.cluster_args = parsed_clusters
        return parsed_args

    __classcell__ = None

