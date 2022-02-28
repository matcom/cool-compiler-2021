"""
Main entry point of COOL compiler
"""
import os
import subprocess

from coolcmp.codegen.cil2mips.mips_formatter import MIPSFormatter
from coolcmp.lexing_parsing.lexer import errors as lexer_errors
from coolcmp.lexing_parsing.parser import parser, errors as parser_errors
from coolcmp.semantics import check_semantics
from coolcmp.codegen.cool2cil import build_cil

from coolcmp.codegen.cil2mips import build_mips
from coolcmp.utils.ast_formatter import ASTFormatter
from coolcmp.utils.cil_formatter import CILFormatter

from coolcmp.utils.cil import ProgramNode
from coolcmp.utils.registers import FP


def main(cool_code: str, run: bool, verbose: bool):
    ast = parser.parse(cool_code)

    if verbose:
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

    cil: ProgramNode
    cil = build_cil(ast, ctx, scope)

    if verbose:
        cil_str = CILFormatter().visit(cil)
        print(cil_str)

    mips = build_mips(cil, None, None)
    mips_str = MIPSFormatter().visit(mips)

    if verbose:
        print("Mips code:")
        print(mips_str)

    if run:
        executable_name = '__temp_code.mips'
        with open(executable_name, 'x', encoding='utf8') as f:
            f.write(mips_str)
        print('=' * 20, 'Running SPIM', '=' * 20)
        try:
            subprocess.run(['spim', '-f', executable_name])
        finally:
            os.remove(executable_name)


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        '-r', type=bool, default=False,
        help='If present the file compiled will be executed by SPIM.'
    )
    arg_parser.add_argument(
        '-v', type=bool, default=False,
        help='Verbose output.'
    )
    arg_parser.add_argument(
        'file', type=FileType(mode='r', encoding='utf8'),
        help='COOL source file.'
    )
    args = arg_parser.parse_args()

    cool_program = args.file.read()
    main(cool_program, args.r, args.v)
