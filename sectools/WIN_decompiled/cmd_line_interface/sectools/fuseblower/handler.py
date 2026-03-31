
from argparse import SUPPRESS
from typing import Any
from cmd_line_interface.base_defines import XMLInfo, get_cmd_member
from cmd_line_interface.basecmdline import BaseCMDLine, NamespaceWithGet
from cmd_line_interface.sectools import fuseblower
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE
from cmd_line_interface.sectools.cmd_line_common.defines import HASH, SIGN
from cmd_line_interface.sectools.cmd_line_common.handler import CommonCMDLineHandler
from cmd_line_interface.sectools.dynamic_arguments_interface import DynamicArgumentsInterface
from cmd_line_interface.sectools.fuseblower.defines import FUSE_BLOWER_DEVICE_RESTRICTIONS, FUSE_BLOWER_DEVICE_RESTRICTIONS_ARGUMENTS, FUSE_BLOWER_SIGNING, FUSE_GROUP, RECOMMENDED_FUSES, SHOW_OEM_CHOICE_FUSES
from cmd_line_interface.sectools.fuseblower.dynamic_arguments import update_fuseblower_security_profile_arguments
from common.data.data import and_separated, numbered_string, plural_s, properties_repr

class FuseBlowerSigningOptionsCMDLine(BaseCMDLine):
    
    def __init__(self = None):
        super().__init__(FUSE_BLOWER_SIGNING, SUPPRESS, **('usage',))

    __classcell__ = None


class FuseBlowerRestrictionsCMDLine(BaseCMDLine):
    
    def __init__(self = None):
        super().__init__(FUSE_BLOWER_DEVICE_RESTRICTIONS, SUPPRESS, **('usage',))

    __classcell__ = None


class FuseBlowerCMDLineHandler(DynamicArgumentsInterface, CommonCMDLineHandler):
    
    def show_signing_options_help():
        FuseBlowerSigningOptionsCMDLine().print_help()

    show_signing_options_help = None(show_signing_options_help)
    
    def show_available_device_restrictions():
        FuseBlowerRestrictionsCMDLine().print_help()

    show_available_device_restrictions = None(show_available_device_restrictions)
    
    def show_available_fuse_groups():
        if not fuseblower.security_profile_data:
            raise RuntimeError(f'''{SECURITY_PROFILE} must be provided in order to show available {FUSE_GROUP}.''')
        if not None.fuse_groups:
            raise RuntimeError(f'''Provided {SECURITY_PROFILE} does not support {FUSE_GROUP}.''')
        table = [
            None]
        sep_rows = []
        for group, fuse_arguments in sorted(fuseblower.fuse_groups.items()):
            sep_rows.append(len(table) - 1)
            fuse_arguments = sorted(fuse_arguments, (lambda arg: not (arg.multi_bit)), **('key',))
            for i, fuse_argument in enumerate(fuse_arguments):
                table.append((group if not i else '', fuse_argument.argument, 'True' if fuse_argument.multi_bit else 'False'))
        print(f'''Available Fuse Groups:\n{properties_repr(table, sep_rows, **('sep_rows',))}''')

    show_available_fuse_groups = None(show_available_fuse_groups)
    
    def show_recommended_fuses():
        if not fuseblower.security_profile_data:
            raise RuntimeError(f'''{SECURITY_PROFILE} must be provided in order to show fuses that will be included in a Fuse Blower Image generated using {RECOMMENDED_FUSES}.''')
        if not None.recommended_fuses_qti_values:
            raise RuntimeError(f'''Provided {SECURITY_PROFILE} does not support {RECOMMENDED_FUSES}.''')
        table = [
            None]
        if fuseblower.recommended_fuses_oem_values:
            table.extend((lambda .0: [ (arg_name, 'OEM Value') for arg_name in .0 ])(fuseblower.recommended_fuses_oem_values))
        for argument, recommended_value in sorted(fuseblower.recommended_fuses_qti_values.items(), (lambda x: len(x[1]) == 1), **('key',)):
            if recommended_value != '0':
                table.append((argument, recommended_value))
        print(f'''Recommended Fuses Values:\n{properties_repr(table, [
            0], **('sep_rows',))}''')

    show_recommended_fuses = None(show_recommended_fuses)
    
    def show_oem_choice_fuses():
        if not fuseblower.security_profile_data:
            raise RuntimeError(f'''{SECURITY_PROFILE} must be provided in order to show fuses that are entirely optional for the OEM to provide.''')
        if not None.oem_choice_fuses:
            raise RuntimeError(f'''Provided {SECURITY_PROFILE} does not support {SHOW_OEM_CHOICE_FUSES}.''')
        None(f'''OEM Choice Fuses:\n{numbered_string(fuseblower.oem_choice_fuses)}''')

    show_oem_choice_fuses = None(show_oem_choice_fuses)
    
    def validate_cmd_line_args(cls = None, args = None):
        super().validate_cmd_line_args(args)
        security_profile_data = fuseblower.security_profile_data
        if args.generate:
            if security_profile_data and security_profile_data.sec_dat_properties:
                if args.sign:
                    raise RuntimeError(f'''Cannot perform {SIGN} when generating a Sec Dat image.''')
                if None.hash:
                    raise RuntimeError(f'''Cannot perform {HASH} when generating a Sec Dat image.''')
                if not None and security_profile_data.sec_elf_properties and args.hash and args.sign:
                    raise RuntimeError(f'''{HASH} or {SIGN} operation must be provided when generating a Sec ELF image.''')
                for device_restriction in None:
                    value = getattr(args, get_cmd_member(device_restriction))
                    if value and security_profile_data and security_profile_data.sec_dat_properties:
                        raise RuntimeError(f'''{device_restriction} cannot be provided when generating a Sec Dat image.''')
                    if fuse_groups = args.get(FUSE_GROUP):
                        for group in fuse_groups:
                            if (lambda .0 = None: [ arg for arg in .0 if args.get(arg) is None ])(required)(missing = (lambda .0 = None: [ arg for arg in .0 if args.get(arg) is None ])(required)):
                                raise RuntimeError(f'''The value "{group}" of {FUSE_GROUP} requires{' the following' if len(missing) > 1 else ''} additional argument{plural_s(missing)}: {and_separated(missing)}.''')
                            return None
                            return None

    validate_cmd_line_args = None(validate_cmd_line_args)
    
    def add_dynamic_arguments(parsed_args = None):
        security_profile = parsed_args[get_cmd_member(SECURITY_PROFILE)]
    # WARNING: Decompyle incomplete

    add_dynamic_arguments = None(add_dynamic_arguments)
    __classcell__ = None

