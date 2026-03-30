
import sys
import traceback
from contextlib import contextmanager
from functools import cache
from logging import CRITICAL, DEBUG, ERROR, Formatter, INFO, LogRecord, Logger, StreamHandler, WARNING, getLogger, shutdown
from textwrap import indent
from threading import Lock
from typing import Generator, List
from colorama import Fore, Style, init
from cmd_line_interface.basecmdline import CORE_ERROR, FRONT_END_ERROR
__LOGGER_INSTANCE__: List[Logger] = []
MESSAGE_ONLY_FORMAT_STRING = '%(message)s'
LEVEL_FORMAT_STRING = '%(levelname)s: %(message)s'
TIME_MESSAGE_FORMAT_STRING = f'''[%(asctime)s] {MESSAGE_ONLY_FORMAT_STRING}'''
TIME_LEVEL_FORMAT_STRING = f'''[%(asctime)s] {LEVEL_FORMAT_STRING}'''

class QuietError(Exception):
    '''Raised when we do not want the stack trace to be displayed with the error unless -v is provided.'''
    pass


class TimedLevelFormatter(Formatter):
    '''Like ColorFormatter, this formatter includes the log level only if the record is not at the INFO level.'''
    
    def format(self, record):
        format_string = TIME_MESSAGE_FORMAT_STRING if record.levelno == INFO else TIME_LEVEL_FORMAT_STRING
        return Formatter(format_string).format(record)



class ColorFormatter(Formatter):
    LEVEL_FORMAT = f'''{{}}{LEVEL_FORMAT_STRING}{{}}'''
    INFO_FORMAT = MESSAGE_ONLY_FORMAT_STRING
    
    def formats(self):
        return {
            CRITICAL: self.LEVEL_FORMAT.format(Fore.MAGENTA, Style.RESET_ALL),
            ERROR: self.LEVEL_FORMAT.format(Fore.RED, Style.RESET_ALL),
            WARNING: self.LEVEL_FORMAT.format(Fore.YELLOW, Style.RESET_ALL),
            INFO: self.INFO_FORMAT,
            DEBUG: self.LEVEL_FORMAT.format(Fore.BLUE, Style.RESET_ALL) }

    formats = cache(formats)
    
    def format(self, record):
        return Formatter(self.formats().get(record.levelno, self.INFO_FORMAT)).format(record)



class TimedColorFormatter(ColorFormatter):
    LEVEL_FORMAT = f'''{{}}{TIME_LEVEL_FORMAT_STRING}{{}}'''
    INFO_FORMAT = TIME_LEVEL_FORMAT_STRING


class FilterStreamHandler(StreamHandler):
    
    def __init__(self = None, stream = None, min_level = None, max_level = None):
        self.min_level = min_level
        self.max_level = max_level
        super().__init__(stream)

    
    def emit(self = None, record = None):
        if record.levelno <= record.levelno or record.levelno <= self.max_level:
            pass
        else:
            self.min_level
            return None
        self.min_level().emit(record)
        return None

    __classcell__ = None


def add_color_stream_handlers(logger = None, show_times = None):
    stdout_handler = FilterStreamHandler(sys.stdout, DEBUG, INFO, **('stream', 'min_level', 'max_level'))
    stdout_handler.setFormatter(TimedColorFormatter() if show_times else ColorFormatter())
    stderr_handler = FilterStreamHandler(sys.stderr, WARNING, CRITICAL, **('stream', 'min_level', 'max_level'))
    stderr_handler.setFormatter(TimedColorFormatter() if show_times else ColorFormatter())
    logger.handlers.clear()
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)


def initialize_logger(log_level = None):
    logger = getLogger('sectools')
    logger.setLevel(log_level)
    if not __LOGGER_INSTANCE__:
        init()
        __LOGGER_INSTANCE__.append(logger)
    add_color_stream_handlers(logger)
    sys.excepthook = log_excepthook


def determine_log_level(verbose_level = None):
    if not verbose_level:
        pass
    verbose_level = 0
    return max(WARNING - verbose_level * 10, DEBUG)


def log_excepthook(exctype, value, tb):
    if exctype == KeyboardInterrupt:
        log_error('Keyboard Interrupt Received. Exiting.')
        shutdown()
        sys.exit(FRONT_END_ERROR)
    if exctype == QuietError and __LOGGER_INSTANCE__ and __LOGGER_INSTANCE__[0].level > INFO:
        log_error(value)
    else:
        log_error(indent(''.join(traceback.format_exception(exctype, value, tb)), '  ').strip())
    shutdown()
    sys.exit(CORE_ERROR)


def _log(log_level_func, msg):
    if __LOGGER_INSTANCE__:
        getattr(__LOGGER_INSTANCE__[0], log_level_func)(msg)
        return None


def log_critical(msg):
    _log('critical', msg)


def log_error(msg):
    _log('error', msg)


def log_warning(msg):
    _log('warning', msg)


def log_info(msg):
    _log('info', msg)


def log_debug(msg):
    _log('debug', msg)


class DelayedLogger(Logger):
    '''
    Custom logging class which groups all logs into a single cluster. All logs in the cluster are emitted at the same
    time using a lock to avoid interspersing of log messages in use cases such as multi-threading.

    @param escalate_clusters - Controls whether all clusters are escalated to the highest level of log that already
                               exists in the cluster prior to flushing.
    Other params are inherited from parent with no change in behavior.
    '''
    log_lock = Lock()
    
    def __init__(self = None, name = None, level = None, escalate_clusters = None):
        super().__init__(name, level)
        self.records = []
        self.escalate_clusters = escalate_clusters

    
    def handle(self = None, record = None):
        '''Overrides the default handling behavior to cache logs until the flush method is called.'''
        self.records.append(record)

    
    def flush(self = None):
        '''Emit all the cached records as a single cluster.'''
        max_level = max((lambda .0: for record in .0:
record.levelno)(self.records))
    # WARNING: Decompyle incomplete

    __classcell__ = None


def cluster_logs(cluster_name = None, parent_log = None):
    log_cluster = DelayedLogger(f'''{parent_log.name}.{cluster_name}''')
    log_cluster.parent = parent_log
    yield log_cluster
    log_cluster.flush()

cluster_logs = None(cluster_logs)
