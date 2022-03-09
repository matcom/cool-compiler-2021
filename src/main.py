from lexical_analizer import tokenize_cool_text
from cool_grammar import define_cool_grammar
from cool_visitor import FormatVisitorST
from visitor_type_ast import FormatVisitorTypedAst

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
from code_gen.mips_builder import MIPSBuilder
from code_gen.mips_writer import MIPSWriter
from cmp.cil import PrintVisitor
import typer


def report_and_exit(errors):
    if len(errors) == 0:
        raise typer.Exit(code=0)

    # typer.echo(errors[0])
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

    parse, operations = parser(tokens)

    if len(errors) > 0:
        report_and_exit(errors)

    # get parsing tree
    ast = evaluate_reverse_parse(parse, operations, tokens)

    # print("-------------------------------Initial AST-------------------------------")
    # formatter = FormatVisitorST()
    # tree = formatter.visit(ast)
    # print(tree)

    visitors = [TypeCollector(errors), TypeBuilder(errors)]
    for visitor in visitors:
        ast = visitor.visit(ast)

    type_checker = TypeChecker(errors)
    scope, typed_ast = type_checker.visit(ast)

    # formatter = FormatVisitorTypedAst()
    # print("-------------------------------Typed AST-------------------------------")
    # tree = formatter.visit(typed_ast)
    # print(tree)

    if len(errors) > 0:
        report_and_exit(errors)

    cool_to_cil_visitor = CILBuilder()
    cil_ast = cool_to_cil_visitor.visit(typed_ast)

    formatter = PrintVisitor()
    tree = formatter.visit(cil_ast)
    print(tree)

    cil_to_mips_visitor = MIPSBuilder()
    mips_ast = cil_to_mips_visitor.visit(cil_ast)

    mips_writer = MIPSWriter()
    output = mips_writer.visit(mips_ast)

    output = '\n'.join(mips_writer.output)

    if output_file is None:
        output_file = input_file.with_suffix(".mips")

    with output_file.open("w") as file:
        print(output, file=file)
        
    #with open(f'{input_file[:-3]}.mips','w') as f:
    #    f.write(f'{output}')
    #output_file.write_text(output)


if __name__ == "__main__":
    #input_file = Path("/home/sandra/Desktop/FinalProjects/Compiler/cool-compiler-2021/customized_tests/code_gen/test_goto_if.cl")
    #output_file =  Path("/home/sandra/Desktop/FinalProjects/Compiler/cool-compiler-2021/customized_tests/test_hello_world.mips")

    #pipeline()
    typer.run(pipeline)
