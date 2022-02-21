from pathlib import Path

import typer

from coolpyler.errors import InvalidInputFileError
from coolpyler.lexer import CoolLexer
from coolpyler.parser import CoolParser
from coolpyler.visitors.visitor import Visitor


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
    ast = parser.parse(tokens)  # noqa: F841

    visitor = Visitor(errors)
    ast = visitor.visit(ast)

    if len(errors) > 0:
        report_and_exit(errors)

    if output is None:
        output = input.with_suffix(".mips")


if __name__ == "__main__":
    typer.run(coolpyler)
