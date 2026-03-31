
__doc__ = '\nAn XML-RPC client interface for Python.\n\nThe marshalling and response parser code can also be used to\nimplement XML-RPC servers.\n\nExported exceptions:\n\n  Error          Base class for client errors\n  ProtocolError  Indicates an HTTP protocol error\n  ResponseError  Indicates a broken response package\n  Fault          Indicates an XML-RPC fault package\n\nExported classes:\n\n  ServerProxy    Represents a logical connection to an XML-RPC server\n\n  MultiCall      Executor of boxcared xmlrpc requests\n  DateTime       dateTime wrapper for an ISO 8601 string or time tuple or\n                 localtime integer value to generate a "dateTime.iso8601"\n                 XML-RPC value\n  Binary         binary data wrapper\n\n  Marshaller     Generate an XML-RPC params chunk from a Python data structure\n  Unmarshaller   Unmarshal an XML-RPC response from incoming XML event message\n  Transport      Handles an HTTP transaction to an XML-RPC server\n  SafeTransport  Handles an HTTPS transaction to an XML-RPC server\n\nExported constants:\n\n  (none)\n\nExported functions:\n\n  getparser      Create instance of the fastest available parser & attach\n                 to an unmarshalling object\n  dumps          Convert an argument tuple or a Fault instance to an XML-RPC\n                 request (or response, if the methodresponse option is used).\n  loads          Convert an XML-RPC packet to unmarshalled data plus a method\n                 name (None if not present).\n'
import base64
import sys
import time
from datetime import datetime
from decimal import Decimal
import http.client as http
import urllib.parse as urllib
from xml.parsers import expat
import errno
from io import BytesIO
# WARNING: Decompyle incomplete
