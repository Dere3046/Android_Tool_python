
from abc import ABC, abstractmethod
from itertools import starmap
from typing import Any
from cmd_line_interface.base_defines import get_cmd_arg, get_cmd_member
from cmd_line_interface.basecmdline import CMDLineArgs, NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_handler_interface import CMDLineHandlerInterface
from cmd_line_interface.sectools.metadata import validate_cmd_line_args_with_metadata
from common.data.data import comma_separated_string, plural_s

class RuntimeErrorInCluster(RuntimeError):
    
    def __init__(self = None, arg_cluster_separator = None, cluster_no = None, *args):
        self.arg_cluster_separator = arg_cluster_separator
        self.cluster_no = cluster_no
    # WARNING: Decompyle incomplete

    
    def __str__(self = None):
        return super().__str__().rstrip(' .') + f''' in {self.arg_cluster_separator} argument cluster #{self.cluster_no}.'''

    __classcell__ = None


class ArgumentClusteringInterface(ABC, CMDLineHandlerInterface):
    
    def TOOL_NAME(self = None):
        '''The name of the tool (and handler).'''
        pass

    TOOL_NAME = None(None(TOOL_NAME))
    
    def ARG_CLUSTER_SEPARATOR(self = None):
        '''The cluster separator cmd argument.'''
        pass

    ARG_CLUSTER_SEPARATOR = None(None(ARG_CLUSTER_SEPARATOR))
    
    def GLOBAL_CLUSTER_ARGS(self = None):
        '''The arguments that are shared between all clusters.'''
        pass

    GLOBAL_CLUSTER_ARGS = None(None(GLOBAL_CLUSTER_ARGS))
    
    def validate_each_cmd_line_cluster(self = None, cluster_args = None):
        '''Can be used to run additional validations for each argument cluster.'''
        pass

    
    def post_cmd_line_validation(self = None, args = None):
        '''Can be used to run additional argument patching and post validation checks.'''
        pass

    
    def validate_cmd_line_argument_clusters(self = None, args = None, arguments = None):
        global_cluster_args_as_members = dict(starmap((lambda k, v: (get_cmd_member(k), v)), self.GLOBAL_CLUSTER_ARGS.items()))
        global_args = { }
        for i, cluster in enumerate(args.cluster_args, 1, **('start',)):
            found_globals = (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(vars(cluster).items())
            duplicates = set(global_args).intersection(set(found_globals))
            if duplicates:
                raise RuntimeErrorInCluster(self.ARG_CLUSTER_SEPARATOR, i, f'''Remove duplicated argument{plural_s(duplicates)} {comma_separated_string(map(get_cmd_arg, duplicates), 'and')}.''')
            None.update(found_globals)
        for cluster in args.cluster_args:
            vars(cluster).update(global_args)
        self.validate_cmd_line_args(args)
    # WARNING: Decompyle incomplete


