
OUTFILE = '--outfile'
SIGNING_MODE_GROUP = 'Signing Mode'
SIGNING_MODE = '--signing-mode'
ENCRYPTION_MODE_GROUP = 'Encryption Mode'
ENCRYPTION_MODE = '--encryption-mode'
ENCRYPT_THEN_SIGN = '--encrypt-then-sign'
PLUGIN_SIGNER = '--plugin-signer'
SIGN = '--sign'
SECURITY_PROFILE = '--security-profile'
ROOT_KEY = '--root-key'
LOCAL = 'LOCAL'
TEST = 'TEST'
PLUGIN = 'PLUGIN'
QTI = '--qti'
SIGNING_MODE_COMMON_HELP = f'''If {LOCAL}, locally provided signing keys and certificates are used to generate the signature and certificates. If {TEST}, Security Tools\' prepackaged internal test signing keys and certificates are used to generate the signature and certificates. If {PLUGIN}, generation of the signature and certificates is off-loaded to {PLUGIN_SIGNER}.'''
SIGNATURE_FORMAT_GROUP = 'Signature Format'
SIGNATURE_FORMAT = '--signature-format'
AVAILABLE_SIGNATURE_FORMATS = '--available-signature-formats'
SIGNATURE_FORMAT_HELP = f'''Defaults to the signature format in {SECURITY_PROFILE}. Denotes the signature format to be used to sign {OUTFILE}. To list supported signature formats, provide {AVAILABLE_SIGNATURE_FORMATS}.'''
HYBRID_SIGN_GROUP = 'Hybrid Sign'
HYBRID_SIGN = '--hybrid-sign'
PAD_FOR_HYBRID_SIGN = '--pad-for-hybrid-sign'
UIE_ENCRYPTION_DESCRIPTION = 'Applicable only to UIE encryption.'
HIDDEN_ARGS = [
    ENCRYPT_THEN_SIGN,
    HYBRID_SIGN,
    PAD_FOR_HYBRID_SIGN]
