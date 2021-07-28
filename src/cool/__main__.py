import os
import sys
from pathlib import Path
from typing import List

import typer

sys.path.append(os.getcwd())

from cool.grammar import Token, serialize_parser_and_lexer
from cool.lexertab import CoolLexer
from cool.parsertab import CoolParser
from cool.semantics import (OverriddenMethodChecker, PositionAssigner,
                            TypeBuilderForFeatures, TypeBuilderForInheritance, TypeChecker, TypeCollector,
                            topological_sorting)
from cool.semantics.utils.scope import Context, Scope

app = typer.Typer()


def log_success(s: str):
    styled_e = typer.style(s, fg=typer.colors.GREEN, bold=True)
    typer.echo(styled_e)


def log_error(s: str):
    styled_e = typer.style(s, fg=typer.colors.RED, bold=True)
    typer.echo(styled_e)


def format_tokens(tokens: List[Token]) -> str:
    s = ''
    last_line = 1
    for t in tokens:
        if t.line != last_line:
            last_line = t.line
            s += '\n' + ' ' * t.column
        else:
            s += ' '
        s += t.token_type.name
    return s


def tokenize(program: str, verbose: bool = False):
    lexer = CoolLexer()
    tokens = lexer(program)

    if lexer.contain_errors:
        for e in lexer.errors:
            log_error(e)

    if verbose:
        log_success('Tokens:')
        log_success('-' * 80)
        log_success(format_tokens(tokens) + '\n')
        log_success('-' * 80)
        print()
    
    return tokens, lexer


def parse(tokens: List[Token], verbose: bool = False):
    parser = CoolParser(verbose)
    ast = parser(tokens)

    if parser.contains_errors:
        for e in parser.errors:
            log_error(e)

    return ast, parser


def check_semantics(ast, scope: Scope, context: Context, errors: List[str]):
    TypeCollector(context, errors).visit(ast)
    TypeBuilderForInheritance(context, errors).visit(ast)
    topological_sorting(ast, context, errors)
    if not errors:
        TypeBuilderForFeatures(context, errors).visit(ast)
        OverriddenMethodChecker(context, errors).visit(ast)
        TypeChecker(context, errors).visit(ast, scope)
    return ast, scope, context, errors

@app.command()
def compile(
        input_file: typer.FileText = typer.Argument(..., help='Cool file'),
        output_file: typer.FileTextWrite = typer.Argument('a.mips', help='Mips file'),
        verbose: bool = typer.Option(False, help='Run in verbose mode.')
):
    # In case of encoding conflict
    if input_file.encoding.lower != 'utf-8':
        input_file = open(input_file.name, encoding='utf-8')
    
    program = input_file.read()
    tokens, lexer = tokenize(program, verbose)

    if lexer is None or lexer.contain_errors:
        exit(1)

    if not tokens[:-1]:  # there is always at least the EOF token
        log_error('(0, 0) - SyntacticError: ERROR at or near EOF')
        exit(1)
    
    ast, parser = parse(tokens, verbose)

    # parsing process failed
    if ast is None:
        exit(1)

    PositionAssigner(tokens).visit(ast)
    ast, _, _, errors = check_semantics(ast, Scope(), Context(), [])

    if errors or parser.contains_errors:
        for e in errors:
            log_error(e)
        exit(1)
    
    exit(0)

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
