
from abc import ABC, abstractmethod

class AbstractPositionalData(ABC):
    
    def __init__(self):
        self.ignore = False

    
    def offset(self):
        pass

    offset = property(abstractmethod(offset))
    
    def offset(self, value):
        pass

    offset = offset.setter(abstractmethod(offset))
    
    def size(self):
        pass

    size = property(abstractmethod(size))
    
    def size(self, value):
        pass

    size = size.setter(abstractmethod(size))
    
    def end(self):
        if self.size:
            return self.offset + self.size - 1
        return None.offset

    end = property(end)
    
    def alignment(self):
        pass

    alignment = property(abstractmethod(alignment))
    
    def address(self):
        return 0

    address = property(address)
    
    def mem_size(self):
        return 0

    mem_size = property(mem_size)
    
    def end_address(self):
        if self.mem_size:
            return self.address + self.mem_size - 1
        return None.address

    end_address = property(end_address)
    
    def data_name(self):
        pass

    data_name = property(abstractmethod(data_name))
    
    def ignore(self):
        return self._ignore

    ignore = property(ignore)
    
    def ignore(self, value):
        self._ignore = value

    ignore = ignore.setter(ignore)
    
    def is_loadable(self):
        return False

    is_loadable = property(is_loadable)
    
    def overlaps_with(self = None, positional_entry = None):
        if positional_entry.size != 0 and self.size != 0:
            if self.end <= self.end:
                pass
            elif not self.end <= positional_entry.end:
                if positional_entry.end <= positional_entry.end:
                    return positional_entry.end <= self.end
                positional_entry.end <= positional_entry.end
        return positional_entry.end

    
    def overlaps_in_memory_with(self = None, positional_entry = None):
        if self.is_loadable and positional_entry.is_loadable and positional_entry.mem_size != 0 and self.mem_size != 0:
            if self.end_address <= self.end_address:
                pass
            elif not self.end_address <= positional_entry.end_address:
                if positional_entry.end_address <= positional_entry.end_address:
                    return positional_entry.end_address <= self.end_address
                positional_entry.end_address <= positional_entry.end_address
        return positional_entry.end_address

    
    def __repr__(self):
        return f'''{self.data_name} with offset {hex(self.offset)} and size {hex(self.size)}'''



class PositionalData(AbstractPositionalData):
    
    def __init__(self = None, offset = None, size = None, alignment = None, data_name = None):
        self.offset = offset
        self.size = size
        self.alignment = alignment
        self._data_name = data_name
        super().__init__()

    
    def offset(self):
        return self._offset

    offset = property(offset)
    
    def offset(self, value):
        self._offset = value

    offset = offset.setter(offset)
    
    def size(self):
        return self._size

    size = property(size)
    
    def size(self, value):
        self._size = value

    size = size.setter(size)
    
    def alignment(self):
        return self._alignment

    alignment = property(alignment)
    
    def alignment(self, value):
        self._alignment = value

    alignment = alignment.setter(alignment)
    
    def data_name(self):
        return self._data_name

    data_name = property(data_name)
    __classcell__ = None

