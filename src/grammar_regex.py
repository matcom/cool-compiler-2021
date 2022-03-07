import os
from grammar_class import Grammar
import ast_regex as ast

regex_grammar = Grammar("regex")

#Terminals " | * + - ? ^ \ . ( ) [ ] char"
# ALT: A | B (are evaluated form left to right)
# STAR: A* (can appear 0, 1 or more times)  
# PLUS: A+ (must appear at least 1 time)
# MINUS: [a-b] In range context 
# ACC : ^[a-b] (start with a || b)
#     : [^\w] (any char that is not in the group)
# ASK : A? (can appear at 1 or 0 times)
# ESC : \  (gives significant to others symbols)  
# DOT : A.B (any char between A & B)
# LPAREN - RPAREN :() to mark precedencia
# LBRACE - RBRACE : [\A-B] (to group range & may included others special chars)
alt, star, plus, minus, acc, ask, esc, dot,\
lparen, rparen, lbrace, rbrace, char = regex_grammar.terminal((ast.TOKEN_TYPE.ALT, "|"),
                                                         (ast.TOKEN_TYPE.STAR, "*"),
                                                         (ast.TOKEN_TYPE.PLUS, "+"),
                                                         (ast.TOKEN_TYPE.MINUS, "-"),
                                                         (ast.TOKEN_TYPE.ACC, "^"),
                                                         (ast.TOKEN_TYPE.ASK, "?"),
                                                         (ast.TOKEN_TYPE.ESC, "\\"),
                                                         (ast.TOKEN_TYPE.DOT, "."),
                                                         (ast.TOKEN_TYPE.LPAREN, "("),
                                                         (ast.TOKEN_TYPE.RPAREN, ")"),
                                                         (ast.TOKEN_TYPE.LBRACE, "["),
                                                         (ast.TOKEN_TYPE.RBRACE, "]"),
                                                         (ast.TOKEN_TYPE.CHAR, ""))

# Non Terminals
Regex, ConcatenationRegex, ClosureRegex, ContentRegex ,GrouperRegex, SetterRegex, \
NoSetterRegex, AnyEnfRegex, SetRegex, ElemSetRegex, CharRegex, Reserved = \
    regex_grammar.nonTerminals(*"Regex,ConcatenationRegex,ClosureRegex,ContentRegex,"
            "GrouperRegex,SetterRegex,NoSetterRegex,AnyEfRegex,SetRegex,ElemSetRegex,CharRegex,"
            "Reserved".split(","))

regex_grammar.start_symbol = Regex

Reserved != alt | star | plus | minus | ask | acc | esc | dot | lparen | rparen | lbrace | rbrace

# (s)|(r)
Regex != Regex + alt + ConcatenationRegex / (ast.UnionNode, (0, 2)) \
| ConcatenationRegex

# (s)(r) 
ConcatenationRegex != ConcatenationRegex + ClosureRegex / (ast.ConcatenationNode, (0, 1)) \
| ClosureRegex

# (s)∗  (s)+  (s)? () 
ClosureRegex != ContentRegex + star / (ast.ClousureStarNode, (0,)) \
| ContentRegex + plus / (ast.ClousurePlusNode, (0,)) \
| ContentRegex + ask / (ast.ClousureMayNode, (0,)) \
| ContentRegex

# () []  [^]  .[] s
ContentRegex != GrouperRegex | SetterRegex | NoSetterRegex | AnyEnfRegex | CharRegex

#(s)
GrouperRegex != lparen + Regex + rparen / (ast.GrouperNode, (1,)) \

#[]: Caracters classes
SetterRegex != lbrace + SetRegex + rbrace / (ast.SetterNode, (1,))
NoSetterRegex != lbrace + acc + SetRegex + rbrace / (ast.NoSetterNode, (2,))

SetRegex != SetRegex + ElemSetRegex / (ast.ElemSetComNode, (0, 1)) \
| ElemSetRegex / (ast.ElemSetComNode, (0, 0))

ElemSetRegex != char + minus + char / (ast.RangeNode, (0, 2)) \
| AnyEnfRegex \
| char

AnyEnfRegex != esc + char / (ast.AnyEscaperNode, (0,1)) \
| esc + Reserved / (ast.AnyEscaperNode, (0,1)) \
| dot / (ast.AnyEscaperNode, (0,0))

CharRegex != char / (ast.CharNode, (0,))

current_path = os.path.dirname(__file__)
regex_grammar.parser(current_path)
regex_grammar.lexer(current_path)

# This grammas Must Have:
# states: 104
# action shift 127
# action reduce 652
# actions 779 (780?)
# goto 94