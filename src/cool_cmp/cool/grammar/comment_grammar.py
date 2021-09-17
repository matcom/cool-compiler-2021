from cmp.pycompiler import Grammar, NonTerminal, Terminal
from cool.ast.ast import *

C = Grammar()

# non-terminals
text = C.NonTerminal('<text>', startSymbol=True)
chunk = C.NonTerminal('<chunk>')

# Terminals
delimiter_open,delimiter_close, plain_text = C.Terminals('(* *) text')

# productions
text %= chunk + delimiter_open + text + delimiter_close + text, lambda h,s: s[1] + s[5]
text %= chunk, lambda h,s: s[1]
chunk %= plain_text + chunk, lambda h,s: s[1][0] + s[2]
chunk %= C.Epsilon, lambda h,s: ''

