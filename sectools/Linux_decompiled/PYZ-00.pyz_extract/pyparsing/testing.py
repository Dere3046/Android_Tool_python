
from contextlib import contextmanager
from typing import Optional
from core import ParserElement, ParseException, Keyword, __diag__, __compat__

class pyparsing_test:
    '''
    namespace class for classes useful in writing unit tests
    '''
    
    class reset_pyparsing_context:
        __qualname__ = 'pyparsing_test.reset_pyparsing_context'
        __doc__ = '\n        Context manager to be used when writing unit tests that modify pyparsing config values:\n        - packrat parsing\n        - bounded recursion parsing\n        - default whitespace characters.\n        - default keyword characters\n        - literal string auto-conversion class\n        - __diag__ settings\n\n        Example::\n\n            with reset_pyparsing_context():\n                # test that literals used to construct a grammar are automatically suppressed\n                ParserElement.inlineLiteralsUsing(Suppress)\n\n                term = Word(alphas) | Word(nums)\n                group = Group(\'(\' + term[...] + \')\')\n\n                # assert that the \'()\' characters are not included in the parsed tokens\n                self.assertParseAndCheckList(group, "(abc 123 def)", [\'abc\', \'123\', \'def\'])\n\n            # after exiting context manager, literals are converted to Literal expressions again\n        '
        
        def __init__(self):
            self._save_context = { }

        
        def save(self):
            self._save_context['default_whitespace'] = ParserElement.DEFAULT_WHITE_CHARS
            self._save_context['default_keyword_chars'] = Keyword.DEFAULT_KEYWORD_CHARS
            self._save_context['literal_string_class'] = ParserElement._literalStringClass
            self._save_context['verbose_stacktrace'] = ParserElement.verbose_stacktrace
            self._save_context['packrat_enabled'] = ParserElement._packratEnabled
            if ParserElement._packratEnabled:
                self._save_context['packrat_cache_size'] = ParserElement.packrat_cache.size
            else:
                self._save_context['packrat_cache_size'] = None
            self._save_context['packrat_parse'] = ParserElement._parse
            self._save_context['recursion_enabled'] = ParserElement._left_recursion_enabled
            self._save_context['__diag__'] = (lambda .0: pass# WARNING: Decompyle incomplete
)(__diag__._all_names)
            self._save_context['__compat__'] = {
                'collect_all_And_tokens': __compat__.collect_all_And_tokens }
            return self

        
        def restore(self):
            if ParserElement.DEFAULT_WHITE_CHARS != self._save_context['default_whitespace']:
                ParserElement.set_default_whitespace_chars(self._save_context['default_whitespace'])
            ParserElement.verbose_stacktrace = self._save_context['verbose_stacktrace']
            Keyword.DEFAULT_KEYWORD_CHARS = self._save_context['default_keyword_chars']
            ParserElement.inlineLiteralsUsing(self._save_context['literal_string_class'])
            for name, value in self._save_context['__diag__'].items():
                __diag__.enable if value else __diag__.disable(name)
            ParserElement._packratEnabled = False
            if self._save_context['packrat_enabled']:
                ParserElement.enable_packrat(self._save_context['packrat_cache_size'])
            else:
                ParserElement._parse = self._save_context['packrat_parse']
            ParserElement._left_recursion_enabled = self._save_context['recursion_enabled']
            __compat__.collect_all_And_tokens = self._save_context['__compat__']
            return self

        
        def copy(self):
            ret = type(self)()
            ret._save_context.update(self._save_context)
            return ret

        
        def __enter__(self):
            return self.save()

        
        def __exit__(self, *args):
            self.restore()


    
    class TestParseResultsAsserts:
        __qualname__ = 'pyparsing_test.TestParseResultsAsserts'
        __doc__ = '\n        A mixin class to add parse results assertion methods to normal unittest.TestCase classes.\n        '
        
        def assertParseResultsEquals(self, result, expected_list, expected_dict, msg = (None, None, None)):
            '''
            Unit test assertion to compare a :class:`ParseResults` object with an optional ``expected_list``,
            and compare any defined results names with an optional ``expected_dict``.
            '''
            if expected_list is not None:
                self.assertEqual(expected_list, result.as_list(), msg, **('msg',))
            if expected_dict is not None:
                self.assertEqual(expected_dict, result.as_dict(), msg, **('msg',))
                return None

        
        def assertParseAndCheckList(self, expr, test_string, expected_list, msg, verbose = (None, True)):
            '''
            Convenience wrapper assert to test a parser element and input string, and assert that
            the resulting ``ParseResults.asList()`` is equal to the ``expected_list``.
            '''
            result = expr.parse_string(test_string, True, **('parse_all',))
            if verbose:
                print(result.dump())
            else:
                print(result.as_list())
            self.assertParseResultsEquals(result, expected_list, msg, **('expected_list', 'msg'))

        
        def assertParseAndCheckDict(self, expr, test_string, expected_dict, msg, verbose = (None, True)):
            '''
            Convenience wrapper assert to test a parser element and input string, and assert that
            the resulting ``ParseResults.asDict()`` is equal to the ``expected_dict``.
            '''
            result = expr.parse_string(test_string, True, **('parseAll',))
            if verbose:
                print(result.dump())
            else:
                print(result.as_list())
            self.assertParseResultsEquals(result, expected_dict, msg, **('expected_dict', 'msg'))

        
        def assertRunTestResults(self, run_tests_report, expected_parse_results, msg = (None, None)):
            '''
            Unit test assertion to evaluate output of ``ParserElement.runTests()``. If a list of
            list-dict tuples is given as the ``expected_parse_results`` argument, then these are zipped
            with the report tuples returned by ``runTests`` and evaluated using ``assertParseResultsEquals``.
            Finally, asserts that the overall ``runTests()`` success value is ``True``.

            :param run_tests_report: tuple(bool, [tuple(str, ParseResults or Exception)]) returned from runTests
            :param expected_parse_results (optional): [tuple(str, list, dict, Exception)]
            '''
            (run_test_success, run_test_results) = run_tests_report
        # WARNING: Decompyle incomplete

        
        def assertRaisesParseException(self, exc_type, msg = (ParseException, None)):
            pass
        # WARNING: Decompyle incomplete

        assertRaisesParseException = contextmanager(assertRaisesParseException)

    
    def with_line_numbers(s, start_line, end_line = None, expand_tabs = None, eol_mark = staticmethod, mark_spaces = (None, None, True, '|', None, None), mark_control = ('s', str, 'start_line', Optional[int], 'end_line', Optional[int], 'expand_tabs', bool, 'eol_mark', str, 'mark_spaces', Optional[str], 'mark_control', Optional[str], 'return', str)):
        '''
        Helpful method for debugging a parser - prints a string with line and column numbers.
        (Line and column numbers are 1-based.)

        :param s: tuple(bool, str - string to be printed with line and column numbers
        :param start_line: int - (optional) starting line number in s to print (default=1)
        :param end_line: int - (optional) ending line number in s to print (default=len(s))
        :param expand_tabs: bool - (optional) expand tabs to spaces, to match the pyparsing default
        :param eol_mark: str - (optional) string to mark the end of lines, helps visualize trailing spaces (default="|")
        :param mark_spaces: str - (optional) special character to display in place of spaces
        :param mark_control: str - (optional) convert non-printing control characters to a placeholding
                                 character; valid values:
                                 - "unicode" - replaces control chars with Unicode symbols, such as "␍" and "␊"
                                 - any single character string - replace control characters with given string
                                 - None (default) - string is displayed as-is

        :return: str - input string with leading line numbers and column number headers
        '''
        if expand_tabs:
            s = s.expandtabs()
        if mark_control is not None:
            if mark_control == 'unicode':
                tbl = str.maketrans((lambda .0: pass# WARNING: Decompyle incomplete
)(zip(range(0, 33), range(9216, 9267))) | {
                    127: 9249 })
                eol_mark = ''
            else:
                tbl = None((lambda .0 = None: pass# WARNING: Decompyle incomplete
)(list(range(0, 32)) + [
                    127]))
            s = s.translate(tbl)
        if mark_spaces is not None and mark_spaces != ' ':
            if mark_spaces == 'unicode':
                tbl = str.maketrans({
                    9: 9225,
                    32: 9251 })
                s = s.translate(tbl)
            else:
                s = s.replace(' ', mark_spaces)
        if start_line is None:
            start_line = 1
        if end_line is None:
            end_line = len(s)
        end_line = min(end_line, len(s))
        start_line = min(max(1, start_line), end_line)
        if mark_control != 'unicode':
            s_lines = s.splitlines()[start_line - 1:end_line]
        else:
            s_lines = (lambda .0: [ line + '␊' for line in .0 ])(s.split('␊')[start_line - 1:end_line])
        if not s_lines:
            return ''
        lineno_width = None(str(end_line))
        max_line_len = max((lambda .0: for line in .0:
len(line))(s_lines))
        lead = ' ' * (lineno_width + 1)
        if max_line_len >= 99:
            header0 = lead + ''.join((lambda .0: for i in .0:
'{}{}'.format('                                                                                                   ', (i + 1) % 100))(range(max(max_line_len // 100, 1)))) + '\n'
        else:
            header0 = ''
        header1 = header0 + lead + ''.join((lambda .0: for i in .0:
'         {}'.format((i + 1) % 10))(range(-(-max_line_len // 10)))) + '\n'
        header2 = lead + '1234567890' * -(-max_line_len // 10) + '\n'
        return None + None((lambda .0 = None: for i, line in .0:
'{:{}d}:{}{}'.format(i, lineno_width, line, eol_mark))(enumerate(s_lines, start_line, **('start',)))) + '\n'

    with_line_numbers = None(with_line_numbers)

