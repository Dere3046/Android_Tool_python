
from  import c_ast

def fix_switch_cases(switch_node):
    """ The 'case' statements in a 'switch' come out of parsing with one
        child node, so subsequent statements are just tucked to the parent
        Compound. Additionally, consecutive (fall-through) case statements
        come out messy. This is a peculiarity of the C grammar. The following:

            switch (myvar) {
                case 10:
                    k = 10;
                    p = k + 1;
                    return 10;
                case 20:
                case 30:
                    return 20;
                default:
                    break;
            }

        Creates this tree (pseudo-dump):

            Switch
                ID: myvar
                Compound:
                    Case 10:
                        k = 10
                    p = k + 1
                    return 10
                    Case 20:
                        Case 30:
                            return 20
                    Default:
                        break

        The goal of this transform is to fix this mess, turning it into the
        following:

            Switch
                ID: myvar
                Compound:
                    Case 10:
                        k = 10
                        p = k + 1
                        return 10
                    Case 20:
                    Case 30:
                        return 20
                    Default:
                        break

        A fixed AST node is returned. The argument may be modified.
    """
    pass
# WARNING: Decompyle incomplete


def _extract_nested_case(case_node, stmts_list):
    ''' Recursively extract consecutive Case statements that are made nested
        by the parser and add them to the stmts_list.
    '''
    if isinstance(case_node.stmts[0], (c_ast.Case, c_ast.Default)):
        stmts_list.append(case_node.stmts.pop())
        _extract_nested_case(stmts_list[-1], stmts_list)
        return None


def fix_atomic_specifiers(decl):
    ''' Atomic specifiers like _Atomic(type) are unusually structured,
        conferring a qualifier upon the contained type.

        This function fixes a decl with atomic specifiers to have a sane AST
        structure, by removing spurious Typename->TypeDecl pairs and attaching
        the _Atomic qualifier in the right place.
    '''
    (decl, found) = _fix_atomic_specifiers_once(decl)
    if not found:
        pass
    
    typ = decl
# WARNING: Decompyle incomplete


def _fix_atomic_specifiers_once(decl):
    """ Performs one 'fix' round of atomic specifiers.
        Returns (modified_decl, found) where found is True iff a fix was made.
    """
    parent = decl
    grandparent = None
    node = decl.type
# WARNING: Decompyle incomplete

