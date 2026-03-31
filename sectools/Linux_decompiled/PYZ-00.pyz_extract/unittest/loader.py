
'''Loading unittests.'''
import os
import re
import sys
import traceback
import types
import functools
import warnings
from fnmatch import fnmatch, fnmatchcase
from  import case, suite, util
__unittest = True
VALID_MODULE_NAME = re.compile('[_a-z]\\w*\\.py$', re.IGNORECASE)

class _FailedTest(case.TestCase):
    _testMethodName = None
    
    def __init__(self = None, method_name = None, exception = None):
        self._exception = exception
        super(_FailedTest, self).__init__(method_name)

    
    def __getattr__(self = None, name = None):
        if name != self._testMethodName:
            return super(_FailedTest, self).__getattr__(name)
        
        def testFailure():
            raise self._exception

        return testFailure

    __classcell__ = None


def _make_failed_import_test(name, suiteClass):
    message = 'Failed to import test module: %s\n%s' % (name, traceback.format_exc())
    return _make_failed_test(name, ImportError(message), suiteClass, message)


def _make_failed_load_tests(name, exception, suiteClass):
    message = 'Failed to call load_tests:\n%s' % (traceback.format_exc(),)
    return _make_failed_test(name, exception, suiteClass, message)


def _make_failed_test(methodname, exception, suiteClass, message):
    test = _FailedTest(methodname, exception)
    return (suiteClass((test,)), message)


def _make_skipped_test(methodname, exception, suiteClass):
    
    def testSkipped(self):
        pass

    testSkipped = case.skip(str(exception))(testSkipped)
    attrs = {
        methodname: testSkipped }
    TestClass = type('ModuleSkipped', (case.TestCase,), attrs)
    return suiteClass((TestClass(methodname),))


def _jython_aware_splitext(path):
    if path.lower().endswith('$py.class'):
        return path[:-9]
    return None.path.splitext(path)[0]


class TestLoader(object):
    '''
    This class is responsible for loading tests according to various criteria
    and returning them wrapped in a TestSuite
    '''
    testMethodPrefix = 'test'
    sortTestMethodsUsing = staticmethod(util.three_way_cmp)
    testNamePatterns = None
    suiteClass = suite.TestSuite
    _top_level_dir = None
    
    def __init__(self = None):
        super(TestLoader, self).__init__()
        self.errors = []
        self._loading_packages = set()

    
    def loadTestsFromTestCase(self, testCaseClass):
        '''Return a suite of all test cases contained in testCaseClass'''
        if issubclass(testCaseClass, suite.TestSuite):
            raise TypeError('Test cases should not be derived from TestSuite. Maybe you meant to derive from TestCase?')
        testCaseNames = None.getTestCaseNames(testCaseClass)
        if testCaseNames and hasattr(testCaseClass, 'runTest'):
            testCaseNames = [
                'runTest']
        loaded_suite = self.suiteClass(map(testCaseClass, testCaseNames))
        return loaded_suite

    
    def loadTestsFromModule(self = None, module = {
        'pattern': None }, *, pattern, *args, **kws):
        '''Return a suite of all test cases contained in the given module'''
        if len(args) > 0 or 'use_load_tests' in kws:
            warnings.warn('use_load_tests is deprecated and ignored', DeprecationWarning)
            kws.pop('use_load_tests', None)
        if len(args) > 1:
            complaint = len(args) + 1
            raise TypeError('loadTestsFromModule() takes 1 positional argument but {} were given'.format(complaint))
        if None(kws) != 0:
            complaint = sorted(kws)[0]
            raise TypeError("loadTestsFromModule() got an unexpected keyword argument '{}'".format(complaint))
        tests = None
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, case.TestCase):
                tests.append(self.loadTestsFromTestCase(obj))
        load_tests = getattr(module, 'load_tests', None)
        tests = self.suiteClass(tests)
    # WARNING: Decompyle incomplete

    
    def loadTestsFromName(self, name, module = (None,)):
        '''Return a suite of all test cases given a string specifier.

        The name may resolve either to a module, a test case class, a
        test method within a test case class, or a callable object which
        returns a TestCase or TestSuite instance.

        The method optionally resolves the names relative to a given module.
        '''
        parts = name.split('.')
        (error_case, error_message) = (None, None)
    # WARNING: Decompyle incomplete

    
    def loadTestsFromNames(self, names, module = (None,)):
        """Return a suite of all test cases found using the given sequence
        of string specifiers. See 'loadTestsFromName()'.
        """
        suites = (lambda .0 = None: [ self.loadTestsFromName(name, module) for name in .0 ])(names)
        return self.suiteClass(suites)

    
    def getTestCaseNames(self, testCaseClass):
        '''Return a sorted sequence of method names found within testCaseClass
        '''
        
        def shouldIncludeMethod(attrname = None):
            if not attrname.startswith(self.testMethodPrefix):
                return False
            testFunc = None(testCaseClass, attrname)
            if not callable(testFunc):
                return False
            fullName = None % (testCaseClass.__module__, testCaseClass.__qualname__, attrname)
            if not self.testNamePatterns is None:
                pass
            return None((lambda .0 = None: for pattern in .0:
fnmatchcase(fullName, pattern))(self.testNamePatterns))

        testFnNames = list(filter(shouldIncludeMethod, dir(testCaseClass)))
        if self.sortTestMethodsUsing:
            testFnNames.sort(functools.cmp_to_key(self.sortTestMethodsUsing), **('key',))
        return testFnNames

    
    def discover(self, start_dir, pattern, top_level_dir = ('test*.py', None)):
        """Find and return all test modules from the specified start
        directory, recursing into subdirectories to find them and return all
        tests found within them. Only test files that match the pattern will
        be loaded. (Using shell style pattern matching.)

        All test modules must be importable from the top level of the project.
        If the start directory is not the top level directory then the top
        level directory must be specified separately.

        If a test package name (directory with '__init__.py') matches the
        pattern then the package will be checked for a 'load_tests' function. If
        this exists then it will be called with (loader, tests, pattern) unless
        the package has already had load_tests called from the same discovery
        invocation, in which case the package module object is not scanned for
        tests - this ensures that when a package uses discover to further
        discover child tests that infinite recursion does not happen.

        If load_tests exists then discovery does *not* recurse into the package,
        load_tests is responsible for loading all tests in the package.

        The pattern is deliberately not stored as a loader attribute so that
        packages can continue discovery themselves. top_level_dir is stored so
        load_tests does not need to pass this argument in to loader.discover().

        Paths are sorted before being imported to ensure reproducible execution
        order even on filesystems with non-alphabetical ordering like ext3/4.
        """
        set_implicit_top = False
        if top_level_dir is None and self._top_level_dir is not None:
            top_level_dir = self._top_level_dir
        elif top_level_dir is None:
            set_implicit_top = True
            top_level_dir = start_dir
        top_level_dir = os.path.abspath(top_level_dir)
        if top_level_dir not in sys.path:
            sys.path.insert(0, top_level_dir)
        self._top_level_dir = top_level_dir
        is_not_importable = False
        is_namespace = False
        tests = []
    # WARNING: Decompyle incomplete

    
    def _get_directory_containing_module(self, module_name):
        module = sys.modules[module_name]
        full_path = os.path.abspath(module.__file__)
        if os.path.basename(full_path).lower().startswith('__init__.py'):
            return os.path.dirname(os.path.dirname(full_path))
        return None.path.dirname(full_path)

    
    def _get_name_from_path(self, path):
        if path == self._top_level_dir:
            return '.'
        path = None(os.path.normpath(path))
        _relpath = os.path.relpath(path, self._top_level_dir)
    # WARNING: Decompyle incomplete

    
    def _get_module_from_name(self, name):
        __import__(name)
        return sys.modules[name]

    
    def _match_path(self, path, full_path, pattern):
        return fnmatch(path, pattern)

    
    def _find_tests(self, start_dir, pattern, namespace = (False,)):
        '''Used by discovery. Yields test suites it loads.'''
        name = self._get_name_from_path(start_dir)
    # WARNING: Decompyle incomplete

    
    def _find_test_path(self, full_path, pattern, namespace = (False,)):
        """Used by discovery.

        Loads tests from a single file, or a directories' __init__.py when
        passed the directory.

        Returns a tuple (None_or_tests_from_file, should_recurse).
        """
        basename = os.path.basename(full_path)
    # WARNING: Decompyle incomplete

    __classcell__ = None

defaultTestLoader = TestLoader()

def _makeLoader(prefix, sortUsing, suiteClass, testNamePatterns = (None, None)):
    loader = TestLoader()
    loader.sortTestMethodsUsing = sortUsing
    loader.testMethodPrefix = prefix
    loader.testNamePatterns = testNamePatterns
    if suiteClass:
        loader.suiteClass = suiteClass
    return loader


def getTestCaseNames(testCaseClass, prefix, sortUsing, testNamePatterns = (util.three_way_cmp, None)):
    return _makeLoader(prefix, sortUsing, testNamePatterns, **('testNamePatterns',)).getTestCaseNames(testCaseClass)


def makeSuite(testCaseClass, prefix, sortUsing, suiteClass = ('test', util.three_way_cmp, suite.TestSuite)):
    return _makeLoader(prefix, sortUsing, suiteClass).loadTestsFromTestCase(testCaseClass)


def findTestCases(module, prefix, sortUsing, suiteClass = ('test', util.three_way_cmp, suite.TestSuite)):
    return _makeLoader(prefix, sortUsing, suiteClass).loadTestsFromModule(module)

