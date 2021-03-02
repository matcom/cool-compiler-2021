import os
import sys
from pathlib import Path
from typing import List

import typer

sys.path.append(os.getcwd())

from cool.grammar import serialize_parser_and_lexer
from cool.lexertab import CoolLexer
from cool.parsertab import CoolParser
from cool.semantics import TypeCollector, TypeBuilder, OverriddenMethodChecker, TypeChecker, topological_sorting
from cool.semantics.execution import Executor, ExecutionError
from cool.semantics.formatter import CodeBuilder
from cool.semantics.type_inference import InferenceChecker
from cool.semantics.utils.scope import Context, Scope

app = typer.Typer()


def check_semantics(ast, scope: Scope, context: Context, errors: List[str]):
    TypeCollector(context, errors).visit(ast)
    TypeBuilder(context, errors).visit(ast)
    declarations = ast.declarations
    topological_sorting(ast, context, errors)
    ast.declarations = declarations
    if not errors:
        OverriddenMethodChecker(context, errors).visit(ast)
        InferenceChecker(context, errors).visit(ast, scope)
        TypeChecker(context, errors).visit(ast, scope)
    return ast, scope, context, errors


def tokenize(file: typer.FileText, verbose: bool = False):
    path = Path.cwd() / file.name
    if not path.exists():
        typer.echo(f'File {file.name} does not exist.')
        return None, None

    s = path.open('r').read()
    lexer = CoolLexer()
    tokens = lexer(s)

    if lexer.contain_errors:
        for e in lexer.errors:
            typer.echo(e, err=True)

    if verbose:
        for t in tokens:
            typer.echo(t)

    return tokens, lexer


def parse(file: typer.FileText, verbose: bool = False):
    tokens, lexer = tokenize(file, verbose)

    if lexer is None or lexer.contain_errors:
        return None, None

    parser = CoolParser(verbose)
    ast = parser(tokens)

    if parser.contains_errors:
        for e in parser.errors:
            typer.echo(e, err=True)

    return ast, parser


@app.command()
def infer(
        file: typer.FileText = typer.Argument(..., help='Cool file'),
        verbose: bool = typer.Argument(False, help='Execute in verbose mode.')
):
    ast, _ = parse(file, verbose)

    if ast is not None:
        ast, _, _, errors = check_semantics(ast, Scope(), Context(), [])
        if errors:
            for e in errors:
                typer.echo(e, err=True)
        typer.echo(CodeBuilder().visit(ast, 0))


@app.command()
def run(
        file: typer.FileText = typer.Argument(..., help='Cool file'),
        verbose: bool = typer.Argument(False, help='Execute in verbose mode.')
):
    ast, parser = parse(file, verbose)

    if ast is not None:
        ast, _, context, errors = check_semantics(ast, Scope(), Context(), [])

        if not errors and not parser.contains_errors:
            try:
                Executor(context).visit(ast, Scope())
                typer.echo('Program finished...')
            except ExecutionError as e:
                typer.echo(e.text, err=True)

        for error in errors:
            typer.echo(error, err=True)
        exit(0)
    else:
        exit(1)


@app.command()
def serialize():
    serialize_parser_and_lexer()

    cwd = os.getcwd()

    lexertab = os.path.join(cwd, 'lexertab.py')
    parsertab = os.path.join(cwd, 'parsertab.py')

    cool_lexertab = Path(os.path.join(cwd, 'cool', 'lexertab.py'))
    cool_parsertab = Path(os.path.join(cwd, 'cool', 'parsertab.py'))

    mode = 'w' if cool_lexertab.exists() else 'x'
    fr = open(lexertab, 'r')
    with cool_lexertab.open(mode) as fw:
        fw.write(fr.read().replace('from grammar', 'from cool.grammar'))
        fr.close()

    mode = 'w' if cool_parsertab.exists() else 'x'
    fr = open(parsertab, 'r')
    with cool_parsertab.open(mode) as fw:
        fw.write(fr.read().replace('from grammar', 'from cool.grammar'))
        fr.close()

    os.remove(lexertab)
    os.remove(parsertab)


if __name__ == '__main__':
    app()
