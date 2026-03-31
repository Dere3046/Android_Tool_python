
from typing import List
from common.parser.elf.bit32.program_header import ProgramHeader32

def get_loadable_phdrs(phdrs = None, reverse = None):
    '''Given a list of program headers, return a sublist with only the ones to be packaged.'''
    if reverse:
        return (lambda .0: [ phdr for phdr in .0 if phdr.size > 0 ])(reversed(phdrs))
    
    def <listcomp>(.0):
        return [ phdr for phdr in .0 if phdr.size > 0 ]

    return None(<listcomp>)

