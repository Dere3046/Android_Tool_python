
import sys
from Cryptodome.Cipher import _create_cipher
from Cryptodome.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, SmartPointer, c_size_t, c_uint8_ptr, c_uint
_raw_blowfish_lib = load_pycryptodome_raw_lib('Cryptodome.Cipher._raw_eksblowfish', '\n        int EKSBlowfish_start_operation(const uint8_t key[],\n                                        size_t key_len,\n                                        const uint8_t salt[16],\n                                        size_t salt_len,\n                                        unsigned cost,\n                                        unsigned invert,\n                                        void **pResult);\n        int EKSBlowfish_encrypt(const void *state,\n                                const uint8_t *in,\n                                uint8_t *out,\n                                size_t data_len);\n        int EKSBlowfish_decrypt(const void *state,\n                                const uint8_t *in,\n                                uint8_t *out,\n                                size_t data_len);\n        int EKSBlowfish_stop_operation(void *state);\n        ')

def _create_base_cipher(dict_parameters):
    '''This method instantiates and returns a smart pointer to
    a low-level base cipher. It will absorb named parameters in
    the process.'''
    pass
# WARNING: Decompyle incomplete


def new(key, mode, salt, cost, invert):
    '''Create a new EKSBlowfish cipher
    
    Args:

      key (bytes, bytearray, memoryview):
        The secret key to use in the symmetric cipher.
        Its length can vary from 0 to 72 bytes.

      mode (one of the supported ``MODE_*`` constants):
        The chaining mode to use for encryption or decryption.

      salt (bytes, bytearray, memoryview):
        The salt that bcrypt uses to thwart rainbow table attacks

      cost (integer):
        The complexity factor in bcrypt

      invert (bool):
        If ``False``, in the inner loop use ``ExpandKey`` first over the salt
        and then over the key, as defined in
        the `original bcrypt specification <https://www.usenix.org/legacy/events/usenix99/provos/provos_html/node4.html>`_.
        If ``True``, reverse the order, as in the first implementation of
        `bcrypt` in OpenBSD.

    :Return: an EKSBlowfish object
    '''
    kwargs = {
        'salt': salt,
        'cost': cost,
        'invert': invert }
# WARNING: Decompyle incomplete

MODE_ECB = 1
block_size = 8
key_size = range(0, 73)
