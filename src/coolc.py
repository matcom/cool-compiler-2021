"""
Main entry point of COOL compiler
"""
from coolcmp.lexing_parsing.lexer import errors as lexer_errors
from coolcmp.lexing_parsing.parser import parser, errors as parser_errors
from coolcmp.semantics import check_semantics
from coolcmp.formatter import FormatVisitor


def main(cool_code: str, verbose: bool = False):
    ast = parser.parse(cool_code)

    if verbose:
        formatter = FormatVisitor()
        print(formatter.visit(ast))

    if lexer_errors:
        for error in lexer_errors:
            print(error)
        exit(1)

    if parser_errors:
        for error in parser_errors:
            print(error)
        exit(1)

    sem_errors = check_semantics(ast)
    if sem_errors:
        for error in sem_errors:
            print(error)
        exit(1)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: python3 coolc.py program.cl [-v]')
        exit(1)
    elif not sys.argv[1].endswith('.cl'):
        print('COOl source code files must end with .cl extension.')
        print('Usage: python3 coolc.py program.cl')
        exit(1)

    cool_program = open(sys.argv[1], encoding='utf8').read()
    try:
        verbose = sys.argv[2] == '-v'
    except IndexError:
        verbose = False
    main(cool_program, verbose)
