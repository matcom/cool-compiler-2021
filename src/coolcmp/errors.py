"""
Compilation errors.
"""

LEX_ERROR = '(%s,%s) - LexicographicError: Unexpected symbol "%s".'
UNT_STR = '(%s,%s) - LexicographicError: Unterminated string.'
EOF_STR = '(%s,%s) - LexicographicError: EOF in string.'
NULL_STR = '(%s,%s) - LexicographicError: String contains null character'
EOF_COMM = '(%s,%s) - LexicographicError: EOF in comment.'

SYN_ERROR = '(%s,%s) - SyntacticError: Syntax error at or near "%s"'
SYN_EOF = '(0, 0) - SyntacticError: ERROR at or near EOF'   # empty program
