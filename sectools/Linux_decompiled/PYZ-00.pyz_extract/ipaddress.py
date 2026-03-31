
'''A fast, lightweight IPv4/IPv6 manipulation library in Python.

This library is used to create/poke/manipulate IPv4 and IPv6 addresses
and networks.

'''
__version__ = '1.0'
import functools
IPV4LENGTH = 32
IPV6LENGTH = 128

class AddressValueError(ValueError):
    '''A Value Error related to the address.'''
    pass


class NetmaskValueError(ValueError):
    '''A Value Error related to the netmask.'''
    pass


def ip_address(address):
    """Take an IP string/int and return an object of the correct type.

    Args:
        address: A string or integer, the IP address.  Either IPv4 or
          IPv6 addresses may be supplied; integers less than 2**32 will
          be considered to be IPv4 by default.

    Returns:
        An IPv4Address or IPv6Address object.

    Raises:
        ValueError: if the *address* passed isn't either a v4 or a v6
          address

    """
    pass
# WARNING: Decompyle incomplete


def ip_network(address, strict = (True,)):
    """Take an IP string/int and return an object of the correct type.

    Args:
        address: A string or integer, the IP network.  Either IPv4 or
          IPv6 networks may be supplied; integers less than 2**32 will
          be considered to be IPv4 by default.

    Returns:
        An IPv4Network or IPv6Network object.

    Raises:
        ValueError: if the string passed isn't either a v4 or a v6
          address. Or if the network has host bits set.

    """
    pass
# WARNING: Decompyle incomplete


def ip_interface(address):
    """Take an IP string/int and return an object of the correct type.

    Args:
        address: A string or integer, the IP address.  Either IPv4 or
          IPv6 addresses may be supplied; integers less than 2**32 will
          be considered to be IPv4 by default.

    Returns:
        An IPv4Interface or IPv6Interface object.

    Raises:
        ValueError: if the string passed isn't either a v4 or a v6
          address.

    Notes:
        The IPv?Interface classes describe an Address on a particular
        Network, so they're basically a combination of both the Address
        and Network classes.

    """
    pass
# WARNING: Decompyle incomplete


def v4_int_to_packed(address):
    '''Represent an address as 4 packed bytes in network (big-endian) order.

    Args:
        address: An integer representation of an IPv4 IP address.

    Returns:
        The integer address packed as 4 bytes in network (big-endian) order.

    Raises:
        ValueError: If the integer is negative or too large to be an
          IPv4 IP address.

    '''
    pass
# WARNING: Decompyle incomplete


def v6_int_to_packed(address):
    '''Represent an address as 16 packed bytes in network (big-endian) order.

    Args:
        address: An integer representation of an IPv6 IP address.

    Returns:
        The integer address packed as 16 bytes in network (big-endian) order.

    '''
    pass
# WARNING: Decompyle incomplete


def _split_optional_netmask(address):
    '''Helper to split the netmask and raise AddressValueError if needed'''
    addr = str(address).split('/')
    if len(addr) > 2:
        raise AddressValueError("Only one '/' permitted in %r" % address)


def _find_address_range(addresses):
    '''Find a sequence of sorted deduplicated IPv#Address.

    Args:
        addresses: a list of IPv#Address objects.

    Yields:
        A tuple containing the first and last IP addresses in the sequence.

    '''
    it = iter(addresses)
    first = last = next(it)
    for ip in it:
        if ip._ip != last._ip + 1:
            yield (first, last)
            first = ip
        last = ip
    yield (first, last)


def _count_righthand_zero_bits(number, bits):
    '''Count the number of zero bits on the right hand side.

    Args:
        number: an integer.
        bits: maximum number of bits to count.

    Returns:
        The number of zero bits on the right hand side of the number.

    '''
    if number == 0:
        return bits
    return None(bits, (~number & number - 1).bit_length())


def summarize_address_range(first, last):
    """Summarize a network range given the first and last IP addresses.

    Example:
        >>> list(summarize_address_range(IPv4Address('192.0.2.0'),
        ...                              IPv4Address('192.0.2.130')))
        ...                                #doctest: +NORMALIZE_WHITESPACE
        [IPv4Network('192.0.2.0/25'), IPv4Network('192.0.2.128/31'),
         IPv4Network('192.0.2.130/32')]

    Args:
        first: the first IPv4Address or IPv6Address in the range.
        last: the last IPv4Address or IPv6Address in the range.

    Returns:
        An iterator of the summarized IPv(4|6) network objects.

    Raise:
        TypeError:
            If the first and last objects are not IP addresses.
            If the first and last objects are not the same version.
        ValueError:
            If the last object is not greater than the first.
            If the version of the first address is not 4 or 6.

    """
    if not isinstance(first, _BaseAddress) or isinstance(last, _BaseAddress):
        raise TypeError('first and last must be IP addresses, not networks')
    if None.version != last.version:
        raise TypeError('%s and %s are not of the same version' % (first, last))
    if None > last:
        raise ValueError('last IP address must be greater than first')
    if None.version == 4:
        ip = IPv4Network
    elif first.version == 6:
        ip = IPv6Network
    else:
        raise ValueError('unknown IP version')
    ip_bits = None._max_prefixlen
    first_int = first._ip
    last_int = last._ip
    if first_int <= last_int:
        nbits = min(_count_righthand_zero_bits(first_int, ip_bits), ((last_int - first_int) + 1).bit_length() - 1)
        net = ip((first_int, ip_bits - nbits))
        yield net
        first_int += 1 << nbits
        if first_int - 1 == ip._ALL_ONES:
            return None
        if not None <= last_int:
            return None
        return None


def _collapse_addresses_internal(addresses):
    """Loops through the addresses, collapsing concurrent netblocks.

    Example:

        ip1 = IPv4Network('192.0.2.0/26')
        ip2 = IPv4Network('192.0.2.64/26')
        ip3 = IPv4Network('192.0.2.128/26')
        ip4 = IPv4Network('192.0.2.192/26')

        _collapse_addresses_internal([ip1, ip2, ip3, ip4]) ->
          [IPv4Network('192.0.2.0/24')]

        This shouldn't be called directly; it is called via
          collapse_addresses([]).

    Args:
        addresses: A list of IPv4Network's or IPv6Network's

    Returns:
        A list of IPv4Network's or IPv6Network's depending on what we were
        passed.

    """
    to_merge = list(addresses)
    subnets = { }
    if to_merge:
        net = to_merge.pop()
        supernet = net.supernet()
        existing = subnets.get(supernet)
        if existing is None:
            subnets[supernet] = net
        elif existing != net:
            del subnets[supernet]
            to_merge.append(supernet)
        if not to_merge:
            last = None
            for net in sorted(subnets.values()):
                if last is not None and last.broadcast_address >= net.broadcast_address:
                    continue
                yield net
                last = net
            return None


def collapse_addresses(addresses):
    """Collapse a list of IP objects.

    Example:
        collapse_addresses([IPv4Network('192.0.2.0/25'),
                            IPv4Network('192.0.2.128/25')]) ->
                           [IPv4Network('192.0.2.0/24')]

    Args:
        addresses: An iterator of IPv4Network or IPv6Network objects.

    Returns:
        An iterator of the collapsed IPv(4|6)Network objects.

    Raises:
        TypeError: If passed a list of mixed version objects.

    """
    addrs = []
    ips = []
    nets = []
    for ip in addresses:
        if isinstance(ip, _BaseAddress):
            if ips and ips[-1]._version != ip._version:
                raise TypeError('%s and %s are not of the same version' % (ip, ips[-1]))
            None.append(ip)
            continue
        if ip._prefixlen == ip._max_prefixlen:
            if ips and ips[-1]._version != ip._version:
                raise TypeError('%s and %s are not of the same version' % (ip, ips[-1]))
            ips.append(ip.ip)
# WARNING: Decompyle incomplete


def get_mixed_type_key(obj):
    """Return a key suitable for sorting between networks and addresses.

    Address and Network objects are not sortable by default; they're
    fundamentally different so the expression

        IPv4Address('192.0.2.0') <= IPv4Network('192.0.2.0/24')

    doesn't make any sense.  There are some times however, where you may wish
    to have ipaddress sort these for you anyway. If you need to do this, you
    can use this function as the key= argument to sorted().

    Args:
      obj: either a Network or Address object.
    Returns:
      appropriate key.

    """
    if isinstance(obj, _BaseNetwork):
        return obj._get_networks_key()
    if None(obj, _BaseAddress):
        return obj._get_address_key()


class _IPAddressBase:
    '''The mother class.'''
    __slots__ = ()
    
    def exploded(self):
        '''Return the longhand version of the IP address as a string.'''
        return self._explode_shorthand_ip_string()

    exploded = property(exploded)
    
    def compressed(self):
        '''Return the shorthand version of the IP address as a string.'''
        return str(self)

    compressed = property(compressed)
    
    def reverse_pointer(self):
        '''The name of the reverse DNS pointer for the IP address, e.g.:
            >>> ipaddress.ip_address("127.0.0.1").reverse_pointer
            \'1.0.0.127.in-addr.arpa\'
            >>> ipaddress.ip_address("2001:db8::1").reverse_pointer
            \'1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa\'

        '''
        return self._reverse_pointer()

    reverse_pointer = property(reverse_pointer)
    
    def version(self):
        msg = '%200s has no version specified' % (type(self),)
        raise NotImplementedError(msg)

    version = property(version)
    
    def _check_int_address(self, address):
        if address < 0:
            msg = '%d (< 0) is not permitted as an IPv%d address'
            raise AddressValueError(msg % (address, self._version))
        if None > self._ALL_ONES:
            msg = '%d (>= 2**%d) is not permitted as an IPv%d address'
            raise AddressValueError(msg % (address, self._max_prefixlen, self._version))

    
    def _check_packed_address(self, address, expected_len):
        address_len = len(address)
        if address_len != expected_len:
            msg = '%r (len %d != %d) is not permitted as an IPv%d address'
            raise AddressValueError(msg % (address, address_len, expected_len, self._version))

    
    def _ip_int_from_prefix(cls, prefixlen):
        '''Turn the prefix length into a bitwise netmask

        Args:
            prefixlen: An integer, the prefix length.

        Returns:
            An integer.

        '''
        return cls._ALL_ONES ^ cls._ALL_ONES >> prefixlen

    _ip_int_from_prefix = classmethod(_ip_int_from_prefix)
    
    def _prefix_from_ip_int(cls, ip_int):
        '''Return prefix length from the bitwise netmask.

        Args:
            ip_int: An integer, the netmask in expanded bitwise format

        Returns:
            An integer, the prefix length.

        Raises:
            ValueError: If the input intermingles zeroes & ones
        '''
        trailing_zeroes = _count_righthand_zero_bits(ip_int, cls._max_prefixlen)
        prefixlen = cls._max_prefixlen - trailing_zeroes
        leading_ones = ip_int >> trailing_zeroes
        all_ones = (1 << prefixlen) - 1
        if leading_ones != all_ones:
            byteslen = cls._max_prefixlen // 8
            details = ip_int.to_bytes(byteslen, 'big')
            msg = 'Netmask pattern %r mixes zeroes & ones'
            raise ValueError(msg % details)

    _prefix_from_ip_int = classmethod(_prefix_from_ip_int)
    
    def _report_invalid_netmask(cls, netmask_str):
        msg = '%r is not a valid netmask' % netmask_str
        raise NetmaskValueError(msg), None

    _report_invalid_netmask = classmethod(_report_invalid_netmask)
    
    def _prefix_from_prefix_string(cls, prefixlen_str):
        '''Return prefix length from a numeric string

        Args:
            prefixlen_str: The string to be converted

        Returns:
            An integer, the prefix length.

        Raises:
            NetmaskValueError: If the input is not a valid netmask
        '''
        if not prefixlen_str.isascii() or prefixlen_str.isdigit():
            cls._report_invalid_netmask(prefixlen_str)
    # WARNING: Decompyle incomplete

    _prefix_from_prefix_string = classmethod(_prefix_from_prefix_string)
    
    def _prefix_from_ip_string(cls, ip_str):
        '''Turn a netmask/hostmask string into a prefix length

        Args:
            ip_str: The netmask/hostmask to be converted

        Returns:
            An integer, the prefix length.

        Raises:
            NetmaskValueError: If the input is not a valid netmask/hostmask
        '''
        pass
    # WARNING: Decompyle incomplete

    _prefix_from_ip_string = classmethod(_prefix_from_ip_string)
    
    def _split_addr_prefix(cls, address):
        '''Helper function to parse address of Network/Interface.

        Arg:
            address: Argument of Network/Interface.

        Returns:
            (addr, prefix) tuple.
        '''
        if isinstance(address, (bytes, int)):
            return (address, cls._max_prefixlen)
        if not None(address, tuple):
            address = _split_optional_netmask(address)
        if len(address) > 1:
            return address
        return (None[0], cls._max_prefixlen)

    _split_addr_prefix = classmethod(_split_addr_prefix)
    
    def __reduce__(self):
        return (self.__class__, (str(self),))


_address_fmt_re = None
_BaseAddress = functools.total_ordering(<NODE:12>)
_BaseNetwork = functools.total_ordering(<NODE:12>)

class _BaseV4:
    '''Base IPv4 object.

    The following methods are used by IPv4 objects in both single IP
    addresses and networks.

    '''
    __slots__ = ()
    _version = 4
    _ALL_ONES = 2 ** IPV4LENGTH - 1
    _max_prefixlen = IPV4LENGTH
    _netmask_cache = { }
    
    def _explode_shorthand_ip_string(self):
        return str(self)

    
    def _make_netmask(cls, arg):
        '''Make a (netmask, prefix_len) tuple from the given argument.

        Argument can be:
        - an integer (the prefix length)
        - a string representing the prefix length (e.g. "24")
        - a string representing the prefix netmask (e.g. "255.255.255.0")
        '''
        pass
    # WARNING: Decompyle incomplete

    _make_netmask = classmethod(_make_netmask)
    
    def _ip_int_from_string(cls, ip_str):
        """Turn the given IP string into an integer for comparison.

        Args:
            ip_str: A string, the IP ip_str.

        Returns:
            The IP ip_str as an integer.

        Raises:
            AddressValueError: if ip_str isn't a valid IPv4 Address.

        """
        if not ip_str:
            raise AddressValueError('Address cannot be empty')
        octets = None.split('.')
        if len(octets) != 4:
            raise AddressValueError('Expected 4 octets in %r' % ip_str)
        :
            if not ip_str:
                raise AddressValueError('Address cannot be empty')
            octets = None.split('.')
            if len(octets) != 4:
                raise AddressValueError('Expected 4 octets in %r' % ip_str)
            :
                if not ip_str:
                    raise AddressValueError('Address cannot be empty')
                octets = None.split('.')
                if len(octets) != 4:
                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                :
                    if not ip_str:
                        raise AddressValueError('Address cannot be empty')
                    octets = None.split('.')
                    if len(octets) != 4:
                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                    :
                        if not ip_str:
                            raise AddressValueError('Address cannot be empty')
                        octets = None.split('.')
                        if len(octets) != 4:
                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                        :
                            if not ip_str:
                                raise AddressValueError('Address cannot be empty')
                            octets = None.split('.')
                            if len(octets) != 4:
                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                            :
                                if not ip_str:
                                    raise AddressValueError('Address cannot be empty')
                                octets = None.split('.')
                                if len(octets) != 4:
                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                :
                                    if not ip_str:
                                        raise AddressValueError('Address cannot be empty')
                                    octets = None.split('.')
                                    if len(octets) != 4:
                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                    :
                                        if not ip_str:
                                            raise AddressValueError('Address cannot be empty')
                                        octets = None.split('.')
                                        if len(octets) != 4:
                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                        :
                                            if not ip_str:
                                                raise AddressValueError('Address cannot be empty')
                                            octets = None.split('.')
                                            if len(octets) != 4:
                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                            :
                                                if not ip_str:
                                                    raise AddressValueError('Address cannot be empty')
                                                octets = None.split('.')
                                                if len(octets) != 4:
                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                :
                                                    if not ip_str:
                                                        raise AddressValueError('Address cannot be empty')
                                                    octets = None.split('.')
                                                    if len(octets) != 4:
                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                    :
                                                        if not ip_str:
                                                            raise AddressValueError('Address cannot be empty')
                                                        octets = None.split('.')
                                                        if len(octets) != 4:
                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                        :
                                                            if not ip_str:
                                                                raise AddressValueError('Address cannot be empty')
                                                            octets = None.split('.')
                                                            if len(octets) != 4:
                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                            :
                                                                if not ip_str:
                                                                    raise AddressValueError('Address cannot be empty')
                                                                octets = None.split('.')
                                                                if len(octets) != 4:
                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                :
                                                                    if not ip_str:
                                                                        raise AddressValueError('Address cannot be empty')
                                                                    octets = None.split('.')
                                                                    if len(octets) != 4:
                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                    :
                                                                        if not ip_str:
                                                                            raise AddressValueError('Address cannot be empty')
                                                                        octets = None.split('.')
                                                                        if len(octets) != 4:
                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                        :
                                                                            if not ip_str:
                                                                                raise AddressValueError('Address cannot be empty')
                                                                            octets = None.split('.')
                                                                            if len(octets) != 4:
                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                            :
                                                                                if not ip_str:
                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                octets = None.split('.')
                                                                                if len(octets) != 4:
                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                :
                                                                                    if not ip_str:
                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                    octets = None.split('.')
                                                                                    if len(octets) != 4:
                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                    :
                                                                                        if not ip_str:
                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                        octets = None.split('.')
                                                                                        if len(octets) != 4:
                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                        :
                                                                                            if not ip_str:
                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                            octets = None.split('.')
                                                                                            if len(octets) != 4:
                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                            :
                                                                                                if not ip_str:
                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                octets = None.split('.')
                                                                                                if len(octets) != 4:
                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                :
                                                                                                    if not ip_str:
                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                    octets = None.split('.')
                                                                                                    if len(octets) != 4:
                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                    :
                                                                                                        if not ip_str:
                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                        octets = None.split('.')
                                                                                                        if len(octets) != 4:
                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                        :
                                                                                                            if not ip_str:
                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                            octets = None.split('.')
                                                                                                            if len(octets) != 4:
                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                            :
                                                                                                                if not ip_str:
                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                octets = None.split('.')
                                                                                                                if len(octets) != 4:
                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                :
                                                                                                                    if not ip_str:
                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                    octets = None.split('.')
                                                                                                                    if len(octets) != 4:
                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                    :
                                                                                                                        if not ip_str:
                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                        octets = None.split('.')
                                                                                                                        if len(octets) != 4:
                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                        :
                                                                                                                            if not ip_str:
                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                            octets = None.split('.')
                                                                                                                            if len(octets) != 4:
                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                            :
                                                                                                                                if not ip_str:
                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                octets = None.split('.')
                                                                                                                                if len(octets) != 4:
                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                :
                                                                                                                                    if not ip_str:
                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                    octets = None.split('.')
                                                                                                                                    if len(octets) != 4:
                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                    :
                                                                                                                                        if not ip_str:
                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                        octets = None.split('.')
                                                                                                                                        if len(octets) != 4:
                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                        :
                                                                                                                                            if not ip_str:
                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                            octets = None.split('.')
                                                                                                                                            if len(octets) != 4:
                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                            :
                                                                                                                                                if not ip_str:
                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                octets = None.split('.')
                                                                                                                                                if len(octets) != 4:
                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                :
                                                                                                                                                    if not ip_str:
                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                    octets = None.split('.')
                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                    :
                                                                                                                                                        if not ip_str:
                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                        octets = None.split('.')
                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                        :
                                                                                                                                                            if not ip_str:
                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                            octets = None.split('.')
                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                            :
                                                                                                                                                                if not ip_str:
                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                :
                                                                                                                                                                    if not ip_str:
                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                    :
                                                                                                                                                                        if not ip_str:
                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                        :
                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                            :
                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                :
                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                    :
                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                        :
                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                            :
                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                :
                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                    :
                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                        :
                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                            :
                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                :
                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                    :
                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                        :
                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                                if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                                                                octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                                                                if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                                                    raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                                    if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                                                                    octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                                                                    if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                                                        raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                                                        if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                                                                        octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                                                                        if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                                                            raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                                                            if not ip_str:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Address cannot be empty')
                                                                                                                                                                                                                                                                                                                                                                                                                                                            octets = None.split('.')
                                                                                                                                                                                                                                                                                                                                                                                                                                                            if len(octets) != 4:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                raise AddressValueError('Expected 4 octets in %r' % ip_str)
                                                                                                                                                                                         