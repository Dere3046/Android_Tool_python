
from Cryptodome.Util._raw_api import load_pycryptodome_raw_lib
_raw_cpuid_lib = load_pycryptodome_raw_lib('Cryptodome.Util._cpuid_c', '\n                                           int have_aes_ni(void);\n                                           int have_clmul(void);\n                                           ')

def have_aes_ni():
    return _raw_cpuid_lib.have_aes_ni()


def have_clmul():
    return _raw_cpuid_lib.have_clmul()

