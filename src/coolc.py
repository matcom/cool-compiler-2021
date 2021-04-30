"""
Main entry point of COOL compiler
"""
from coolcmp.lexing_parsing.lexer import errors as lexer_errors
from coolcmp.lexing_parsing.parser import parser, errors as parser_errors


def main(cool_program):
    parser.parse(cool_program)

    if lexer_errors:
        for er in lexer_errors:
            print(er)

        exit(1)

    if parser_errors:
        for er in parser_errors:
            print(er)

        exit(1)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print('Usage: python3 coolc.py program.cl')
        exit(1)
    elif not sys.argv[1].endswith('.cl'):
        print('COOl source code files must end with .cl extension.')
        print('Usage: python3 coolc.py program.cl')
        exit(1)

    cool_program = open(sys.argv[1], encoding='utf8').read()

    main(cool_program)
