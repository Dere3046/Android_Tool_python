
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import OPERATION
from cmd_line_interface.sectools.cmd_line_handler_interface import CMDLineHandlerInterface
from cmd_line_interface.sectools.tme_command.soc_terminate.defines import ALLOWED_SOC_TERMINATE_OPERATIONS
from common.data.data import or_separated

class SocTerminateCMDLineHandler(CMDLineHandlerInterface):
    
    def validate_cmd_line_args(cls = None, args = None):
        if args.get(OPERATION) not in ALLOWED_SOC_TERMINATE_OPERATIONS:
            raise RuntimeError(f'''An operation is required. (choose from \'{or_separated(ALLOWED_SOC_TERMINATE_OPERATIONS)}\')''')

    validate_cmd_line_args = None(validate_cmd_line_args)

