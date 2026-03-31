
import sys
import warnings
from typing import TYPE_CHECKING, List, Dict
from distutils.command.build import build as _build
from setuptools import SetuptoolsDeprecationWarning
if sys.version_info >= (3, 8):
    from typing import Protocol
elif TYPE_CHECKING:
    from typing_extensions import Protocol
else:
    from abc import ABC as Protocol
_ORIGINAL_SUBCOMMANDS = {
    'build_py',
    'build_clib',
    'build_ext',
    'build_scripts'}

class build(_build):
    sub_commands = _build.sub_commands[:]
    
    def get_sub_commands(self = None):
        subcommands = (lambda .0: pass# WARNING: Decompyle incomplete
)(_build.sub_commands)
        if subcommands - _ORIGINAL_SUBCOMMANDS:
            msg = '\n            It seems that you are using `distutils.command.build` to add\n            new subcommands. Using `distutils` directly is considered deprecated,\n            please use `setuptools.command.build`.\n            '
            warnings.warn(msg, SetuptoolsDeprecationWarning)
            self.sub_commands = _build.sub_commands
        return super().get_sub_commands()

    __classcell__ = None


class SubCommand(Protocol):
    '''In order to support editable installations (see :pep:`660`) all
    build subcommands **SHOULD** implement this protocol. They also **MUST** inherit
    from ``setuptools.Command``.

    When creating an :pep:`editable wheel <660>`, ``setuptools`` will try to evaluate
    custom ``build`` subcommands using the following procedure:

    1. ``setuptools`` will set the ``editable_mode`` attribute to ``True``
    2. ``setuptools`` will execute the ``run()`` command.

       .. important::
          Subcommands **SHOULD** take advantage of ``editable_mode=True`` to adequate
          its behaviour or perform optimisations.

          For example, if a subcommand don\'t need to generate any extra file and
          everything it does is to copy a source file into the build directory,
          ``run()`` **SHOULD** simply "early return".

          Similarly, if the subcommand creates files that would be placed alongside
          Python files in the final distribution, during an editable install
          the command **SHOULD** generate these files "in place" (i.e. write them to
          the original source directory, instead of using the build directory).
          Note that ``get_output_mapping()`` should reflect that and include mappings
          for "in place" builds accordingly.

    3. ``setuptools`` use any knowledge it can derive from the return values of
       ``get_outputs()`` and ``get_output_mapping()`` to create an editable wheel.
       When relevant ``setuptools`` **MAY** attempt to use file links based on the value
       of ``get_output_mapping()``. Alternatively, ``setuptools`` **MAY** attempt to use
       :doc:`import hooks <python:reference/import>` to redirect any attempt to import
       to the directory with the original source code and other files built in place.

    Please note that custom sub-commands **SHOULD NOT** rely on ``run()`` being
    executed (or not) to provide correct return values for ``get_outputs()``,
    ``get_output_mapping()`` or ``get_source_files()``. The ``get_*`` methods should
    work independently of ``run()``.
    '''
    build_lib: str = False
    
    def initialize_options(self):
        '''(Required by the original :class:`setuptools.Command` interface)'''
        pass

    
    def finalize_options(self):
        '''(Required by the original :class:`setuptools.Command` interface)'''
        pass

    
    def run(self):
        '''(Required by the original :class:`setuptools.Command` interface)'''
        pass

    
    def get_source_files(self = None):
        '''
        Return a list of all files that are used by the command to create the expected
        outputs.
        For example, if your build command transpiles Java files into Python, you should
        list here all the Java files.
        The primary purpose of this function is to help populating the ``sdist``
        with all the files necessary to build the distribution.
        All files should be strings relative to the project root directory.
        '''
        pass

    
    def get_outputs(self = None):
        '''
        Return a list of files intended for distribution as they would have been
        produced by the build.
        These files should be strings in the form of
        ``"{build_lib}/destination/file/path"``.

        .. note::
           The return value of ``get_output()`` should include all files used as keys
           in ``get_output_mapping()`` plus files that are generated during the build
           and don\'t correspond to any source file already present in the project.
        '''
        pass

    
    def get_output_mapping(self = None):
        '''
        Return a mapping between destination files as they would be produced by the
        build (dict keys) into the respective existing (source) files (dict values).
        Existing (source) files should be represented as strings relative to the project
        root directory.
        Destination files should be strings in the form of
        ``"{build_lib}/destination/file/path"``.
        '''
        pass


