from pathlib import Path

import jsonpickle
import typer

from coolpyler.errors import InvalidInputFileError
from coolpyler.lexer.main import CoolLexer
from coolpyler.parser.main import CoolParser
from coolpyler.semantics.inference.inferencer_ast import ProgramNode
from coolpyler.semantics.type_builder import TypeBuilder
from coolpyler.semantics.type_collector import TypeCollector
from coolpyler.semantics.inference.soft_inferencer import SoftInferencer
from coolpyler.semantics.inference.hard_inferencer import HardInferencer
from coolpyler.cil.cool_to_cil import COOLToCILVisitor
from coolpyler.mips.cil_to_mips import CILToMIPSVisitor
from coolpyler.mips.ast_printer import PrintVisitor


def report_and_exit(errors):
    if len(errors) == 0:
        raise typer.Exit(code=0)

    for error in errors:
        typer.echo(error)
    raise typer.Exit(code=1)


def coolpyler(input: Path, output: Path = None):
    errors = []

    if not input.is_file:
        errors.append(InvalidInputFileError(str(input)))

    if len(errors) > 0:
        report_and_exit(errors)

    code = input.read_text()

    lexer = CoolLexer(errors)
    tokens = lexer.tokenize(code)

    parser = CoolParser(errors)
    ast = parser.parse(tokens)

    if(len(errors) > 0):
        report_and_exit(errors)

    collector = TypeCollector()
    collector.visit(ast)
    context = collector.context
    errors += collector.errors

    builder = TypeBuilder(context)
    builder.visit(ast)
    errors += builder.errors

    soft = SoftInferencer(context)
    soft_ast: ProgramNode = soft.visit(ast)
    errors += soft.errors

    hard = HardInferencer(context)
    hard_ast: ProgramNode = hard.visit(soft_ast)
    errors += hard.errors

    # astfile = open('ast.json', 'w')
    # frozen = jsonpickle.encode(soft_ast)
    # astfile.write(str(frozen))

    if(len(errors) > 0):
        report_and_exit(errors)

    cool_to_cil = COOLToCILVisitor(context)
    cil_ast = cool_to_cil.visit(hard_ast)

    astfile = open('ast.json', 'w')
    frozen = jsonpickle.encode(cil_ast)
    astfile.write(str(frozen))

    cil_to_mips = CILToMIPSVisitor()
    mips_ast = cil_to_mips.visit(cil_ast)
    printer = PrintVisitor()
    mips_code = printer.visit(mips_ast)

    out_file = str(input).split(".")
    out_file[-1] = "mips"
    out_file = ".".join(out_file)

    with open(out_file, 'w') as f:
        f.write(mips_code)
        with open("coolpyler/mips/mips_lib.asm") as f2:
            f.write("".join(f2.readlines()))

    exit(0)

   # print('hard errors:', hard.errors)

   # visitor = Visitor(errors)
   # ast = visitor.visit(ast)

    if len(errors) > 0:
        report_and_exit(errors)

    if output is None:
        output = input.with_suffix(".mips")


if __name__ == "__main__":
    typer.run(coolpyler)
