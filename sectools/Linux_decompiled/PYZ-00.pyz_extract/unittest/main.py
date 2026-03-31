
'''Unittest main program'''
import sys
import argparse
import os
from  import loader, runner
from signals import installHandler
__unittest = True
MAIN_EXAMPLES = 'Examples:\n  %(prog)s test_module               - run tests from test_module\n  %(prog)s module.TestClass          - run tests from module.TestClass\n  %(prog)s module.Class.test_method  - run specified test method\n  %(prog)s path/to/test_file.py      - run tests from test_file.py\n'
MODULE_EXAMPLES = "Examples:\n  %(prog)s                           - run default set of tests\n  %(prog)s MyTestSuite               - run suite 'MyTestSuite'\n  %(prog)s MyTestCase.testSomething  - run MyTestCase.testSomething\n  %(prog)s MyTestCase                - run all 'test*' test methods\n                                       in MyTestCase\n"

def _convert_name(name):
    if os.path.isfile(name) and name.lower().endswith('.py'):
        if os.path.isabs(name):
            rel_path = os.path.relpath(name, os.getcwd())
            if os.path.isabs(rel_path) or rel_path.startswith(os.pardir):
                return name
            name = None
        return name[:-3].replace('\\', '.').replace('/', '.')


def _convert_names(names):
    return (lambda .0: [ _convert_name(name) for name in .0 ])(names)


def _convert_select_pattern(pattern):
    if '*' not in pattern:
        pattern = '*%s*' % pattern
    return pattern


class TestProgram(object):
    '''A command-line program that runs a set of tests; this is primarily
       for making test modules conveniently executable.
    '''
    module = None
    verbosity = 1
    failfast = None
    catchbreak = None
    buffer = None
    progName = None
    warnings = None
    testNamePatterns = None
    _discovery_parser = None
    
    def __init__(self, module, defaultTest, argv, testRunner, testLoader, exit, verbosity, failfast, catchbreak = None, buffer = ('__main__', None, None, None, loader.defaultTestLoader, True, 1, None, None, None, None), warnings = {
        'tb_locals': False }, *, tb_locals):
        if isinstance(module, str):
            self.module = __import__(module)
            for part in module.split('.')[1:]:
                self.module = getattr(self.module, part)
        else:
            self.module = module
        if argv is None:
            argv = sys.argv
        self.exit = exit
        self.failfast = failfast
        self.catchbreak = catchbreak
        self.verbosity = verbosity
        self.buffer = buffer
        self.tb_locals = tb_locals
        if not warnings is None and sys.warnoptions:
            self.warnings = 'default'
        else:
            self.warnings = warnings
        self.defaultTest = defaultTest
        self.testRunner = testRunner
        self.testLoader = testLoader
        self.progName = os.path.basename(argv[0])
        self.parseArgs(argv)
        self.runTests()

    
    def usageExit(self, msg = (None,)):
        if msg:
            print(msg)
        if self._discovery_parser is None:
            self._initArgParsers()
        self._print_help()
        sys.exit(2)

    
    def _print_help(self, *args, **kwargs):
        if self.module is None:
            print(self._main_parser.format_help())
            print(MAIN_EXAMPLES % {
                'prog': self.progName })
            self._discovery_parser.print_help()
            return None
        None(self._main_parser.format_help())
        print(MODULE_EXAMPLES % {
            'prog': self.progName })

    
    def parseArgs(self, argv):
        self._initArgParsers()
        if self.module is None:
            if len(argv) > 1 and argv[1].lower() == 'discover':
                self._do_discovery(argv[2:])
                return None
            None._main_parser.parse_args(argv[1:], self)
            if not self.tests:
                self._do_discovery([])
                return None
        self._main_parser.parse_args(argv[1:], self)
        if self.tests:
            self.testNames = _convert_names(self.tests)
            if __name__ == '__main__':
                self.module = None
            elif self.defaultTest is None:
                self.testNames = None
            elif isinstance(self.defaultTest, str):
                self.testNames = (self.defaultTest,)
            else:
                self.testNames = list(self.defaultTest)
        self.createTests()

    
    def createTests(self, from_discovery, Loader = (False, None)):
        if self.testNamePatterns:
            self.testLoader.testNamePatterns = self.testNamePatterns
        if from_discovery:
            loader = self.testLoader if Loader is None else Loader()
            self.test = loader.discover(self.start, self.pattern, self.top)
            return None
        if None.testNames is None:
            self.test = self.testLoader.loadTestsFromModule(self.module)
            return None
        self.test = None.testLoader.loadTestsFromNames(self.testNames, self.module)

    
    def _initArgParsers(self):
        parent_parser = self._getParentArgParser()
        self._main_parser = self._getMainArgParser(parent_parser)
        self._discovery_parser = self._getDiscoveryArgParser(parent_parser)

    
    def _getParentArgParser(self):
        parser = argparse.ArgumentParser(False, **('add_help',))
        parser.add_argument('-v', '--verbose', 'verbosity', 'store_const', 2, 'Verbose output', **('dest', 'action', 'const', 'help'))
        parser.add_argument('-q', '--quiet', 'verbosity', 'store_const', 0, 'Quiet output', **('dest', 'action', 'const', 'help'))
        parser.add_argument('--locals', 'tb_locals', 'store_true', 'Show local variables in tracebacks', **('dest', 'action', 'help'))
        if self.failfast is None:
            parser.add_argument('-f', '--failfast', 'failfast', 'store_true', 'Stop on first fail or error', **('dest', 'action', 'help'))
            self.failfast = False
        if self.catchbreak is None:
            parser.add_argument('-c', '--catch', 'catchbreak', 'store_true', 'Catch Ctrl-C and display results so far', **('dest', 'action', 'help'))
            self.catchbreak = False
        if self.buffer is None:
            parser.add_argument('-b', '--buffer', 'buffer', 'store_true', 'Buffer stdout and stderr during tests', **('dest', 'action', 'help'))
            self.buffer = False
        if self.testNamePatterns is None:
            parser.add_argument('-k', 'testNamePatterns', 'append', _convert_select_pattern, 'Only run tests which match the given substring', **('dest', 'action', 'type', 'help'))
            self.testNamePatterns = []
        return parser

    
    def _getMainArgParser(self, parent):
        parser = argparse.ArgumentParser([
            parent], **('parents',))
        parser.prog = self.progName
        parser.print_help = self._print_help
        parser.add_argument('tests', '*', 'a list of any number of test modules, classes and test methods.', **('nargs', 'help'))
        return parser

    
    def _getDiscoveryArgParser(self, parent):
        parser = argparse.ArgumentParser([
            parent], **('parents',))
        parser.prog = '%s discover' % self.progName
        parser.epilog = 'For test discovery all test modules must be importable from the top level directory of the project.'
        parser.add_argument('-s', '--start-directory', 'start', "Directory to start discovery ('.' default)", **('dest', 'help'))
        parser.add_argument('-p', '--pattern', 'pattern', "Pattern to match tests ('test*.py' default)", **('dest', 'help'))
        parser.add_argument('-t', '--top-level-directory', 'top', 'Top level directory of project (defaults to start directory)', **('dest', 'help'))
        for arg in ('start', 'pattern', 'top'):
            parser.add_argument(arg, '?', argparse.SUPPRESS, argparse.SUPPRESS, **('nargs', 'default', 'help'))
        return parser

    
    def _do_discovery(self, argv, Loader = (None,)):
        self.start = '.'
        self.pattern = 'test*.py'
        self.top = None
        if argv is not None:
            if self._discovery_parser is None:
                self._initArgParsers()
            self._discovery_parser.parse_args(argv, self)
        self.createTests(True, Loader, **('from_discovery', 'Loader'))

    
    def runTests(self):
        if self.catchbreak:
            installHandler()
        if self.testRunner is None:
            self.testRunner = runner.TextTestRunner
    # WARNING: Decompyle incomplete


main = TestProgram
