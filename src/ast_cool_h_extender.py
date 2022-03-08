# Tokens terminals
from enum import Enum, auto
from typing import List
from ast_cool_hierarchy import *


class TOKEN_TYPE(Enum):
    LINEBREAK = auto()
    TAB = auto()
    NXTPAGE = auto()
    SPACE = auto()
    DIV = auto()
    MULT = auto()
    PLUS = auto()
    MINUS = auto()
    EQ = auto()
    LT = auto()
    LTEQ = auto()
    ASSIGN = auto()
    ACTION = auto()
    INT_COMP = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    DOT = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    AT = auto()
    CLASS = auto()
    INHERITS = auto()
    NEW = auto()
    ISVOID = auto()
    IN = auto()
    CASE = auto()
    OF = auto()
    ESAC = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    FI = auto()
    WHILE = auto()
    LOOP = auto()
    POOL = auto()
    LET = auto()
    NOT = auto()
    INTEGER = auto()
    TRUE = auto()
    FALSE = auto()
    SELF_TYPE = auto()
    TYPE_ID = auto()
    SELF_OBJECT = auto()
    OBJECT_ID = auto()
    STRING = auto()
    LINECOMMENT = auto()
    MULTILINECOMMENT = auto()


class ListNode:
    def __new__(cls, *args):
        args = args[2:]
        list_ret = []
        first = args[0] if len(args) > 0 else None
        second = args[1] if len(args) > 1 else None

        if isinstance(first, list):
            list_ret.extend(first)
        elif first is not None:
            list_ret.append(first)

        if isinstance(second, list):
            list_ret.extend(second)
        elif second is not None:
            list_ret.append(second)
        return list_ret

    # def __init__(self, line_no,col_no,list_=None, elem=None):
    #    if isinstance(list_, ListNode):
    #        self.extend(list_)
    #    elif list_ is not None:
    #        self.append(list_)
    #    if isinstance(elem, ListNode):
    #        self.extend(elem)
    #    elif elem is not None:
    #        self.append(elem)
    #    self.line_no=self[0].line_no if len(self) else -1
    #    self.col_no=self[0].col_no if len(self) else -1


class TupleWrapper:
    def __new__(cls, *args):
        args = args[2:]
        return tuple(args)


class ClassDeclarationWrapper:
    def __new__(cls, *args):
        args = list(args)
        args.append("Object")
        return ClassDeclarationNode(*args)


class CallNodeWrapper:
    def __new__(cls, *args):
        args = list(args)
        s = VariableNode(args[0], args[1], "self")
        return CallNode(args[0], args[1], s, *args[2:])


class StringWrapper:
    def __new__(cls, *args):
        line, col, lex = args
        lex = lex[1:-1]
        n_lex = ""
        string_backslash = False
        for t in lex:
            if not string_backslash:  # if the previosur chat is not '\'
                if t == "\\":
                    string_backslash = True  # backslash caracter
                else:
                    n_lex += t  # no backslash caracter situation
            else:
                string_backslash = False
                if t == "b":  # \b backspace
                    n_lex += "\b"
                elif t == "t":  # \t tab
                    n_lex += "\t"
                elif t == "n":
                    n_lex += "\n"
                elif t == "f":  # \f formfeed
                    n_lex += "\f"
                elif t == "\\":  # \\ backslash caracter
                    n_lex += "\\"
                    string_backslash = True
                else:
                    n_lex += t

        return StringNode(line, col, n_lex)
