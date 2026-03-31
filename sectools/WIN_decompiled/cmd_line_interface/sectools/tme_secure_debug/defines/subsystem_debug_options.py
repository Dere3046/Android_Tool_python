
from collections import namedtuple
from typing import Dict, Iterator, List, NamedTuple
SubsystemDebugOption = NamedTuple('SubsystemDebugOption', [
    ('arg', str),
    ('help', str),
    ('subsystem', str),
    ('name', str),
    ('bit', int)])
DebugOption = namedtuple('DebugOption', 'id, bit, description')

def get_supported_subsystem_debug_options(security_profile_data = None):
    '''
    Uses Security Profile to find out the supported subsystem debug options.
    Note: define this function in core to speed up handler and argument auto completion.
    '''
    subsystem_debug_options = (lambda .0: pass# WARNING: Decompyle incomplete
)(security_profile_data['subsystems']['subsystem'])
    get_selections_for_tag = get_selections_for_tag
    import common.parser.tme.tme_parser.tme
    tme_supported_subsystems = get_selections_for_tag('SubsysIdentifier')
    for k, debug_options in None((lambda kv = None: kv[0] in tme_supported_subsystems), subsystem_debug_options.items()):
        k_tmp = k
        remove_suffix = '_SS_MSID'
        if k.endswith(remove_suffix) and len(k) > len(remove_suffix):
            k = k[:-len(remove_suffix)]
        for debug_option in debug_options:
            yield SubsystemDebugOption(f'''--{k}-{debug_option.id}'''.replace('_', '-').lower(), debug_option.description, k_tmp, debug_option.id, debug_option.bit)

