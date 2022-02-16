from lexical_analizer import tokenize_cool_text
from cool_grammar import define_cool_grammar
from cool_visitor import FormatVisitorST

from type_collector import TypeCollector
from type_builder import TypeBuilder
from type_checker import TypeChecker

from shift_reduce_parsers import LR1Parser, DerivationTree
from errors import parsing_table_error, Error

from cmp.evaluation import evaluate_reverse_parse
from pathlib import Path
from errors import InvalidInputFileError
import typer


def report_and_exit(errors):
    if len(errors) == 0:
        raise typer.Exit(code=0)

    for error in errors:
        typer.echo(error)
    raise typer.Exit(code=1)


def pipeline(input_file: Path, output_file: Path = None):
    errors = []

    if not input_file.is_file:
        errors.append(InvalidInputFileError(str(input_file)))

    if len(errors) > 0:
        report_and_exit(errors)

    text = input_file.read_text()

    # main_error1 = ["A class Main with a method main most be provided"]
    # main_error2 = ['"main" method in class Main does not receive any parameters']

    # define grammar
    grammar, idx, string, num = define_cool_grammar()

    tokens = tokenize_cool_text(grammar, idx, string, num, text)
    parser = LR1Parser(grammar)
    parse, operations = parser([t.token_type for t in tokens])

    ast = evaluate_reverse_parse(parse, operations, tokens)
    # formatter = FormatVisitorST()
    # tree = formatter.visit(ast)

    visitors = [TypeCollector(errors), TypeBuilder(errors), TypeChecker(errors)]
    for visitor in visitors:
        ast = visitor.visit(ast)

    if len(errors) > 0:
        report_and_exit(errors)

    if output is None:
        output = input.with_suffix(".mips")


if __name__ == "__main__":
    typer.run(pipeline)
