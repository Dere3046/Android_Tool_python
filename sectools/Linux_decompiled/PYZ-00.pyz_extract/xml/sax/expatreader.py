
__doc__ = "\nSAX driver for the pyexpat C module.  This driver works with\npyexpat.__version__ == '2.22'.\n"
version = '0.20'
from xml.sax._exceptions import *
from xml.sax.handler import feature_validation, feature_namespaces
from xml.sax.handler import feature_namespace_prefixes
from xml.sax.handler import feature_external_ges, feature_external_pes
from xml.sax.handler import feature_string_interning
from xml.sax.handler import property_xml_string, property_interning_dict
import sys
if sys.platform[:4] == 'java':
    raise SAXReaderNotAvailable('expat not available in Java', None)
# WARNING: Decompyle incomplete
