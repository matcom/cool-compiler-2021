from compiler.cmp.grammar import G
from compiler.lexer.lex import CoolLexer
from compiler.parser.parser import LR1Parser, evaluate_reverse_parse
from compiler.visitors.cil2mips.cil2mips import CILToMIPSVisitor
from compiler.visitors.cil2mips.mips_printer import MIPSPrintVisitor
from compiler.visitors.cool2cil.cool2cil import COOLToCILVisitor
from compiler.visitors.semantics_check.type_builder import TypeBuilder
from compiler.visitors.semantics_check.type_checker import TypeChecker
from compiler.visitors.semantics_check.type_collector import TypeCollector
from compiler.visitors.semantics_check.type_inferencer import TypeInferencer
from sys import exit
import os


def main(args):
    try:
        with open(args.file, "r") as fd:
            code = fd.read()
    except:
        print(f"(0,0) - CompilerError: file {args.file} not found")
        exit(1)

    # Lexer
    lexer = CoolLexer()
    tokens, errors = lexer.tokenize(code)
    for error in errors:
        print(error)
    if errors:
        exit(1)

    # Parser
    parser = LR1Parser(G)
    parseResult, error = parser(tokens, get_shift_reduce=True)
    if error:
        print(error)
        exit(1)

    parse, operations = parseResult
    ast = evaluate_reverse_parse(parse, operations, tokens)

    # Collecting types
    collector = TypeCollector()
    collector.visit(ast)
    context = collector.context
    for (e, pos) in collector.errors:
        print(f"{pos} - {type(e).__name__}: {str(e)}")
    if collector.errors:
        exit(1)

    # Building types
    builder = TypeBuilder(context)
    builder.visit(ast)
    manager = builder.manager
    for (e, pos) in builder.errors:
        print(f"{pos} - {type(e).__name__}: {str(e)}")
    if builder.errors:
        exit(1)

    # Type checking
    checker = TypeChecker(context, manager)
    scope = checker.visit(ast)
    for (e, pos) in checker.errors:
        print(f"{pos} - {type(e).__name__}: {str(e)}")
    if checker.errors:
        exit(1)

    # Inferencing Autotype
    inferencer = TypeInferencer(context, manager)
    inferencer.visit(ast, scope)
    for e in inferencer.errors:
        print(f"{pos} - {type(e).__name__}: {str(e)}")
    if inferencer.errors:
        exit(1)

    # Last check without autotypes
    checker = TypeChecker(context, manager)
    checker.visit(ast)
    for (e, pos) in checker.errors:
        print(f"{pos} - {type(e).__name__}: {str(e)}")
    if checker.errors:
        exit(1)

    # COOL to CIL
    cil_visitor = COOLToCILVisitor(context)
    cil_ast = cil_visitor.visit(ast, scope)

    # CIL to MIPS
    cil_to_mips = CILToMIPSVisitor()
    mips_ast = cil_to_mips.visit(cil_ast)
    printer = MIPSPrintVisitor()
    mips_code = printer.visit(mips_ast)

    # Output MIPS file
    out_file = f"{args.file[:-3]}.mips"
    lib_path = os.path.abspath(
        os.path.join(__file__, "../compiler/visitors/cil2mips/mips_lib.asm")
    )
    with open(out_file, "w") as f:
        f.write(mips_code)
        with open(lib_path) as f2:
            f.write("".join(f2.readlines()))

    exit(0)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CoolCompiler")
    parser.add_argument(
        "-f", "--file", type=str, default="code.cl", help="File to read cool code from"
    )

    args = parser.parse_args()

    main(args)
