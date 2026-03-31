
'''Running tests'''
import sys
import time
import warnings
from  import result
from signals import registerResult
__unittest = True

class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""
    
    def __init__(self, stream):
        self.stream = stream

    
    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return None(self.stream, attr)

    
    def writeln(self, arg = (None,)):
        if arg:
            self.write(arg)
        self.write('\n')



class TextTestResult(result.TestResult):
    '''A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    '''
    separator1 = '======================================================================'
    separator2 = '----------------------------------------------------------------------'
    
    def __init__(self = None, stream = None, descriptions = None, verbosity = None):
        super(TextTestResult, self).__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    
    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        return None(test)

    
    def startTest(self = None, test = None):
        super(TextTestResult, self).startTest(test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(' ... ')
            self.stream.flush()
            return None

    
    def addSuccess(self = None, test = None):
        super(TextTestResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln('ok')
            self.stream.flush()
            return None
        if None.dots:
            self.stream.write('.')
            self.stream.flush()
            return None

    
    def addError(self = None, test = None, err = None):
        super(TextTestResult, self).addError(test, err)
        if self.showAll:
            self.stream.writeln('ERROR')
            self.stream.flush()
            return None
        if None.dots:
            self.stream.write('E')
            self.stream.flush()
            return None

    
    def addFailure(self = None, test = None, err = None):
        super(TextTestResult, self).addFailure(test, err)
        if self.showAll:
            self.stream.writeln('FAIL')
            self.stream.flush()
            return None
        if None.dots:
            self.stream.write('F')
            self.stream.flush()
            return None

    
    def addSkip(self = None, test = None, reason = None):
        super(TextTestResult, self).addSkip(test, reason)
        if self.showAll:
            self.stream.writeln('skipped {0!r}'.format(reason))
            self.stream.flush()
            return None
        if None.dots:
            self.stream.write('s')
            self.stream.flush()
            return None

    
    def addExpectedFailure(self = None, test = None, err = None):
        super(TextTestResult, self).addExpectedFailure(test, err)
        if self.showAll:
            self.stream.writeln('expected failure')
            self.stream.flush()
            return None
        if None.dots:
            self.stream.write('x')
            self.stream.flush()
            return None

    
    def addUnexpectedSuccess(self = None, test = None):
        super(TextTestResult, self).addUnexpectedSuccess(test)
        if self.showAll:
            self.stream.writeln('unexpected success')
            self.stream.flush()
            return None
        if None.dots:
            self.stream.write('u')
            self.stream.flush()
            return None

    
    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
            self.stream.flush()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    
    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln('%s: %s' % (flavour, self.getDescription(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln('%s' % err)
            self.stream.flush()

    __classcell__ = None


class TextTestRunner(object):
    '''A test runner class that displays results in textual form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    '''
    resultclass = TextTestResult
    
    def __init__(self, stream, descriptions, verbosity, failfast, buffer = None, resultclass = (None, True, 1, False, False, None, None), warnings = {
        'tb_locals': False }, *, tb_locals):
        '''Construct a TextTestRunner.

        Subclasses should accept **kwargs to ensure compatibility as the
        interface changes.
        '''
        if stream is None:
            stream = sys.stderr
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        self.tb_locals = tb_locals
        self.warnings = warnings
        if resultclass is not None:
            self.resultclass = resultclass
            return None

    
    def _makeResult(self):
        return self.resultclass(self.stream, self.descriptions, self.verbosity)

    
    def run(self, test):
        '''Run the given test case or test suite.'''
        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        result.tb_locals = self.tb_locals
    # WARNING: Decompyle incomplete


