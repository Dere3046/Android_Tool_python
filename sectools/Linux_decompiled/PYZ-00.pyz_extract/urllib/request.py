
__doc__ = 'An extensible library for opening URLs using a variety of protocols\n\nThe simplest way to use this module is to call the urlopen function,\nwhich accepts a string containing a URL or a Request object (described\nbelow).  It opens the URL and returns the results as file-like\nobject; the returned object has some extra methods described below.\n\nThe OpenerDirector manages a collection of Handler objects that do\nall the actual work.  Each Handler implements a particular protocol or\noption.  The OpenerDirector is a composite object that invokes the\nHandlers needed to open the requested URL.  For example, the\nHTTPHandler performs HTTP GET and POST requests and deals with\nnon-error returns.  The HTTPRedirectHandler automatically deals with\nHTTP 301, 302, 303 and 307 redirect errors, and the HTTPDigestAuthHandler\ndeals with digest authentication.\n\nurlopen(url, data=None) -- Basic usage is the same as original\nurllib.  pass the url and optionally data to post to an HTTP URL, and\nget a file-like object back.  One difference is that you can also pass\na Request instance instead of URL.  Raises a URLError (subclass of\nOSError); for HTTP errors, raises an HTTPError, which can also be\ntreated as a valid response.\n\nbuild_opener -- Function that creates a new OpenerDirector instance.\nWill install the default handlers.  Accepts one or more Handlers as\narguments, either instances or Handler classes that it will\ninstantiate.  If one of the argument is a subclass of the default\nhandler, the argument will be installed instead of the default.\n\ninstall_opener -- Installs a new opener as the default opener.\n\nobjects of interest:\n\nOpenerDirector -- Sets up the User Agent as the Python-urllib client and manages\nthe Handler classes, while dealing with requests and responses.\n\nRequest -- An object that encapsulates the state of a request.  The\nstate can be as simple as the URL.  It can also include extra HTTP\nheaders, e.g. a User-Agent.\n\nBaseHandler --\n\ninternals:\nBaseHandler and parent\n_call_chain conventions\n\nExample usage:\n\nimport urllib.request\n\n# set up authentication info\nauthinfo = urllib.request.HTTPBasicAuthHandler()\nauthinfo.add_password(realm=\'PDQ Application\',\n                      uri=\'https://mahler:8092/site-updates.py\',\n                      user=\'klem\',\n                      passwd=\'geheim$parole\')\n\nproxy_support = urllib.request.ProxyHandler({"http" : "http://ahad-haam:3128"})\n\n# build a new opener that adds authentication and caching FTP handlers\nopener = urllib.request.build_opener(proxy_support, authinfo,\n                                     urllib.request.CacheFTPHandler)\n\n# install it\nurllib.request.install_opener(opener)\n\nf = urllib.request.urlopen(\'https://www.python.org/\')\n'
import base64
import bisect
import email
import hashlib
import http.client as http
import io
import os
import posixpath
import re
import socket
import string
import sys
import time
import tempfile
import contextlib
import warnings
from urllib.error import URLError, HTTPError, ContentTooShortError
from urllib.parse import urlparse, urlsplit, urljoin, unwrap, quote, unquote, _splittype, _splithost, _splitport, _splituser, _splitpasswd, _splitattr, _splitquery, _splitvalue, _splittag, _to_bytes, unquote_to_bytes, urlunparse
from urllib.response import addinfourl, addclosehook
# WARNING: Decompyle incomplete
