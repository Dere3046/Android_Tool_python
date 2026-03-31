
import re
import sys
import os
from ansi import AnsiFore, AnsiBack, AnsiStyle, Style, BEL
from winterm import WinTerm, WinColor, WinStyle
from win32 import windll, winapi_test
winterm = None
if windll is not None:
    winterm = WinTerm()

class StreamWrapper(object):
    """
    Wraps a stream (such as stdout), acting as a transparent proxy for all
    attribute access apart from method 'write()', which is delegated to our
    Converter instance.
    """
    
    def __init__(self, wrapped, converter):
        self._StreamWrapper__wrapped = wrapped
        self._StreamWrapper__convertor = converter

    
    def __getattr__(self, name):
        return getattr(self._StreamWrapper__wrapped, name)

    
    def __enter__(self, *args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def __exit__(self, *args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def write(self, text):
        self._StreamWrapper__convertor.write(text)

    
    def isatty(self):
        stream = self._StreamWrapper__wrapped
        if 'PYCHARM_HOSTED' in os.environ and stream is not None:
            if stream is sys.__stdout__ or stream is sys.__stderr__:
                return True
            stream_isatty = stream.isatty
        return stream_isatty()
    # WARNING: Decompyle incomplete

    
    def closed(self):
        stream = self._StreamWrapper__wrapped
    # WARNING: Decompyle incomplete

    closed = property(closed)


class AnsiToWin32(object):
    """
    Implements a 'write()' method which, on Windows, will strip ANSI character
    sequences from the text, and if outputting to a tty, will convert them into
    win32 function calls.
    """
    ANSI_CSI_RE = re.compile('\x01?\x1b\\[((?:\\d|;)*)([a-zA-Z])\x02?')
    ANSI_OSC_RE = re.compile('\x01?\x1b\\]([^\x07]*)(\x07)\x02?')
    
    def __init__(self, wrapped, convert, strip, autoreset = (None, None, False)):
        self.wrapped = wrapped
        self.autoreset = autoreset
        self.stream = StreamWrapper(wrapped, self)
        on_windows = os.name == 'nt'
        if on_windows:
            pass
        conversion_supported = winapi_test()
        if strip is None:
            if conversion_supported and not (self.stream.closed):
                pass
            strip = not self.stream.isatty()
        self.strip = strip
        if convert is None:
            if conversion_supported and not (self.stream.closed):
                pass
            convert = self.stream.isatty()
        self.convert = convert
        self.win32_calls = self.get_win32_calls()
        self.on_stderr = self.wrapped is sys.stderr

    
    def should_wrap(self):
        '''
        True if this class is actually needed. If false, then the output
        stream will not be affected, nor will win32 calls be issued, so
        wrapping stdout is not actually required. This will generally be
        False on non-Windows platforms, unless optional functionality like
        autoreset has been requested using kwargs to init()
        '''
        if not self.convert and self.strip:
            pass
        return self.autoreset

    
    def get_win32_calls(self):
        pass
    # WARNING: Decompyle incomplete

    
    def write(self, text):
        if self.strip or self.convert:
            self.write_and_convert(text)
        else:
            self.wrapped.write(text)
            self.wrapped.flush()
        if self.autoreset:
            self.reset_all()
            return None

    
    def reset_all(self):
        if self.convert:
            self.call_win32('m', (0,))
            return None
        if not None.strip or self.stream.closed:
            self.wrapped.write(Style.RESET_ALL)
            return None
        return None

    
    def write_and_convert(self, text):
        '''
        Write the given text to our wrapped stream, stripping any ANSI
        sequences from the text, and optionally converting them into win32
        calls.
        '''
        cursor = 0
        text = self.convert_osc(text)
    # WARNING: Decompyle incomplete

    
    def write_plain_text(self, text, start, end):
        if start < end:
            self.wrapped.write(text[start:end])
            self.wrapped.flush()
            return None

    
    def convert_ansi(self, paramstring, command):
        if self.convert:
            params = self.extract_params(command, paramstring)
            self.call_win32(command, params)
            return None

    
    def extract_params(self, command, paramstring):
        if command in 'Hf':
            params = tuple((lambda .0: for p in .0:
int(p) if len(p) != 0 else 1)(paramstring.split(';')))
            if len(params) < 2:
                params = params + (1,)
                if not len(params) < 2:
                    return params
                params = None((lambda .0: for p in .0:
if len(p) != 0:
int(p)continueNone)(paramstring.split(';')))
                if len(params) == 0:
                    if command in 'JKm':
                        params = (0,)
                        return params
                    if None in 'ABCD':
                        params = (1,)
        return params

    
    def call_win32(self, command, params):
        pass
    # WARNING: Decompyle incomplete

    
    def convert_osc(self, text):
        for match in self.ANSI_OSC_RE.finditer(text):
            (start, end) = match.span()
            text = text[:start] + text[end:]
            (paramstring, command) = match.groups()
            if command == BEL and paramstring.count(';') == 1:
                params = paramstring.split(';')
                if params[0] in '02':
                    winterm.set_title(params[1])
        return text


