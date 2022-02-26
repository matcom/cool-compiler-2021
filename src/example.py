from coolcmp.codegen.cil2mips.mips_formatter import MIPSFormatter
from coolcmp.lexing_parsing.lexer import errors as lexer_errors
from coolcmp.lexing_parsing.parser import parser, errors as parser_errors
from coolcmp.semantics import check_semantics
from coolcmp.codegen.cool2cil import build_cil

from coolcmp.codegen.cil2mips import build_mips
from coolcmp.utils.ast_formatter import ASTFormatter
from coolcmp.utils.cil_formatter import CILFormatter

from test_cil2mips import hello_world, allocate, print_int


def main():
    cil_ast = print_int

    mips_ast = build_mips(cil_ast, None, None)

    mips_str = MIPSFormatter().visit(mips_ast)

    print("Mips code:")
    print(mips_str)

    with open("./code.mips", "w") as fd:
        fd.write(mips_str)


if __name__ == "__main__":
    main()
