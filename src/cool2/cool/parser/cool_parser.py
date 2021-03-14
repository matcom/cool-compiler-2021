from cool.grammar.cool_grammar import G
from cool.parser.utils import load_parser, save_parser

cool_parser_path = 'cool2/cool/parser/cool_parser.obj'
# cool_parser = save_parser(cool_parser_path,G)
# print('Errors',cool_parser.errors)
cool_parser = load_parser(cool_parser_path,G)