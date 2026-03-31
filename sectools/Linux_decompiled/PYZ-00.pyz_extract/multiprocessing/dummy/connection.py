
__all__ = [
    'Client',
    'Listener',
    'Pipe']
from queue import Queue
families = [
    None]

class Listener(object):
    
    def __init__(self, address, family, backlog = (None, None, 1)):
        self._backlog_queue = Queue(backlog)

    
    def accept(self):
        pass
    # WARNING: Decompyle incomplete

    
    def close(self):
        self._backlog_queue = None

    
    def address(self):
        return self._backlog_queue

    address = property(address)
    
    def __enter__(self):
        return self

    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()



def Client(address):
    _in = Queue()
    _out = Queue()
    address.put((_out, _in))
    return Connection(_in, _out)


def Pipe(duplex = (True,)):
    a = Queue()
    b = Queue()
    return (Connection(a, b), Connection(b, a))


class Connection(object):
    
    def __init__(self, _in, _out):
        self._out = _out
        self._in = _in
        self.send = self.send_bytes = _out.put
        self.recv = self.recv_bytes = _in.get

    
    def poll(self, timeout = (0,)):
        if self._in.qsize() > 0:
            return True
        if None <= 0:
            return False
        with None._in.not_empty:
            self._in.not_empty.wait(timeout)
            None(None, None, None)
    # WARNING: Decompyle incomplete

    
    def close(self):
        pass

    
    def __enter__(self):
        return self

    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()


