from cool.lexer.cool_lexer import Lexer, save_lexer, load_lexer, lower_case,upper_case,numbers
from cool.grammar.comment_grammar import delimiter_close,delimiter_open,plain_text,C

text = f'[{lower_case}{upper_case}_{numbers}\n\r\b\f\t\v"~`\'!,:;<@=> \\[\\]\\*/-\\+.\\?\\(\\)\\\\#$%^&\\|'+'{}'+']*'
tex = text.replace('\\(\\)','').replace('\\*','')

tex3 = f'[(\\*+(\\()*)(\\(+(\\))*)\\)+]' # ( \\(\\* | \\*\\) )^C
tex3 = tex + f'|{tex3}'
tex1 = '\\(\\*'
tex2 = '\\*\\)'

comment_tokens_def = [
    (plain_text, tex3),
    (delimiter_open, tex1),
    (delimiter_close, tex2),
    ]

# comment_lexer = Lexer(comment_tokens_def,C.EOF)

comment_lexer_path = 'cool2/cool/lexer/comment_lexer.obj'
# comment_lexer = save_lexer(comment_tokens_def,comment_lexer_path,C)
comment_lexer = load_lexer(comment_lexer_path)