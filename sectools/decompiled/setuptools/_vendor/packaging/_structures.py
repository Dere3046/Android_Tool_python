

class InfinityType:
    
    def __repr__(self = None):
        return 'Infinity'

    
    def __hash__(self = None):
        return hash(repr(self))

    
    def __lt__(self = None, other = None):
        return False

    
    def __le__(self = None, other = None):
        return False

    
    def __eq__(self = None, other = None):
        return isinstance(other, self.__class__)

    
    def __gt__(self = None, other = None):
        return True

    
    def __ge__(self = None, other = None):
        return True

    
    def __neg__(self = None):
        return NegativeInfinity


Infinity = InfinityType()

class NegativeInfinityType:
    
    def __repr__(self = None):
        return '-Infinity'

    
    def __hash__(self = None):
        return hash(repr(self))

    
    def __lt__(self = None, other = None):
        return True

    
    def __le__(self = None, other = None):
        return True

    
    def __eq__(self = None, other = None):
        return isinstance(other, self.__class__)

    
    def __gt__(self = None, other = None):
        return False

    
    def __ge__(self = None, other = None):
        return False

    
    def __neg__(self = None):
        return Infinity


NegativeInfinity = NegativeInfinityType()
