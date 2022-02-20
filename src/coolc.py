"""
Main entry point of COOL compiler
"""
from coolcmp.lexing_parsing.lexer import errors as lexer_errors
from coolcmp.lexing_parsing.parser import parser, errors as parser_errors
from coolcmp.semantics import check_semantics
from coolcmp.codegen.cool2cil import build_cil
from coolcmp.utils.ast_formatter import ASTFormatter
from coolcmp.utils.cil_formatter import CILFormatter


def main(cool_code: str, verbose: int):
    ast = parser.parse(cool_code)

    if verbose > 0:
        ast_str = ASTFormatter().visit(ast)
        print(ast_str)

    if lexer_errors:
        for error in lexer_errors:
            print(error)
        exit(1)

    if parser_errors:
        for error in parser_errors:
            print(error)
        exit(1)

    sem_errors, ctx, scope = check_semantics(ast)
    if sem_errors:
        for error in sem_errors:
            print(error)
        exit(1)

    # print('-' * 40)
    # print(ctx)
    # print('-' * 40)
    # print(scope)
    # print('-' * 40)

    cil = build_cil(ast, ctx, scope)

    if verbose > 1:
        cil_str = CILFormatter().visit(cil)
        print(cil_str)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: python3 coolc.py program.cl [-v+]')
        exit(1)
    elif not sys.argv[1].endswith('.cl'):
        print('COOl source code files must end with .cl extension.')
        print('Usage: python3 coolc.py program.cl')
        exit(1)

    cool_program = open(sys.argv[1], encoding='utf8').read()
    try:
        verb_count = sys.argv[2].count('v')
    except IndexError:
        verb_count = 0
    main(cool_program, verb_count)
