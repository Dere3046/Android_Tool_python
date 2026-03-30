
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.argument_clustering_interface import RuntimeErrorInCluster
from cmd_line_interface.sectools.cmd_line_common.defines import QTI_DPR, SECURITY_PROFILE
from cmd_line_interface.sectools.tme_secure_debug.defines import defines
from cmd_line_interface.sectools.tme_secure_debug.defines.image_inputs import DEC, SLC
from cmd_line_interface.sectools.tme_secure_debug.defines.image_operations import NEW_DPR
from cmd_line_interface.sectools.tme_secure_debug.dynamic_arguments import security_profile_process
from common.parser.tme.tme_parser.tme import TME
from common.parser.tme_elf.tme_elf import TMEELF
from core.tme_secure_debug.augmented_inspect import DESCRIBE_DPR, DESCRIBE_SLC, describe
from core.tme_secure_debug.generate_dp import generate_dp
from core.tme_secure_debug.generate_dpr import generate_dpr

def generate_elf(parsed_args = None):
    tme_objects = []
    defines.global_security_profile_data = security_profile_process(parsed_args.get(SECURITY_PROFILE)[0])
# WARNING: Decompyle incomplete

