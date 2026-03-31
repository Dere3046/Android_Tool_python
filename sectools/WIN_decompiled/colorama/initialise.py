
import atexit
import contextlib
import sys
from ansitowin32 import AnsiToWin32
orig_stdout = None
orig_stderr = None
wrapped_stdout = None
wrapped_stderr = None
atexit_done = False

def reset_all():
    if AnsiToWin32 is not None:
        AnsiToWin32(orig_stdout).reset_all()
        return None


def init(autoreset, convert, strip, wrap = (False, None, None, True)):
    global orig_stdout, orig_stderr, wrapped_stdout, wrapped_stdout, wrapped_stderr, wrapped_stderr, atexit_done
    if wrap and any([
        autoreset,
        convert,
        strip]):
        raise ValueError('wrap=False conflicts with any other arg=True')
    orig_stdout = None.stdout
    orig_stderr = sys.stderr
    if sys.stdout is None:
        wrapped_stdout = None
    else:
        sys.stdout = wrapped_stdout = wrap_stream(orig_stdout, convert, strip, autoreset, wrap)
    if sys.stderr is None:
        wrapped_stderr = None
    else:
        sys.stderr = wrapped_stderr = wrap_stream(orig_stderr, convert, strip, autoreset, wrap)
    if not atexit_done:
        atexit.register(reset_all)
        atexit_done = True
        return None


def deinit():
    if orig_stdout is not None:
        sys.stdout = orig_stdout
    if orig_stderr is not None:
        sys.stderr = orig_stderr
        return None


def colorama_text(*args, **kwargs):
    pass
# WARNING: Decompyle incomplete

colorama_text = contextlib.contextmanager(colorama_text)

def reinit():
    if wrapped_stdout is not None:
        sys.stdout = wrapped_stdout
    if wrapped_stderr is not None:
        sys.stderr = wrapped_stderr
        return None


def wrap_stream(stream, convert, strip, autoreset, wrap):
    if wrap:
        wrapper = AnsiToWin32(stream, convert, strip, autoreset, **('convert', 'strip', 'autoreset'))
        if wrapper.should_wrap():
            stream = wrapper.stream
    return stream

