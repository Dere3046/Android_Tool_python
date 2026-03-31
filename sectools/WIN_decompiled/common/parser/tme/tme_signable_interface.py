
from abc import ABC, abstractmethod
from common.parser.tme.base_tme import BaseTME
from public.tme_signable import TMESignable

class TMESignableInterface(ABC, TMESignable, BaseTME):
    '''This interface needed to be implemented by TME signable objects.'''
    
    def SIGNATURE_JSON_POINTER(self = None):
        '''
        The signable object must provide JSON path to its signature tag. E.g., "SvcDebugPolicy/Signature" for DPR.
        '''
        pass

    SIGNATURE_JSON_POINTER = None(None(SIGNATURE_JSON_POINTER))
    
    def SIGNATURE_ID_JSON_POINTER(self = None):
        '''
        The signable object must provide JSON path to its signature id tag.
        E.g., "SvcDebugPolicy/CmdSigningAlgorithmId" for DPR.
        '''
        pass

    SIGNATURE_ID_JSON_POINTER = None(None(SIGNATURE_ID_JSON_POINTER))
    
    def from_unsigned(cls = None, tme = classmethod):
        '''
        The TME objects (including DPRs) need to know how to verify themselves. In the case of a DPR, when
        created but not yet signed, it could be invalid due to missing signature fields (as the DEC may require it).
        Note that the signature is not always needed, but is enforced by the DEC (for a DPR, that is used as
        an example here).
        Therefore this alternative constructor needed to be implemented by a signable TME object to produce
        a copy of that object, bypassing potential missing signature validations errors.
        '''
        pass

    from_unsigned = None(None(from_unsigned))

