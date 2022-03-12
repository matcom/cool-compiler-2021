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


def main(filename: str, cool_code: str, run: bool, verbose: bool):
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

    cil: ProgramNode
    cil = build_cil(ast, ctx, scope)

    if verbose:
        cil_str = CILFormatter().visit(cil)
        print(cil_str)

    mips = build_mips(cil, None, None)
    mips_str = MIPSFormatter().visit(mips)

    mips_file = filename + '.mips'

    with open(mips_file, 'w') as fd:
        fd.write(mips_str)

    if run:
        print('=' * 20, 'Running SPIM', '=' * 20)
        subprocess.run(['spim', '-f', mips_file])


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType, BooleanOptionalAction

    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        '--out', required=False,
        help='Name for .mips generated file after compilation.'
    )
    arg_parser.add_argument(
        '--run', default=False, action=BooleanOptionalAction,
        help='Execute the file compiled with SPIM.'
    )
    arg_parser.add_argument(
        '--verbose', default=False, action=BooleanOptionalAction,
        help='Verbose output.'
    )
    arg_parser.add_argument(
        'file', type=FileType(mode='r', encoding='utf8'),
        help='COOL source file.'
    )
    args = arg_parser.parse_args()

    full_name = args.file.name
    filename = full_name[:full_name.rfind('.')]
    cool_code = args.file.read()
    main(
        filename=args.out or filename,
        cool_code=cool_code,
        run=args.run,
        verbose=args.verbose
    )
