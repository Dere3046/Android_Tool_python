

class Timeout(TimeoutError):
    '''Raised when the lock could not be acquired in *timeout* seconds.'''
    
    def __init__(self = None, lock_file = None):
        self.lock_file = lock_file

    
    def __str__(self = None):
        return f'''The file lock \'{self.lock_file}\' could not be acquired.'''


__all__ = [
    'Timeout']
