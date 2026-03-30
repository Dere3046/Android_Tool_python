
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import subprocess
from compat import str, sys_encoding

def _call(*args, **kwargs):
    pass
# WARNING: Decompyle incomplete


class ChoicesCompleter(object):
    
    def __init__(self, choices):
        self.choices = choices

    
    def _convert(self, choice):
        if isinstance(choice, bytes):
            choice = choice.decode(sys_encoding)
        if not isinstance(choice, str):
            choice = str(choice)
        return choice

    
    def __call__(self, **kwargs):
        return (lambda .0 = None: for c in .0:
self._convert(c))(self.choices)


EnvironCompleter = ChoicesCompleter(os.environ)

class FilesCompleter(object):
    '''
    File completer class, optionally takes a list of allowed extensions
    '''
    
    def __init__(self, allowednames, directories = ((), True)):
        if isinstance(allowednames, (str, bytes)):
            allowednames = [
                allowednames]
        self.allowednames = (lambda .0: [ x.lstrip('*').lstrip('.') for x in .0 ])(allowednames)
        self.directories = directories

    
    def __call__(self, prefix, **kwargs):
        completion = []
        if self.allowednames:
            if self.directories:
                files = _call([
                    'bash',
                    '-c',
                    "compgen -A directory -- '{p}'".format(prefix, **('p',))])
                completion += (lambda .0: [ f + '/' for f in .0 ])(files)
            for x in self.allowednames:
                completion += _call([
                    'bash',
                    '-c',
                    "compgen -A file -X '!*.{0}' -- '{p}'".format(x, prefix, **('p',))])
            return completion
        None += _call([
            'bash',
            '-c',
            "compgen -A file -- '{p}'".format(prefix, **('p',))])
        anticomp = _call([
            'bash',
            '-c',
            "compgen -A directory -- '{p}'".format(prefix, **('p',))])
        completion = list(set(completion) - set(anticomp))
        if self.directories:
            completion += (lambda .0: [ f + '/' for f in .0 ])(anticomp)
        return completion



class _FilteredFilesCompleter(object):
    
    def __init__(self, predicate):
        '''
        Create the completer

        A predicate accepts as its only argument a candidate path and either
        accepts it or rejects it.
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def __call__(self, prefix, **kwargs):
        '''
        Provide completions on prefix
        '''
        target_dir = os.path.dirname(prefix)
        
        try:
            if not target_dir:
                pass
            names = os.listdir('.')
        finally:
            pass
        return None
        incomplete_part = os.path.basename(prefix)
        for name in names:
            if not name.startswith(incomplete_part):
                continue
            candidate = os.path.join(target_dir, name)
            if not self.predicate(candidate):
                continue
            yield candidate + '/' if os.path.isdir(candidate) else candidate
        return None




class DirectoriesCompleter(_FilteredFilesCompleter):
    
    def __init__(self):
        _FilteredFilesCompleter.__init__(self, os.path.isdir, **('predicate',))



class SuppressCompleter(object):
    '''
    A completer used to suppress the completion of specific arguments
    '''
    
    def __init__(self):
        pass

    
    def suppress(self):
        '''
        Decide if the completion should be suppressed
        '''
        return True


