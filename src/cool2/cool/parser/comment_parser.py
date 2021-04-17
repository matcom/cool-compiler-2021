from cool.grammar.comment_grammar import C
from cool.parser.utils import load_parser, save_parser

comment_parser_path = 'src/cool2/cool/parser/comment_parser.obj'
# comment_parser = save_parser(comment_parser_path,C)
# print('Errors',comment_parser.errors)
comment_parser = load_parser(comment_parser_path,C)