
import re
from ply import lex
from ply.lex import TOKEN

class CLexer(object):
    ''' A lexer for the C language. After building it, set the
        input text with input(), and call token() to get new
        tokens.

        The public attribute filename can be set to an initial
        filename, but the lexer will update it upon #line
        directives.
    '''
    
    def __init__(self, error_func, on_lbrace_func, on_rbrace_func, type_lookup_func):
        """ Create a new Lexer.

            error_func:
                An error function. Will be called with an error
                message, line and column as arguments, in case of
                an error during lexing.

            on_lbrace_func, on_rbrace_func:
                Called when an LBRACE or RBRACE is encountered
                (likely to push/pop type_lookup_func's scope)

            type_lookup_func:
                A type lookup function. Given a string, it must
                return True IFF this string is a name of a type
                that was defined with a typedef earlier.
        """
        self.error_func = error_func
        self.on_lbrace_func = on_lbrace_func
        self.on_rbrace_func = on_rbrace_func
        self.type_lookup_func = type_lookup_func
        self.filename = ''
        self.last_token = None
        self.line_pattern = re.compile('([ \\t]*line\\W)|([ \\t]*\\d+)')
        self.pragma_pattern = re.compile('[ \\t]*pragma\\W')

    
    def build(self, **kwargs):
        ''' Builds the lexer from the specification. Must be
            called after the lexer object is created.

            This method exists separately, because the PLY
            manual warns against calling lex.lex inside
            __init__
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def reset_lineno(self):
        ''' Resets the internal line number counter of the lexer.
        '''
        self.lexer.lineno = 1

    
    def input(self, text):
        self.lexer.input(text)

    
    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token

    
    def find_tok_column(self, token):
        ''' Find the column of the token in its line.
        '''
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        return token.lexpos - last_cr

    
    def _error(self, msg, token):
        location = self._make_tok_location(token)
        self.error_func(msg, location[0], location[1])
        self.lexer.skip(1)

    
    def _make_tok_location(self, token):
        return (token.lineno, self.find_tok_column(token))

    keywords = ('AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE', 'DEFAULT', 'DO', 'DOUBLE', 'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR', 'GOTO', 'IF', 'INLINE', 'INT', 'LONG', 'REGISTER', 'OFFSETOF', 'RESTRICT', 'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT', 'SWITCH', 'TYPEDEF', 'UNION', 'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE', '__INT128')
    keywords_new = ('_BOOL', '_COMPLEX', '_NORETURN', '_THREAD_LOCAL', '_STATIC_ASSERT', '_ATOMIC', '_ALIGNOF', '_ALIGNAS')
    keyword_map = { }
    for keyword in keywords:
        keyword_map[keyword.lower()] = keyword
    for keyword in keywords_new:
        keyword_map[keyword[:2].upper() + keyword[2:].lower()] = keyword
    tokens = keywords + keywords_new + ('ID', 'TYPEID', 'INT_CONST_DEC', 'INT_CONST_OCT', 'INT_CONST_HEX', 'INT_CONST_BIN', 'INT_CONST_CHAR', 'FLOAT_CONST', 'HEX_FLOAT_CONST', 'CHAR_CONST', 'WCHAR_CONST', 'U8CHAR_CONST', 'U16CHAR_CONST', 'U32CHAR_CONST', 'STRING_LITERAL', 'WSTRING_LITERAL', 'U8STRING_LITERAL', 'U16STRING_LITERAL', 'U32STRING_LITERAL', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT', 'LOR', 'LAND', 'LNOT', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE', 'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL', 'LSHIFTEQUAL', 'RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL', 'PLUSPLUS', 'MINUSMINUS', 'ARROW', 'CONDOP', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'COMMA', 'PERIOD', 'SEMI', 'COLON', 'ELLIPSIS', 'PPHASH', 'PPPRAGMA', 'PPPRAGMASTR')
    identifier = '[a-zA-Z_$][0-9a-zA-Z_$]*'
    hex_prefix = '0[xX]'
    hex_digits = '[0-9a-fA-F]+'
    bin_prefix = '0[bB]'
    bin_digits = '[01]+'
    integer_suffix_opt = '(([uU]ll)|([uU]LL)|(ll[uU]?)|(LL[uU]?)|([uU][lL])|([lL][uU]?)|[uU])?'
    decimal_constant = '(0' + integer_suffix_opt + ')|([1-9][0-9]*' + integer_suffix_opt + ')'
    octal_constant = '0[0-7]*' + integer_suffix_opt
    hex_constant = hex_prefix + hex_digits + integer_suffix_opt
    bin_constant = bin_prefix + bin_digits + integer_suffix_opt
    bad_octal_constant = '0[0-7]*[89]'
    simple_escape = '([a-wyzA-Z._~!=&\\^\\-\\\\?\'"]|x(?![0-9a-fA-F]))'
    decimal_escape = '(\\d+)(?!\\d)'
    hex_escape = '(x[0-9a-fA-F]+)(?![0-9a-fA-F])'
    bad_escape = '([\\\\][^a-zA-Z._~^!=&\\^\\-\\\\?\'"x0-9])'
    escape_sequence = '(\\\\(' + simple_escape + '|' + decimal_escape + '|' + hex_escape + '))'
    escape_sequence_start_in_string = '(\\\\[0-9a-zA-Z._~!=&\\^\\-\\\\?\'"])'
    cconst_char = "([^'\\\\\\n]|" + escape_sequence + ')'
    char_const = "'" + cconst_char + "'"
    wchar_const = 'L' + char_const
    u8char_const = 'u8' + char_const
    u16char_const = 'u' + char_const
    u32char_const = 'U' + char_const
    multicharacter_constant = "'" + cconst_char + "{2,4}'"
    unmatched_quote = "('" + cconst_char + "*\\n)|('" + cconst_char + '*$)'
    bad_char_const = "('" + cconst_char + "[^'\n]+')|('')|('" + bad_escape + "[^'\\n]*')"
    string_char = '([^"\\\\\\n]|' + escape_sequence_start_in_string + ')'
    string_literal = '"' + string_char + '*"'
    wstring_literal = 'L' + string_literal
    u8string_literal = 'u8' + string_literal
    u16string_literal = 'u' + string_literal
    u32string_literal = 'U' + string_literal
    bad_string_literal = '"' + string_char + '*' + bad_escape + string_char + '*"'
    exponent_part = '([eE][-+]?[0-9]+)'
    fractional_constant = '([0-9]*\\.[0-9]+)|([0-9]+\\.)'
    floating_constant = '((((' + fractional_constant + ')' + exponent_part + '?)|([0-9]+' + exponent_part + '))[FfLl]?)'
    binary_exponent_part = '([pP][+-]?[0-9]+)'
    hex_fractional_constant = '(((' + hex_digits + ')?\\.' + hex_digits + ')|(' + hex_digits + '\\.))'
    hex_floating_constant = '(' + hex_prefix + '(' + hex_digits + '|' + hex_fractional_constant + ')' + binary_exponent_part + '[FfLl]?)'
    states = (('ppline', 'exclusive'), ('pppragma', 'exclusive'))
    
    def t_PPHASH(self, t):
        '''[ \\t]*\\#'''
        if self.line_pattern.match(t.lexer.lexdata, t.lexer.lexpos, **('pos',)):
            t.lexer.begin('ppline')
            self.pp_line = None
            self.pp_filename = None
            return None
        if None.pragma_pattern.match(t.lexer.lexdata, t.lexer.lexpos, **('pos',)):
            t.lexer.begin('pppragma')
            return None
        t.type = None
        return t

    
    def t_ppline_FILENAME(self, t):
        if self.pp_line is None:
            self._error('filename before line number in #line', t)
            return None
        self.pp_filename = None.value.lstrip('"').rstrip('"')

    t_ppline_FILENAME = TOKEN(string_literal)(t_ppline_FILENAME)
    
    def t_ppline_LINE_NUMBER(self, t):
        if self.pp_line is None:
            self.pp_line = t.value
            return None

    t_ppline_LINE_NUMBER = TOKEN(decimal_constant)(t_ppline_LINE_NUMBER)
    
    def t_ppline_NEWLINE(self, t):
        '''\\n'''
        if self.pp_line is None:
            self._error('line number missing in #line', t)
        else:
            self.lexer.lineno = int(self.pp_line)
            if self.pp_filename is not None:
                self.filename = self.pp_filename
        t.lexer.begin('INITIAL')

    
    def t_ppline_PPLINE(self, t):
        '''line'''
        pass

    t_ppline_ignore = ' \t'
    
    def t_ppline_error(self, t):
        self._error('invalid #line directive', t)

    
    def t_pppragma_NEWLINE(self, t):
        '''\\n'''
        t.lexer.lineno += 1
        t.lexer.begin('INITIAL')

    
    def t_pppragma_PPPRAGMA(self, t):
        '''pragma'''
        return t

    t_pppragma_ignore = ' \t'
    
    def t_pppragma_STR(self, t):
        '''.+'''
        t.type = 'PPPRAGMASTR'
        return t

    
    def t_pppragma_error(self, t):
        self._error('invalid #pragma directive', t)

    t_ignore = ' \t'
    
    def t_NEWLINE(self, t):
        '''\\n+'''
        t.lexer.lineno += t.value.count('\n')

    t_PLUS = '\\+'
    t_MINUS = '-'
    t_TIMES = '\\*'
    t_DIVIDE = '/'
    t_MOD = '%'
    t_OR = '\\|'
    t_AND = '&'
    t_NOT = '~'
    t_XOR = '\\^'
    t_LSHIFT = '<<'
    t_RSHIFT = '>>'
    t_LOR = '\\|\\|'
    t_LAND = '&&'
    t_LNOT = '!'
    t_LT = '<'
    t_GT = '>'
    t_LE = '<='
    t_GE = '>='
    t_EQ = '=='
    t_NE = '!='
    t_EQUALS = '='
    t_TIMESEQUAL = '\\*='
    t_DIVEQUAL = '/='
    t_MODEQUAL = '%='
    t_PLUSEQUAL = '\\+='
    t_MINUSEQUAL = '-='
    t_LSHIFTEQUAL = '<<='
    t_RSHIFTEQUAL = '>>='
    t_ANDEQUAL = '&='
    t_OREQUAL = '\\|='
    t_XOREQUAL = '\\^='
    t_PLUSPLUS = '\\+\\+'
    t_MINUSMINUS = '--'
    t_ARROW = '->'
    t_CONDOP = '\\?'
    t_LPAREN = '\\('
    t_RPAREN = '\\)'
    t_LBRACKET = '\\['
    t_RBRACKET = '\\]'
    t_COMMA = ','
    t_PERIOD = '\\.'
    t_SEMI = ';'
    t_COLON = ':'
    t_ELLIPSIS = '\\.\\.\\.'
    
    def t_LBRACE(self, t):
        self.on_lbrace_func()
        return t

    t_LBRACE = TOKEN('\\{')(t_LBRACE)
    
    def t_RBRACE(self, t):
        self.on_rbrace_func()
        return t

    t_RBRACE = TOKEN('\\}')(t_RBRACE)
    t_STRING_LITERAL = string_literal
    
    def t_FLOAT_CONST(self, t):
        return t

    t_FLOAT_CONST = TOKEN(floating_constant)(t_FLOAT_CONST)
    
    def t_HEX_FLOAT_CONST(self, t):
        return t

    t_HEX_FLOAT_CONST = TOKEN(hex_floating_constant)(t_HEX_FLOAT_CONST)
    
    def t_INT_CONST_HEX(self, t):
        return t

    t_INT_CONST_HEX = TOKEN(hex_constant)(t_INT_CONST_HEX)
    
    def t_INT_CONST_BIN(self, t):
        return t

    t_INT_CONST_BIN = TOKEN(bin_constant)(t_INT_CONST_BIN)
    
    def t_BAD_CONST_OCT(self, t):
        msg = 'Invalid octal constant'
        self._error(msg, t)

    t_BAD_CONST_OCT = TOKEN(bad_octal_constant)(t_BAD_CONST_OCT)
    
    def t_INT_CONST_OCT(self, t):
        return t

    t_INT_CONST_OCT = TOKEN(octal_constant)(t_INT_CONST_OCT)
    
    def t_INT_CONST_DEC(self, t):
        return t

    t_INT_CONST_DEC = TOKEN(decimal_constant)(t_INT_CONST_DEC)
    
    def t_INT_CONST_CHAR(self, t):
        return t

    t_INT_CONST_CHAR = TOKEN(multicharacter_constant)(t_INT_CONST_CHAR)
    
    def t_CHAR_CONST(self, t):
        return t

    t_CHAR_CONST = TOKEN(char_const)(t_CHAR_CONST)
    
    def t_WCHAR_CONST(self, t):
        return t

    t_WCHAR_CONST = TOKEN(wchar_const)(t_WCHAR_CONST)
    
    def t_U8CHAR_CONST(self, t):
        return t

    t_U8CHAR_CONST = TOKEN(u8char_const)(t_U8CHAR_CONST)
    
    def t_U16CHAR_CONST(self, t):
        return t

    t_U16CHAR_CONST = TOKEN(u16char_const)(t_U16CHAR_CONST)
    
    def t_U32CHAR_CONST(self, t):
        return t

    t_U32CHAR_CONST = TOKEN(u32char_const)(t_U32CHAR_CONST)
    
    def t_UNMATCHED_QUOTE(self, t):
        msg = "Unmatched '"
        self._error(msg, t)

    t_UNMATCHED_QUOTE = TOKEN(unmatched_quote)(t_UNMATCHED_QUOTE)
    
    def t_BAD_CHAR_CONST(self, t):
        msg = 'Invalid char constant %s' % t.value
        self._error(msg, t)

    t_BAD_CHAR_CONST = TOKEN(bad_char_const)(t_BAD_CHAR_CONST)
    
    def t_WSTRING_LITERAL(self, t):
        return t

    t_WSTRING_LITERAL = TOKEN(wstring_literal)(t_WSTRING_LITERAL)
    
    def t_U8STRING_LITERAL(self, t):
        return t

    t_U8STRING_LITERAL = TOKEN(u8string_literal)(t_U8STRING_LITERAL)
    
    def t_U16STRING_LITERAL(self, t):
        return t

    t_U16STRING_LITERAL = TOKEN(u16string_literal)(t_U16STRING_LITERAL)
    
    def t_U32STRING_LITERAL(self, t):
        return t

    t_U32STRING_LITERAL = TOKEN(u32string_literal)(t_U32STRING_LITERAL)
    
    def t_BAD_STRING_LITERAL(self, t):
        msg = 'String contains invalid escape code'
        self._error(msg, t)

    t_BAD_STRING_LITERAL = TOKEN(bad_string_literal)(t_BAD_STRING_LITERAL)
    
    def t_ID(self, t):
        t.type = self.keyword_map.get(t.value, 'ID')
        if t.type == 'ID' and self.type_lookup_func(t.value):
            t.type = 'TYPEID'
        return t

    t_ID = TOKEN(identifier)(t_ID)
    
    def t_error(self, t):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)


