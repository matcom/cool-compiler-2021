"""
Main entry point of COOL compiler
"""
from coolcmp.lexer import Lexer


def main(cool_program):
    lexer = Lexer(build_lexer=True)
    lexer.input(cool_program)

    [(t.value, t.type) for t in lexer]  # make lexer process the input
    errors = lexer.errors

    if errors:
        for e in errors:
            print(e)

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
