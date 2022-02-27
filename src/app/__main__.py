from pathlib import Path

import jsonpickle
import typer

from app.shared.errors import InvalidInputFileError
from app.lexer.main import CoolLexer
from app.parser import CoolParser
from app.semantics.ast import ProgramNode
from app.semantics.type_builder import TypeBuilder
from app.semantics.type_collector import TypeCollector
from app.semantics.inference.soft_inferencer import ShallowInferrer
from app.semantics.inference.deep_inferrer import DeepInferrer
from app.cil.cool_to_cil import COOLToCILVisitor


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

    soft = ShallowInferrer(context)
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


if __name__ == "__main__":
    typer.run(app)
