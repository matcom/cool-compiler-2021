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
from cool_visitor import FormatVisitor
from code_gen.cil_builder import CILBuilder
from cmp.cil import PrintVisitor
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
    grammar, idx, type_id, string, num = define_cool_grammar()

    tokens = tokenize_cool_text(grammar, idx, type_id, string, num, text, errors)

    if len(errors) > 0:
        report_and_exit(errors)
    parser = LR1Parser(grammar, errors)

    if len(errors) > 0:
        report_and_exit(errors)

    parse, operations = parser(tokens, text)

    # print("Parse")
    # print(parse)

    if len(errors) > 0:
        report_and_exit(errors)
        
    #get parsing tree
    ast = evaluate_reverse_parse(parse, operations, tokens)

    #printing tree
    # formatter = FormatVisitorST()
    # tree = formatter.visit(ast)
    # print(tree)

    visitors = [TypeCollector(errors), TypeBuilder(errors)]
    for visitor in visitors:
        ast = visitor.visit(ast)

    type_checker = TypeChecker(errors)
    scope = type_checker.visit(ast)

    # formatter = FormatVisitor()
    # tree = formatter.visit(ast)
    # print(tree)

    if len(errors) > 0:
        report_and_exit(errors)

    # cool_to_cil_visitor = CILBuilder(errors)
    # cil_ast = cool_to_cil_visitor.visit(ast)

    # formatter = PrintVisitor()
    # tree = formatter.visit(cil_ast)
    # print(tree)

    # if output_file is None:
    #     output_file = input.with_suffix(".mips")


if __name__ == "__main__":
    typer.run(pipeline)
