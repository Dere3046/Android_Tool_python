
import socket
import warnings

class TransportSocket:
    '''A socket-like wrapper for exposing real transport sockets.

    These objects can be safely returned by APIs like
    `transport.get_extra_info(\'socket\')`.  All potentially disruptive
    operations (like "socket.close()") are banned.
    '''
    __slots__ = ('_sock',)
    
    def __init__(self = None, sock = None):
        self._sock = sock

    
    def _na(self, what):
        warnings.warn(f'''Using {what} on sockets returned from get_extra_info(\'socket\') will be prohibited in asyncio 3.9. Please report your use case to bugs.python.org.''', DeprecationWarning, self, **('source',))

    
    def family(self):
        return self._sock.family

    family = property(family)
    
    def type(self):
        return self._sock.type

    type = property(type)
    
    def proto(self):
        return self._sock.proto

    proto = property(proto)
    
    def __repr__(self):
        s = f'''<asyncio.TransportSocket fd={self.fileno()}, family={self.family!s}, type={self.type!s}, proto={self.proto}'''
    # WARNING: Decompyle incomplete

    
    def __getstate__(self):
        raise TypeError('Cannot serialize asyncio.TransportSocket object')

    
    def fileno(self):
        return self._sock.fileno()

    
    def dup(self):
        return self._sock.dup()

    
    def get_inheritable(self):
        return self._sock.get_inheritable()

    
    def shutdown(self, how):
        self._sock.shutdown(how)

    
    def getsockopt(self, *args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def setsockopt(self, *args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def getpeername(self):
        return self._sock.getpeername()

    
    def getsockname(self):
        return self._sock.getsockname()

    
    def getsockbyname(self):
        return self._sock.getsockbyname()

    
    def accept(self):
        self._na('accept() method')
        return self._sock.accept()

    
    def connect(self, *args, **kwargs):
        self._na('connect() method')
    # WARNING: Decompyle incomplete

    
    def connect_ex(self, *args, **kwargs):
        self._na('connect_ex() method')
    # WARNING: Decompyle incomplete

    
    def bind(self, *args, **kwargs):
        self._na('bind() method')
    # WARNING: Decompyle incomplete

    
    def ioctl(self, *args, **kwargs):
        self._na('ioctl() method')
    # WARNING: Decompyle incomplete

    
    def listen(self, *args, **kwargs):
        self._na('listen() method')
    # WARNING: Decompyle incomplete

    
    def makefile(self):
        self._na('makefile() method')
        return self._sock.makefile()

    
    def sendfile(self, *args, **kwargs):
        self._na('sendfile() method')
    # WARNING: Decompyle incomplete

    
    def close(self):
        self._na('close() method')
        return self._sock.close()

    
    def detach(self):
        self._na('detach() method')
        return self._sock.detach()

    
    def sendmsg_afalg(self, *args, **kwargs):
        self._na('sendmsg_afalg() method')
    # WARNING: Decompyle incomplete

    
    def sendmsg(self, *args, **kwargs):
        self._na('sendmsg() method')
    # WARNING: Decompyle incomplete

    
    def sendto(self, *args, **kwargs):
        self._na('sendto() method')
    # WARNING: Decompyle incomplete

    
    def send(self, *args, **kwargs):
        self._na('send() method')
    # WARNING: Decompyle incomplete

    
    def sendall(self, *args, **kwargs):
        self._na('sendall() method')
    # WARNING: Decompyle incomplete

    
    def set_inheritable(self, *args, **kwargs):
        self._na('set_inheritable() method')
    # WARNING: Decompyle incomplete

    
    def share(self, process_id):
        self._na('share() method')
        return self._sock.share(process_id)

    
    def recv_into(self, *args, **kwargs):
        self._na('recv_into() method')
    # WARNING: Decompyle incomplete

    
    def recvfrom_into(self, *args, **kwargs):
        self._na('recvfrom_into() method')
    # WARNING: Decompyle incomplete

    
    def recvmsg_into(self, *args, **kwargs):
        self._na('recvmsg_into() method')
    # WARNING: Decompyle incomplete

    
    def recvmsg(self, *args, **kwargs):
        self._na('recvmsg() method')
    # WARNING: Decompyle incomplete

    
    def recvfrom(self, *args, **kwargs):
        self._na('recvfrom() method')
    # WARNING: Decompyle incomplete

    
    def recv(self, *args, **kwargs):
        self._na('recv() method')
    # WARNING: Decompyle incomplete

    
    def settimeout(self, value):
        if value == 0:
            return None
        raise None('settimeout(): only 0 timeout is allowed on transport sockets')

    
    def gettimeout(self):
        return 0

    
    def setblocking(self, flag):
        if not flag:
            return None
        raise None('setblocking(): transport sockets cannot be blocking')

    
    def __enter__(self):
        self._na('context manager protocol')
        return self._sock.__enter__()

    
    def __exit__(self, *err):
        self._na('context manager protocol')
    # WARNING: Decompyle incomplete


