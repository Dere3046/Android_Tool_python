
import re
import types
import sys
import os.path as os
import inspect
import base64
import warnings
__version__ = '3.10'
__tabversion__ = '3.10'
yaccdebug = True
debug_file = 'parser.out'
tab_module = 'parsetab'
default_lr = 'LALR'
error_count = 3
yaccdevel = False
resultlimit = 40
pickle_protocol = 0
if sys.version_info[0] < 3:
    string_types = basestring
else:
    string_types = str
MAXINT = sys.maxsize

class PlyLogger(object):
    
    def __init__(self, f):
        self.f = f

    
    def debug(self, msg, *args, **kwargs):
        self.f.write(msg % args + '\n')

    info = debug
    
    def warning(self, msg, *args, **kwargs):
        self.f.write('WARNING: ' + msg % args + '\n')

    
    def error(self, msg, *args, **kwargs):
        self.f.write('ERROR: ' + msg % args + '\n')

    critical = debug


class NullLogger(object):
    
    def __getattribute__(self, name):
        return self

    
    def __call__(self, *args, **kwargs):
        return self



class YaccError(Exception):
    pass


def format_result(r):
    repr_str = repr(r)
    if '\n' in repr_str:
        repr_str = repr(repr_str)
    if len(repr_str) > resultlimit:
        repr_str = repr_str[:resultlimit] + ' ...'
    result = '<%s @ 0x%x> (%s)' % (type(r).__name__, id(r), repr_str)
    return result


def format_stack_entry(r):
    repr_str = repr(r)
    if '\n' in repr_str:
        repr_str = repr(repr_str)
    if len(repr_str) < 16:
        return repr_str
    return None % (type(r).__name__, id(r))

_errok = None
_token = None
_restart = None
_warnmsg = "PLY: Don't use global functions errok(), token(), and restart() in p_error().\nInstead, invoke the methods on the associated parser instance:\n\n    def p_error(p):\n        ...\n        # Use parser.errok(), parser.token(), parser.restart()\n        ...\n\n    parser = yacc.yacc()\n"

def errok():
    warnings.warn(_warnmsg)
    return _errok()


def restart():
    warnings.warn(_warnmsg)
    return _restart()


def token():
    warnings.warn(_warnmsg)
    return _token()


def call_errorfunc(errorfunc, token, parser):
    global _errok, _token, _restart, _errok, _token, _restart
    _errok = parser.errok
    _token = parser.token
    _restart = parser.restart
    r = errorfunc(token)
# WARNING: Decompyle incomplete


class YaccSymbol:
    
    def __str__(self):
        return self.type

    
    def __repr__(self):
        return str(self)



class YaccProduction:
    
    def __init__(self, s, stack = (None,)):
        self.slice = s
        self.stack = stack
        self.lexer = None
        self.parser = None

    
    def __getitem__(self, n):
        if isinstance(n, slice):
            return (lambda .0: [ s.value for s in .0 ])(self.slice[n])
        if None >= 0:
            return self.slice[n].value
        return None.stack[n].value

    
    def __setitem__(self, n, v):
        self.slice[n].value = v

    
    def __getslice__(self, i, j):
        return (lambda .0: [ s.value for s in .0 ])(self.slice[i:j])

    
    def __len__(self):
        return len(self.slice)

    
    def lineno(self, n):
        return getattr(self.slice[n], 'lineno', 0)

    
    def set_lineno(self, n, lineno):
        self.slice[n].lineno = lineno

    
    def linespan(self, n):
        startline = getattr(self.slice[n], 'lineno', 0)
        endline = getattr(self.slice[n], 'endlineno', startline)
        return (startline, endline)

    
    def lexpos(self, n):
        return getattr(self.slice[n], 'lexpos', 0)

    
    def lexspan(self, n):
        startpos = getattr(self.slice[n], 'lexpos', 0)
        endpos = getattr(self.slice[n], 'endlexpos', startpos)
        return (startpos, endpos)

    
    def error(self):
        raise SyntaxError



class LRParser:
    
    def __init__(self, lrtab, errorf):
        self.productions = lrtab.lr_productions
        self.action = lrtab.lr_action
        self.goto = lrtab.lr_goto
        self.errorfunc = errorf
        self.set_defaulted_states()
        self.errorok = True

    
    def errok(self):
        self.errorok = True

    
    def restart(self):
        del self.statestack[:]
        del self.symstack[:]
        sym = YaccSymbol()
        sym.type = '$end'
        self.symstack.append(sym)
        self.statestack.append(0)

    
    def set_defaulted_states(self):
        self.defaulted_states = { }
        for state, actions in self.action.items():
            rules = list(actions.values())
            if len(rules) == 1 and rules[0] < 0:
                self.defaulted_states[state] = rules[0]

    
    def disable_defaulted_states(self):
        self.defaulted_states = { }

    
    def parse(self, input, lexer, debug, tracking, tokenfunc = (None, None, False, False, None)):
        if debug or yaccdevel:
            if isinstance(debug, int):
                debug = PlyLogger(sys.stderr)
            return self.parsedebug(input, lexer, debug, tracking, tokenfunc)
        if None:
            return self.parseopt(input, lexer, debug, tracking, tokenfunc)
        return None.parseopt_notrack(input, lexer, debug, tracking, tokenfunc)

    
    def parsedebug(self, input, lexer, debug, tracking, tokenfunc = (None, None, False, False, None)):
        lookahead = None
        lookaheadstack = []
        actions = self.action
        goto = self.goto
        prod = self.productions
        defaulted_states = self.defaulted_states
        pslice = YaccProduction(None)
        errorcount = 0
        debug.info('PLY: PARSE DEBUG START')
        if not lexer:
            lex = lex
            import 
            lexer = lex.lexer
        pslice.lexer = lexer
        pslice.parser = self
        if input is not None:
            lexer.input(input)
        if tokenfunc is None:
            get_token = lexer.token
        else:
            get_token = tokenfunc
        self.token = get_token
        statestack = []
        self.statestack = statestack
        symstack = []
        self.symstack = symstack
        pslice.stack = symstack
        errtoken = None
        statestack.append(0)
        sym = YaccSymbol()
        sym.type = '$end'
        symstack.append(sym)
        state = 0
        debug.debug('')
        debug.debug('State  : %s', state)
        if state not in defaulted_states:
            if not lookahead:
                if not lookaheadstack:
                    lookahead = get_token()
                else:
                    lookahead = lookaheadstack.pop()
                if not lookahead:
                    lookahead = YaccSymbol()
                    lookahead.type = '$end'
            ltype = lookahead.type
            t = actions[state].get(ltype)
        else:
            t = defaulted_states[state]
            debug.debug('Defaulted state %s: Reduce using %d', state, -t)
        debug.debug('Stack  : %s', ('%s . %s' % (' '.join((lambda .0: [ xx.type for xx in .0 ])(symstack)[1:]), str(lookahead))).lstrip())
    # WARNING: Decompyle incomplete

    
    def parseopt(self, input, lexer, debug, tracking, tokenfunc = (None, None, False, False, None)):
        lookahead = None
        lookaheadstack = []
        actions = self.action
        goto = self.goto
        prod = self.productions
        defaulted_states = self.defaulted_states
        pslice = YaccProduction(None)
        errorcount = 0
        if not lexer:
            lex = lex
            import 
            lexer = lex.lexer
        pslice.lexer = lexer
        pslice.parser = self
        if input is not None:
            lexer.input(input)
        if tokenfunc is None:
            get_token = lexer.token
        else:
            get_token = tokenfunc
        self.token = get_token
        statestack = []
        self.statestack = statestack
        symstack = []
        self.symstack = symstack
        pslice.stack = symstack
        errtoken = None
        statestack.append(0)
        sym = YaccSymbol()
        sym.type = '$end'
        symstack.append(sym)
        state = 0
        if state not in defaulted_states:
            if not lookahead:
                if not lookaheadstack:
                    lookahead = get_token()
                else:
                    lookahead = lookaheadstack.pop()
                if not lookahead:
                    lookahead = YaccSymbol()
                    lookahead.type = '$end'
            ltype = lookahead.type
            t = actions[state].get(ltype)
        else:
            t = defaulted_states[state]
    # WARNING: Decompyle incomplete

    
    def parseopt_notrack(self, input, lexer, debug, tracking, tokenfunc = (None, None, False, False, None)):
        lookahead = None
        lookaheadstack = []
        actions = self.action
        goto = self.goto
        prod = self.productions
        defaulted_states = self.defaulted_states
        pslice = YaccProduction(None)
        errorcount = 0
        if not lexer:
            lex = lex
            import 
            lexer = lex.lexer
        pslice.lexer = lexer
        pslice.parser = self
        if input is not None:
            lexer.input(input)
        if tokenfunc is None:
            get_token = lexer.token
        else:
            get_token = tokenfunc
        self.token = get_token
        statestack = []
        self.statestack = statestack
        symstack = []
        self.symstack = symstack
        pslice.stack = symstack
        errtoken = None
        statestack.append(0)
        sym = YaccSymbol()
        sym.type = '$end'
        symstack.append(sym)
        state = 0
        if state not in defaulted_states:
            if not lookahead:
                if not lookaheadstack:
                    lookahead = get_token()
                else:
                    lookahead = lookaheadstack.pop()
                if not lookahead:
                    lookahead = YaccSymbol()
                    lookahead.type = '$end'
            ltype = lookahead.type
            t = actions[state].get(ltype)
        else:
            t = defaulted_states[state]
    # WARNING: Decompyle incomplete


_is_identifier = re.compile('^[a-zA-Z0-9_-]+$')

class Production(object):
    reduced = 0
    
    def __init__(self, number, name, prod, precedence, func, file, line = (('right', 0), None, '', 0)):
        self.name = name
        self.prod = tuple(prod)
        self.number = number
        self.func = func
        self.callable = None
        self.file = file
        self.line = line
        self.prec = precedence
        self.len = len(self.prod)
        self.usyms = []
        for s in self.prod:
            if s not in self.usyms:
                self.usyms.append(s)
        self.lr_items = []
        self.lr_next = None
        if self.prod:
            self.str = '%s -> %s' % (self.name, ' '.join(self.prod))
            return None
        self.str = None % self.name

    
    def __str__(self):
        return self.str

    
    def __repr__(self):
        return 'Production(' + str(self) + ')'

    
    def __len__(self):
        return len(self.prod)

    
    def __nonzero__(self):
        return 1

    
    def __getitem__(self, index):
        return self.prod[index]

    
    def lr_item(self, n):
        if n > len(self.prod):
            return None
        p = None(self, n)
    # WARNING: Decompyle incomplete

    
    def bind(self, pdict):
        if self.func:
            self.callable = pdict[self.func]
            return None



class MiniProduction(object):
    
    def __init__(self, str, name, len, func, file, line):
        self.name = name
        self.len = len
        self.func = func
        self.callable = None
        self.file = file
        self.line = line
        self.str = str

    
    def __str__(self):
        return self.str

    
    def __repr__(self):
        return 'MiniProduction(%s)' % self.str

    
    def bind(self, pdict):
        if self.func:
            self.callable = pdict[self.func]
            return None



class LRItem(object):
    
    def __init__(self, p, n):
        self.name = p.name
        self.prod = list(p.prod)
        self.number = p.number
        self.lr_index = n
        self.lookaheads = { }
        self.prod.insert(n, '.')
        self.prod = tuple(self.prod)
        self.len = len(self.prod)
        self.usyms = p.usyms

    
    def __str__(self):
        if self.prod:
            s = '%s -> %s' % (self.name, ' '.join(self.prod))
            return s
        s = None % self.name
        return s

    
    def __repr__(self):
        return 'LRItem(' + str(self) + ')'



def rightmost_terminal(symbols, terminals):
    i = len(symbols) - 1
    if i >= 0:
        if symbols[i] in terminals:
            return symbols[i]
        None -= 1
        if not i >= 0:
            return None


class GrammarError(YaccError):
    pass


class Grammar(object):
    
    def __init__(self, terminals):
        self.Productions = [
            None]
        self.Prodnames = { }
        self.Prodmap = { }
        self.Terminals = { }
        for term in terminals:
            self.Terminals[term] = []
        self.Terminals['error'] = []
        self.Nonterminals = { }
        self.First = { }
        self.Follow = { }
        self.Precedence = { }
        self.UsedPrecedence = set()
        self.Start = None

    
    def __len__(self):
        return len(self.Productions)

    
    def __getitem__(self, index):
        return self.Productions[index]

    
    def set_precedence(self, term, assoc, level):
        pass
    # WARNING: Decompyle incomplete

    
    def add_production(self, prodname, syms, func, file, line = (None, '', 0)):
        if prodname in self.Terminals:
            raise GrammarError('%s:%d: Illegal rule name %r. Already defined as a token' % (file, line, prodname))
        if None == 'error':
            raise GrammarError('%s:%d: Illegal rule name %r. error is a reserved word' % (file, line, prodname))
        if not None.match(prodname):
            raise GrammarError('%s:%d: Illegal rule name %r' % (file, line, prodname))
    # WARNING: Decompyle incomplete

    
    def set_start(self, start = (None,)):
        if not start:
            start = self.Productions[1].name
        if start not in self.Nonterminals:
            raise GrammarError('start symbol %s undefined' % start)
        self.Productions[0] = None(0, "S'", [
            start])
        self.Nonterminals[start].append(0)
        self.Start = start

    
    def find_unreachable(self):
        
        def mark_reachable_from(s = None):
            if s in reachable:
                return None
            None.add(s)
            for p in self.Prodnames.get(s, []):
                for r in p.prod:
                    mark_reachable_from(r)

        reachable = set()
        mark_reachable_from(self.Productions[0].prod[0])
        return (lambda .0 = None: [ s for s in .0 if s not in reachable ])(self.Nonterminals)

    
    def infinite_cycles(self):
        terminates = { }
        for t in self.Terminals:
            terminates[t] = True
        terminates['$end'] = True
        for n in self.Nonterminals:
            terminates[n] = False
        some_change = False
        for n, pl in self.Prodnames.items():
            for p in pl:
                for s in p.prod:
                    if not terminates[s]:
                        p_terminates = False
                    
                    p_terminates = True
                    if p_terminates:
                        if not terminates[n]:
                            terminates[n] = True
                            some_change = True
                        continue
        if not some_change:
            pass
        
        infinite = []
        for s, term in terminates.items():
            if not term:
                if s not in self.Prodnames and s not in self.Terminals and s != 'error':
                    continue
                infinite.append(s)
        return infinite

    
    def undefined_symbols(self):
        result = []
        for p in self.Productions:
            if not p:
                continue
            for s in p.prod:
                if s not in self.Prodnames and s not in self.Terminals and s != 'error':
                    result.append((s, p))
        return result

    
    def unused_terminals(self):
        unused_tok = []
        for s, v in self.Terminals.items():
            if not s != 'error' and v:
                unused_tok.append(s)
        return unused_tok

    
    def unused_rules(self):
        unused_prod = []
        for s, v in self.Nonterminals.items():
            if not v:
                p = self.Prodnames[s][0]
                unused_prod.append(p)
        return unused_prod

    
    def unused_precedence(self):
        unused = []
        for termname in self.Precedence:
            if not termname in self.Terminals and termname in self.UsedPrecedence:
                unused.append((termname, self.Precedence[termname][0]))
        return unused

    
    def _first(self, beta):
        result = []
        for x in beta:
            x_produces_empty = False
            for f in self.First[x]:
                if f == '<empty>':
                    x_produces_empty = True
                    continue
                if f not in result:
                    result.append(f)
            if x_produces_empty:
                continue
            return result
            result.append('<empty>')
            return result

    
    def compute_first(self):
        if self.First:
            return self.First
        for t in None.Terminals:
            self.First[t] = [
                t]
        self.First['$end'] = [
            '$end']
        for n in self.Nonterminals:
            self.First[n] = []
        some_change = False
        for n in self.Nonterminals:
            for p in self.Prodnames[n]:
                for f in self._first(p.prod):
                    if f not in self.First[n]:
                        self.First[n].append(f)
                        some_change = True
        if not some_change:
            return self.First

    
    def compute_follow(self, start = (None,)):
        if self.Follow:
            return self.Follow
        if not None.First:
            self.compute_first()
        for k in self.Nonterminals:
            self.Follow[k] = []
        if not start:
            start = self.Productions[1].name
        self.Follow[start] = [
            '$end']
        didadd = False
        for p in self.Productions[1:]:
            for i, B in enumerate(p.prod):
                if B in self.Nonterminals:
                    fst = self._first(p.prod[i + 1:])
                    hasempty = False
                    for f in fst:
                        if f != '<empty>' and f not in self.Follow[B]:
                            self.Follow[B].append(f)
                            didadd = True
                        if f == '<empty>':
                            hasempty = True
                    if hasempty or i == len(p.prod) - 1:
                        for f in self.Follow[p.name]:
                            if f not in self.Follow[B]:
                                self.Follow[B].append(f)
                                didadd = True
        if not didadd:
            return self.Follow

    
    def build_lritems(self):
        pass
    # WARNING: Decompyle incomplete



class VersionError(YaccError):
    pass


class LRTable(object):
    
    def __init__(self):
        self.lr_action = None
        self.lr_goto = None
        self.lr_productions = None
        self.lr_method = None

    
    def read_table(self, module):
        if isinstance(module, types.ModuleType):
            parsetab = module
        else:
            exec('import %s' % module)
            parsetab = sys.modules[module]
        if parsetab._tabversion != __tabversion__:
            raise VersionError('yacc table file version is out of date')
        self.lr_action = None._lr_action
        self.lr_goto = parsetab._lr_goto
        self.lr_productions = []
    # WARNING: Decompyle incomplete

    
    def read_pickle(self, filename):
        pass
    # WARNING: Decompyle incomplete

    
    def bind_callables(self, pdict):
        for p in self.lr_productions:
            p.bind(pdict)



def digraph(X, R, FP):
    N = { }
    for x in X:
        N[x] = 0
    stack = []
    F = { }
    for x in X:
        if N[x] == 0:
            traverse(x, N, stack, F, X, R, FP)
    return F


def traverse(x, N, stack, F, X, R, FP):
    stack.append(x)
    d = len(stack)
    N[x] = d
    F[x] = FP(x)
    rel = R(x)
    for y in rel:
        if N[y] == 0:
            traverse(y, N, stack, F, X, R, FP)
        N[x] = min(N[x], N[y])
        for a in F.get(y, []):
            if a not in F[x]:
                F[x].append(a)
    if N[x] == d:
        N[stack[-1]] = MAXINT
        F[stack[-1]] = F[x]
        element = stack.pop()
        if element != x:
            N[stack[-1]] = MAXINT
            F[stack[-1]] = F[x]
            element = stack.pop()
            if not element != x:
                return None
            return None
        return None


class LALRError(YaccError):
    pass


class LRGeneratedTable(LRTable):
    
    def __init__(self, grammar, method, log = ('LALR', None)):
        if method not in ('SLR', 'LALR'):
            raise LALRError('Unsupported method %s' % method)
        self.grammar = None
        self.lr_method = method
        if not log:
            log = NullLogger()
        self.log = log
        self.lr_action = { }
        self.lr_goto = { }
        self.lr_productions = grammar.Productions
        self.lr_goto_cache = { }
        self.lr0_cidhash = { }
        self._add_count = 0
        self.sr_conflict = 0
        self.rr_conflict = 0
        self.conflicts = []
        self.sr_conflicts = []
        self.rr_conflicts = []
        self.grammar.build_lritems()
        self.grammar.compute_first()
        self.grammar.compute_follow()
        self.lr_parse_table()

    
    def lr0_closure(self, I):
        self._add_count += 1
        J = I[:]
        didadd = True
        if didadd:
            didadd = False
            for j in J:
                for x in j.lr_after:
                    if getattr(x, 'lr0_added', 0) == self._add_count:
                        continue
                    J.append(x.lr_next)
                    x.lr0_added = self._add_count
                    didadd = True
            if not didadd:
                return J

    
    def lr0_goto(self, I, x):
        g = self.lr_goto_cache.get((id(I), x))
        if g:
            return g
        s = None.lr_goto_cache.get(x)
        if not s:
            s = { }
            self.lr_goto_cache[x] = s
        gs = []
        for p in I:
            n = p.lr_next
            if n and n.lr_before == x:
                s1 = s.get(id(n))
                if not s1:
                    s1 = { }
                    s[id(n)] = s1
                gs.append(n)
                s = s1
        g = s.get('$end')
        if not g:
            if gs:
                g = self.lr0_closure(gs)
                s['$end'] = g
            else:
                s['$end'] = gs
        self.lr_goto_cache[(id(I), x)] = g
        return g

    
    def lr0_items(self):
        C = [
            self.lr0_closure([
                self.grammar.Productions[0].lr_next])]
        i = 0
        for I in C:
            self.lr0_cidhash[id(I)] = i
            i += 1
        i = 0
        if i < len(C):
            I = C[i]
            i += 1
            asyms = { }
            for ii in I:
                for s in ii.usyms:
                    asyms[s] = None
            for x in asyms:
                g = self.lr0_goto(I, x)
                if g or id(g) in self.lr0_cidhash:
                    continue
                self.lr0_cidhash[id(g)] = len(C)
                C.append(g)
            if not i < len(C):
                return C

    
    def compute_nullable_nonterminals(self):
        nullable = set()
        num_nullable = 0
        for p in self.grammar.Productions[1:]:
            if p.len == 0:
                nullable.add(p.name)
                continue
            for t in p.prod:
                if t not in nullable:
                    continue
            nullable.add(p.name)
        if len(nullable) == num_nullable:
            return nullable
        num_nullable = None(nullable)
        continue

    
    def find_nonterminal_transitions(self, C):
        trans = []
        for stateno, state in enumerate(C):
            for p in state:
                if p.lr_index < p.len - 1:
                    t = (stateno, p.prod[p.lr_index + 1])
                    if t[1] in self.grammar.Nonterminals and t not in trans:
                        trans.append(t)
        return trans

    
    def dr_relation(self, C, trans, nullable):
        dr_set = { }
        (state, N) = trans
        terms = []
        g = self.lr0_goto(C[state], N)
        for p in g:
            if p.lr_index < p.len - 1:
                a = p.prod[p.lr_index + 1]
                if a in self.grammar.Terminals and a not in terms:
                    terms.append(a)
        if state == 0 and N == self.grammar.Productions[0].prod[0]:
            terms.append('$end')
        return terms

    
    def reads_relation(self, C, trans, empty):
        rel = []
        (state, N) = trans
        g = self.lr0_goto(C[state], N)
        j = self.lr0_cidhash.get(id(g), -1)
        for p in g:
            if p.lr_index < p.len - 1:
                a = p.prod[p.lr_index + 1]
                if a in empty:
                    rel.append((j, a))
        return rel

    
    def compute_lookback_includes(self, C, trans, nullable):
        lookdict = { }
        includedict = { }
        dtrans = { }
        for t in trans:
            dtrans[t] = 1
        for state, N in trans:
            lookb = []
            includes = []
            for p in C[state]:
                if p.name != N:
                    continue
                lr_index = p.lr_index
                j = state
                if lr_index < p.len - 1:
                    lr_index = lr_index + 1
                    t = p.prod[lr_index]
                    if (j, t) in dtrans:
                        li = lr_index + 1
                        if li < p.len:
                            if p.prod[li] in self.grammar.Terminals:
                                pass
                            elif p.prod[li] not in nullable:
                                pass
                            else:
                                li = li + 1
                                if not li < p.len:
                                    includes.append((j, t))
                                    g = self.lr0_goto(C[j], t)
                                    j = self.lr0_cidhash.get(id(g), -1)
                                    if not lr_index < p.len - 1:
                                        for r in C[j]:
                                            if r.name != p.name:
                                                continue
                                            if r.len != p.len:
                                                continue
                                            i = 0
                                            if i < r.lr_index:
                                                if r.prod[i] != p.prod[i + 1]:
                                                    continue
                                                i = i + 1
                                                if not i < r.lr_index:
                                                    lookb.append((j, r))
                                                    continue
                                                    continue
                                                    for i in includes:
                                                        if i not in includedict:
                                                            includedict[i] = []
                                                        includedict[i].append((state, N))
                                                    lookdict[(state, N)] = lookb
                                                    continue
                                                    return (lookdict, includedict)

    
    def compute_read_sets(self, C, ntrans, nullable):
        
        FP = lambda x = None: self.dr_relation(C, x, nullable)
        
        R = lambda x = None: self.reads_relation(C, x, nullable)
        F = digraph(ntrans, R, FP)
        return F

    
    def compute_follow_sets(self, ntrans, readsets, inclsets):
        
        FP = lambda x = None: readsets[x]
        
        R = lambda x = None: inclsets.get(x, [])
        F = digraph(ntrans, R, FP)
        return F

    
    def add_lookaheads(self, lookbacks, followset):
        for trans, lb in lookbacks.items():
            for state, p in lb:
                if state not in p.lookaheads:
                    p.lookaheads[state] = []
                f = followset.get(trans, [])
                for a in f:
                    if a not in p.lookaheads[state]:
                        p.lookaheads[state].append(a)

    
    def add_lalr_lookaheads(self, C):
        nullable = self.compute_nullable_nonterminals()
        trans = self.find_nonterminal_transitions(C)
        readsets = self.compute_read_sets(C, trans, nullable)
        (lookd, included) = self.compute_lookback_includes(C, trans, nullable)
        followsets = self.compute_follow_sets(trans, readsets, included)
        self.add_lookaheads(lookd, followsets)

    
    def lr_parse_table(self):
        Productions = self.grammar.Productions
        Precedence = self.grammar.Precedence
        goto = self.lr_goto
        action = self.lr_action
        log = self.log
        actionp = { }
        log.info('Parsing method: %s', self.lr_method)
        C = self.lr0_items()
        if self.lr_method == 'LALR':
            self.add_lalr_lookaheads(C)
        st = 0
        for I in C:
            actlist = []
            st_action = { }
            st_actionp = { }
            st_goto = { }
            log.info('')
            log.info('state %d', st)
            log.info('')
            for p in I:
                log.info('    (%d) %s', p.number, p)
            log.info('')
            for p in I:
                if p.len == p.lr_index + 1:
                    if p.name == "S'":
                        st_action['$end'] = 0
                        st_actionp['$end'] = p
                        continue
                    if self.lr_method == 'LALR':
                        laheads = p.lookaheads[st]
                    else:
                        laheads = self.grammar.Follow[p.name]
                    for a in laheads:
                        actlist.append((a, p, 'reduce using rule %d (%s)' % (p.number, p)))
                        r = st_action.get(a)
                        if r is not None:
                            if r > 0:
                                (sprec, slevel) = Precedence.get(a, ('right', 0))
                                (rprec, rlevel) = Productions[p.number].prec
                                if (slevel < rlevel or slevel == rlevel) and rprec == 'left':
                                    st_action[a] = -(p.number)
                                    st_actionp[a] = p
                                    if not slevel and rlevel:
                                        log.info('  ! shift/reduce conflict for %s resolved as reduce', a)
                                        self.sr_conflicts.append((st, a, 'reduce'))
                                    Productions[p.number].reduced += 1
                                    continue
                                if slevel == rlevel and rprec == 'nonassoc':
                                    st_action[a] = None
                                    continue
                                if not rlevel:
                                    log.info('  ! shift/reduce conflict for %s resolved as shift', a)
                                    self.sr_conflicts.append((st, a, 'shift'))
                                continue
                            if r < 0:
                                oldp = Productions[-r]
                                pp = Productions[p.number]
                                self.rr_conflicts.append((st, chosenp, rejectp))
                                log.info('  ! reduce/reduce conflict for %s resolved using rule %d (%s)', a, st_actionp[a].number, st_actionp[a])
                                continue
                            raise LALRError('Unknown conflict in state %d' % st)
                        st_action[a] = -(None.number)
                        st_actionp[a] = p
                        Productions[p.number].reduced += 1
                i = p.lr_index
                a = p.prod[i + 1]
                if a in self.grammar.Terminals:
                    g = self.lr0_goto(I, a)
                    j = self.lr0_cidhash.get(id(g), -1)
                    if j >= 0:
                        actlist.append((a, p, 'shift and go to state %d' % j))
                        r = st_action.get(a)
                        if r is not None:
                            if r > 0:
                                if r != j:
                                    raise LALRError('Shift/shift conflict in state %d' % st)
                            if r < 0:
                                (sprec, slevel) = Precedence.get(a, ('right', 0))
                                (rprec, rlevel) = Productions[st_actionp[a].number].prec
                                if (slevel > rlevel or slevel == rlevel) and rprec == 'right':
                                    Productions[st_actionp[a].number].reduced -= 1
                                    st_action[a] = j
                                    st_actionp[a] = p
                                    if not rlevel:
                                        log.info('  ! shift/reduce conflict for %s resolved as shift', a)
                                        self.sr_conflicts.append((st, a, 'shift'))
                                    continue
                                if slevel == rlevel and rprec == 'nonassoc':
                                    st_action[a] = None
                                    continue
                                if not slevel and rlevel:
                                    log.info('  ! shift/reduce conflict for %s resolved as reduce', a)
                                    self.sr_conflicts.append((st, a, 'reduce'))
                                continue
                            raise LALRError('Unknown conflict in state %d' % st)
                        st_action[a] = Productions[p.number]
                        st_actionp[a] = p
            _actprint = { }
            for a, p, m in actlist:
                if a in st_action and p is st_actionp[a]:
                    log.info('    %-15s %s', a, m)
                    _actprint[(a, m)] = 1
            log.info('')
            not_used = 0
            for a, p, m in actlist:
                if a in st_action and p is not st_actionp[a] and (a, m) not in _actprint:
                    log.debug('  ! %-15s [ %s ]', a, m)
                    not_used = 1
                    _actprint[(a, m)] = 1
            if not_used:
                log.debug('')
            nkeys = { }
            for ii in I:
                for s in ii.usyms:
                    if s in self.grammar.Nonterminals:
                        nkeys[s] = None
            for n in nkeys:
                g = self.lr0_goto(I, n)
                j = self.lr0_cidhash.get(id(g), -1)
                if j >= 0:
                    st_goto[n] = j
                    log.info('    %-30s shift and go to state %d', n, j)
            action[st] = st_action
            actionp[st] = st_actionp
            goto[st] = st_goto
            st += 1

    
    def write_table(self, tabmodule, outputdir, signature = ('', '')):
        if isinstance(tabmodule, types.ModuleType):
            raise IOError("Won't overwrite existing tabmodule")
        basemodulename = None.split('.')[-1]
        filename = os.path.join(outputdir, basemodulename) + '.py'
    # WARNING: Decompyle incomplete

    
    def pickle_table(self, filename, signature = ('',)):
        pass
    # WARNING: Decompyle incomplete



def get_caller_module_dict(levels):
    f = sys._getframe(levels)
    ldict = f.f_globals.copy()
    if f.f_globals != f.f_locals:
        ldict.update(f.f_locals)
    return ldict


def parse_grammar(doc, file, line):
    grammar = []
    pstrings = doc.splitlines()
    lastp = None
    dline = line
# WARNING: Decompyle incomplete


class ParserReflect(object):
    
    def __init__(self, pdict, log = (None,)):
        self.pdict = pdict
        self.start = None
        self.error_func = None
        self.tokens = None
        self.modules = set()
        self.grammar = []
        self.error = False
        if log is None:
            self.log = PlyLogger(sys.stderr)
            return None
        self.log = None

    
    def get_all(self):
        self.get_start()
        self.get_error_func()
        self.get_tokens()
        self.get_precedence()
        self.get_pfunctions()

    
    def validate_all(self):
        self.validate_start()
        self.validate_error_func()
        self.validate_tokens()
        self.validate_precedence()
        self.validate_pfunctions()
        self.validate_modules()
        return self.error

    
    def signature(self):
        parts = []
    # WARNING: Decompyle incomplete

    
    def validate_modules(self):
        fre = re.compile('\\s*def\\s+(p_[a-zA-Z_0-9]*)\\(')
    # WARNING: Decompyle incomplete

    
    def get_start(self):
        self.start = self.pdict.get('start')

    
    def validate_start(self):
        if not self.start is not None or isinstance(self.start, string_types):
            self.log.error("'start' must be a string")
            return None
        return None

    
    def get_error_func(self):
        self.error_func = self.pdict.get('p_error')

    
    def validate_error_func(self):
        if self.error_func:
            if isinstance(self.error_func, types.FunctionType):
                ismethod = 0
            elif isinstance(self.error_func, types.MethodType):
                ismethod = 1
            else:
                self.log.error("'p_error' defined, but is not a function or method")
                self.error = True
                return None
            eline = None.error_func.__code__.co_firstlineno
            efile = self.error_func.__code__.co_filename
            module = inspect.getmodule(self.error_func)
            self.modules.add(module)
            argcount = self.error_func.__code__.co_argcount - ismethod
            if argcount != 1:
                self.log.error('%s:%d: p_error() requires 1 argument', efile, eline)
                self.error = True
                return None
            return None

    
    def get_tokens(self):
        tokens = self.pdict.get('tokens')
        if not tokens:
            self.log.error('No token list is defined')
            self.error = True
            return None
        if not None(tokens, (list, tuple)):
            self.log.error('tokens must be a list or tuple')
            self.error = True
            return None
        if not None:
            self.log.error('tokens is empty')
            self.error = True
            return None
        self.tokens = None

    
    def validate_tokens(self):
        if 'error' in self.tokens:
            self.log.error("Illegal token name 'error'. Is a reserved word")
            self.error = True
            return None
        terminals = None()
        for n in self.tokens:
            if n in terminals:
                self.log.warning('Token %r multiply defined', n)
            terminals.add(n)

    
    def get_precedence(self):
        self.prec = self.pdict.get('precedence')

    
    def validate_precedence(self):
        preclist = []
        if self.prec:
            if not isinstance(self.prec, (list, tuple)):
                self.log.error('precedence must be a list or tuple')
                self.error = True
                return None
            for level, p in None(self.prec):
                if not isinstance(p, (list, tuple)):
                    self.log.error('Bad precedence table')
                    self.error = True
                    return None
                if None(p) < 2:
                    self.log.error('Malformed precedence entry %s. Must be (assoc, term, ..., term)', p)
                    self.error = True
                    return None
                assoc = None[0]
                if not isinstance(assoc, string_types):
                    self.log.error('precedence associativity must be a string')
                    self.error = True
                    return None
                for term in None[1:]:
                    if not isinstance(term, string_types):
                        self.log.error('precedence items must be strings')
                        self.error = True
                        return None
                    None.append((term, assoc, level + 1))
        self.preclist = preclist

    
    def get_pfunctions(self):
        p_functions = []
        for name, item in self.pdict.items():
            if name.startswith('p_') or name == 'p_error':
                continue
            if isinstance(item, (types.FunctionType, types.MethodType)):
                line = getattr(item, 'co_firstlineno', item.__code__.co_firstlineno)
                module = inspect.getmodule(item)
                p_functions.append((line, module, name, item.__doc__))
        p_functions.sort((lambda p_function: (p_function[0], str(p_function[1]), p_function[2], p_function[3])), **('key',))
        self.pfuncs = p_functions

    
    def validate_pfunctions(self):
        grammar = []
        if len(self.pfuncs) == 0:
            self.log.error('no rules of the form p_rulename are defined')
            self.error = True
            return None
    # WARNING: Decompyle incomplete



def yacc(method, debug, module, tabmodule, start, check_recursion, optimize, write_tables, debugfile, outputdir, debuglog, errorlog, picklefile = ('LALR', yaccdebug, None, tab_module, None, True, False, True, debug_file, None, None, None, None)):
    global parse
    if tabmodule is None:
        tabmodule = tab_module
    if picklefile:
        write_tables = 0
    if errorlog is None:
        errorlog = PlyLogger(sys.stderr)
    if module:
        _items = (lambda .0 = None: [ (k, getattr(module, k)) for k in .0 ])(dir(module))
        pdict = dict(_items)
        if '__file__' not in pdict:
            pdict['__file__'] = sys.modules[pdict['__module__']].__file__
        else:
            pdict = get_caller_module_dict(2)
    if outputdir is None:
        if isinstance(tabmodule, types.ModuleType):
            srcfile = tabmodule.__file__
        elif '.' not in tabmodule:
            srcfile = pdict['__file__']
        else:
            parts = tabmodule.split('.')
            pkgname = '.'.join(parts[:-1])
            exec('import %s' % pkgname)
            srcfile = getattr(sys.modules[pkgname], '__file__', '')
        outputdir = os.path.dirname(srcfile)
    pkg = pdict.get('__package__')
    if pkg and isinstance(tabmodule, str) and '.' not in tabmodule:
        tabmodule = pkg + '.' + tabmodule
    if start is not None:
        pdict['start'] = start
    pinfo = ParserReflect(pdict, errorlog, **('log',))
    pinfo.get_all()
    if pinfo.error:
        raise YaccError('Unable to build parser')
    signature = None.signature()
# WARNING: Decompyle incomplete

