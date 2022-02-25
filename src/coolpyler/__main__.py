from pathlib import Path

import typer

from coolpyler.errors import InvalidInputFileError
from coolpyler.lexer import CoolLexer
from coolpyler.parser import CoolParser
from coolpyler.visitors.cil.debug import CILDebug
from coolpyler.visitors.visitor import Visitor


def report_and_exit(errors):
    if len(errors) == 0:
        raise typer.Exit(code=0)

    for error in errors:
        typer.echo(error)
    raise typer.Exit(code=1)


def coolpyler(input: Path, output: Path = None, debug: bool = False):
    errors = []

    if not input.is_file:
        errors.append(InvalidInputFileError(str(input)))

    if len(errors) > 0:
        report_and_exit(errors)

    code = input.read_text()

    lexer = CoolLexer(errors)
    tokens = lexer.tokenize(code)

    parser = CoolParser(errors)
    ast = parser.parse(tokens)  # noqa: F841

    visitor = Visitor(errors)

    ast = visitor.visit_up(ast)

    if len(errors) > 0:
        report_and_exit(errors)

    cil = visitor.visit_middle(ast)

    if output is None:
        cil_file = input.with_suffix(".cil")

    with cil_file.open("w") as file:
        CILDebug(file).visit(cil)

    mips = visitor.visit_down(cil)

    if output is None:
        mips_file = input.with_suffix(".mips")

    with mips_file.open("w") as file:
        print(mips, file=file)


if __name__ == "__main__":
    typer.run(coolpyler)
