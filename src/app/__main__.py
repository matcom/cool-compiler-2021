from pathlib import Path

import jsonpickle
import typer

from app.shared.errors import InvalidInputFileError
from app.lexer.main import CoolLexer
from app.parser import CoolParser
from app.semantics.ast import ProgramNode
from app.semantics.type_builder import TypeBuilder
from app.semantics.type_collector import TypeCollector
from app.semantics.inference.soft_inferencer import SoftInferencer
from app.semantics.inference.hard_inferencer import DeepInferrer
from app.cil.cool_to_cil import COOLToCILVisitor
from app.mips.cil_to_mips import CILToMIPSVisitor
from app.mips.ast_printer import PrintVisitor


def notify_failures(errors):
    if len(errors) == 0:
        raise typer.Exit(code=0)

    for error in errors:
        typer.echo(error)
    raise typer.Exit(code=1)


def app(input: Path, output: Path = None):
    errors = []

    if not input.is_file:
        errors.append(InvalidInputFileError(str(input)))

    if len(errors) > 0:
        notify_failures(errors)

    code = input.read_text()

    lexer = CoolLexer(errors)
    tokens = lexer.tokenize(code)

    parser = CoolParser(errors)
    ast = parser.parse(tokens)

    if(len(errors) > 0):
        notify_failures(errors)

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

    hard = DeepInferrer(context)
    hard_ast: ProgramNode = hard.visit(soft_ast)
    errors += hard.errors

    # astfile = open('ast.json', 'w')
    # frozen = jsonpickle.encode(hard_ast, max_iter=-1, max_depth=-1)
    # astfile.write(str(frozen))

    if(len(errors) > 0):
        notify_failures(errors)

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
        with open("app/mips/mips_lib.asm") as f2:
            f.write("".join(f2.readlines()))

    typer.Exit(code=0)


if __name__ == "__main__":
    typer.run(app)
