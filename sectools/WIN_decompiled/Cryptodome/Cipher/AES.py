
__doc__ = "\nModule's constants for the modes of operation supported with AES:\n\n:var MODE_ECB: :ref:`Electronic Code Book (ECB) <ecb_mode>`\n:var MODE_CBC: :ref:`Cipher-Block Chaining (CBC) <cbc_mode>`\n:var MODE_CFB: :ref:`Cipher FeedBack (CFB) <cfb_mode>`\n:var MODE_OFB: :ref:`Output FeedBack (OFB) <ofb_mode>`\n:var MODE_CTR: :ref:`CounTer Mode (CTR) <ctr_mode>`\n:var MODE_OPENPGP:  :ref:`OpenPGP Mode <openpgp_mode>`\n:var MODE_CCM: :ref:`Counter with CBC-MAC (CCM) Mode <ccm_mode>`\n:var MODE_EAX: :ref:`EAX Mode <eax_mode>`\n:var MODE_GCM: :ref:`Galois Counter Mode (GCM) <gcm_mode>`\n:var MODE_SIV: :ref:`Syntethic Initialization Vector (SIV) <siv_mode>`\n:var MODE_OCB: :ref:`Offset Code Book (OCB) <ocb_mode>`\n"
import sys
from Cryptodome.Cipher import _create_cipher
from Cryptodome.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, SmartPointer, c_size_t, c_uint8_ptr
from Cryptodome.Util import _cpu_features
from Cryptodome.Random import get_random_bytes
_cproto = '\n        int AES_start_operation(const uint8_t key[],\n                                size_t key_len,\n                                void **pResult);\n        int AES_encrypt(const void *state,\n                        const uint8_t *in,\n                        uint8_t *out,\n                        size_t data_len);\n        int AES_decrypt(const void *state,\n                        const uint8_t *in,\n                        uint8_t *out,\n                        size_t data_len);\n        int AES_stop_operation(void *state);\n        '
_raw_aes_lib = load_pycryptodome_raw_lib('Cryptodome.Cipher._raw_aes', _cproto)
# WARNING: Decompyle incomplete
