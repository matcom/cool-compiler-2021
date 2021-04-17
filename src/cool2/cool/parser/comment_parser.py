from cool.grammar.comment_grammar import C
from cool.parser.utils import load_parser, save_parser

import os
base_dir = os.path.dirname(__file__)
comment_parser_path = os.path.join(base_dir, 'comment_parser.obj')
# comment_parser = save_parser(comment_parser_path,C)
# print('Errors',comment_parser.errors)
comment_parser = load_parser(comment_parser_path,C)