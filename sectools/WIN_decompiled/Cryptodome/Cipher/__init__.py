
import os
from Cryptodome.Cipher._mode_ecb import _create_ecb_cipher
from Cryptodome.Cipher._mode_cbc import _create_cbc_cipher
from Cryptodome.Cipher._mode_cfb import _create_cfb_cipher
from Cryptodome.Cipher._mode_ofb import _create_ofb_cipher
from Cryptodome.Cipher._mode_ctr import _create_ctr_cipher
from Cryptodome.Cipher._mode_openpgp import _create_openpgp_cipher
from Cryptodome.Cipher._mode_ccm import _create_ccm_cipher
from Cryptodome.Cipher._mode_eax import _create_eax_cipher
from Cryptodome.Cipher._mode_siv import _create_siv_cipher
from Cryptodome.Cipher._mode_gcm import _create_gcm_cipher
from Cryptodome.Cipher._mode_ocb import _create_ocb_cipher
_modes = {
    1: _create_ecb_cipher,
    2: _create_cbc_cipher,
    3: _create_cfb_cipher,
    5: _create_ofb_cipher,
    6: _create_ctr_cipher,
    7: _create_openpgp_cipher,
    9: _create_eax_cipher }
_extra_modes = {
    8: _create_ccm_cipher,
    10: _create_siv_cipher,
    11: _create_gcm_cipher,
    12: _create_ocb_cipher }

def _create_cipher(factory, key, mode, *args, **kwargs):
    kwargs['key'] = key
    modes = dict(_modes)
    if kwargs.pop('add_aes_modes', False):
        modes.update(_extra_modes)
    if mode not in modes:
        raise ValueError('Mode not supported')
# WARNING: Decompyle incomplete

