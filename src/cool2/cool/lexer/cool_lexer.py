from cool.grammar.cool_grammar import *
from cool.lexer.utils import *

# Keyword are case in sensitive except for true and false that the first letter must be lower case
keywords = [
        (ifx, '[iI][fF]'), (if_r, '[fF][iI]'), (then, '[tT][hH][eE][nN]'),
        (elsex, '[eE][lL][sS][eE]'), (isvoid, '[iI][sS][vV][oO][iI][dD]'), 
        (new, '[nN][eE][wW]'), (whilex, '[wW][hH][iI][lL][eE]'), 
        (loop, '[lL][oO][oO][pP]'), (loop_r, '[pP][oO][oO][lL]'), 
        (classx, '[cC][lL][aA][sS][sS]'), (let, '[lL][eE][tT]'), 
        (inx, '[iI][nN]'), (case, '[cC][aA][sS][eE]'), (of, '[oO][fF]'), 
        (case_r, '[eE][sS][aA][cC]'), (inherits, '[iI][nN][hH][eE][rR][iI][tT][sS]'), 
        (true, 't[rR][uU][eE]'), (false, 'f[aA][lL][sS][eE]')
        ]

operators = [
        (dot, '.'),(plus, '\\+'),(minus, '-'),(div, '/'),
        (star, '\\*'),(notx, 'not'),(roof, '~'),(less, '<'),
        (less_eq, '<='),(greater, '>'),(greater_eq, '>='),
        (equal, '='),(assign, '<-'),(arrow, '=>'),(at, '@'),
        ]

signs = [
    (opar, '\\('),(cpar, '\\)'),(ocur, '{'),(ccur ,'}'),
    (colon, ':'),(semi, ';'),(comma,','),
    ]

lower_case = 'qwertyuiopasdfghjklzxcvbnm'
upper_case = 'QWERTYUIOPASDFGHJKLZXCVBNM'
numbers = '1234567890'
text = f'[{lower_case}{upper_case}_{numbers}~`\'!,:;<@=> \\[\\]\\*/-\\+.\\?\\(\\)\\\\#$%^&\\|'+'{}'+']*'

ignore = [('space',f'[ \n\r\b\f\t\v]+|(--({text}|")*\n)')]

other = [
    (idx, f'[{lower_case}][{lower_case}{upper_case}_{numbers}]*'),
    (typex, f'[{upper_case}][{lower_case}{upper_case}_{numbers}]*'),
    (num, f'[123456789][{numbers}]*(.[{numbers}]+)?|0'),
    (string, f'"{text}"')
    ]
cool_tokens_def = keywords+operators+signs+other+ignore
# cool_lexer = Lexer(cool_token_def,G.EOF)

cool_lexer_path = 'cool2/cool/lexer/cool_lexer.obj'
# cool_lexer = save_lexer(cool_tokens_def,cool_lexer_path,G)
cool_lexer = load_lexer(cool_lexer_path)