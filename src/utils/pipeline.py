from os import error
from typing import Counter
import typer

from cool_grammar import parser
from cool_lexer import lexer
from utils.cyclic_dependency import CyclicDependency
from utils.formatter import Formatter, CodeBuilder
from utils.semantic import Context, Scope
from utils.inference import InferenceTypeChecker
from utils.instance import Execution
from utils.type_analysis import TypeBuilder, TypeChecker, TypeCollector
from utils.auxiliar_methods import erase_multiline_comment

app = typer.Typer()


def read_file(file_name: str):
    with open(file_name, 'r', encoding='utf-8') as f: 
        s = f.read()
    return s
    

def log_error(s: str):
    styled_e = typer.style(s, fg=typer.colors.RED, bold=True)
    typer.echo(styled_e)

def parse(program: str, debug: bool = False):
    return parser.parse(program, debug=debug)

def check_semantics(program: str, debug: bool = False):
    context = Context()
    scope = Scope()
    errors = []

    ast = parse(program, debug)
    if parser.errorok:
        errors = ['Syntactic Error']
    else:
        TypeCollector(context, errors).visit(ast)
        TypeBuilder(context, errors).visit(ast)
        CyclicDependency(context, errors)
        if not errors:
            TypeChecker(context, errors).visit(ast, scope)

    return ast, errors, context, scope

def get_tokenline(str, pos):
    temp_pos = -1
    line = 1
    while temp_pos < pos:
        temp_pos += 1
        if str[temp_pos] == '\n':
            line += 1
    return line

def get_eol_pos(str, line):
    pos = 0
    temp_line = 1
    
    temp_pos = 0

    while temp_line != line:
        if str[temp_pos] == '\n':
            temp_line += 1
        temp_pos += 1

    while str[temp_pos] != '\n':
        pos += 1
        temp_pos += 1

    return pos

def get_tokencolumn(str, pos):
    column = 1
    temp_pos = pos
    while str[temp_pos] != '\n':
        if temp_pos == 0: break
        temp_pos -= 1
        column += 1
    return column

def tokenize(program_file: str, debug: bool = False, verbose=False):
    program = read_file(program_file)

    errors, program = erase_multiline_comment(program)
    
    lexer.input(program)
    # print(program)
    while True:
        t = lexer.token()
        if not t:
            break
        if type(t) == tuple:
            column = 1
            current_pos = t[2]
            if t[3] == '\"': pass
            else:
                while program[current_pos] != '\n':
                    column += 1
                    current_pos -= 1
                errors.append(f'({t[1]}, {column - 1}) - LexicographicError: ERROR \"{t[3]}\"')
        elif t.type == 'STRING':
            if t.value.find('\0') != -1:
                pos = t.value.index('\0')
                lineno = get_tokenline(program, t.lexpos)
                column = get_tokencolumn(program, t.lexpos + pos - 1)
                errors.append(f'({lineno}, {column}) - LexicographicError: String contains null character')
        elif t.type == 'USTRING':
            lineno = get_tokenline(program, t.lexpos)
            column = get_tokencolumn(program, t.lexpos)
            if t.lexpos + 1 == len(program) or program[t.lexpos + 1] == '\n':
                errors.append(f'({lineno}, {column}) - LexicographicError: EOF in string constant')
            else:
                lineno = get_tokenline(program, t.lexpos + len(t.value) - 1)
                column = get_tokencolumn(program, t.lexpos + len(t.value) - 1)
                errors.append(f'({lineno}, {column}) - LexicographicError: Unterminated string constant')

            pass
        if verbose:
            print(t)

    return errors, program

def test_parse(program_file: str, debug: bool = False):
    program = read_file(program_file)
    ast = parse(program, debug)
    formater = Formatter()
    print(formater.visit(ast, 0))    

def test_context(program_file: str, debug: bool = False):
    program = read_file(program_file)

    context = Context()
    errors = []

    ast = parse(program, debug)
    TypeCollector(context, errors).visit(ast)
    TypeBuilder(context, errors).visit(ast)
    CyclicDependency(context, errors)
    if not errors:
        print(context)
    else:
        print('\n'.join(errors))


@app.command()
def test_inference(program_file: str, debug: bool = False):
    program = read_file(program_file)

    context = Context()
    errors = []

    ast = parse(program, debug)
    if ast is None:
        errors.append('Syntactic Errors')
    else:
        TypeCollector(context, errors).visit(ast)
        TypeBuilder(context, errors).visit(ast)
        CyclicDependency(context, errors)
        if not errors:
            InferenceTypeChecker(context, errors).visit(ast, Scope())
            print(CodeBuilder().visit(ast, 0))
        else:
            print('\n'.join(errors))

@app.command()
def test_execution(program_file: str, debug: bool = False):
    program = read_file(program_file)

    context = Context()
    errors = []

    ast = parse(program, debug)
    if ast is None:
        # error en el lexer o en el parser
        #
        errors.append('Syntactic Errors')
    else:
        TypeCollector(context, errors).visit(ast)
        TypeBuilder(context, errors).visit(ast)
        CyclicDependency(context, errors)
        if not errors:
            InferenceTypeChecker(context, errors).visit(ast, Scope())
            print(CodeBuilder().visit(ast, 0))
            Execution(context).visit(ast, Scope())
        else:
            print('\n'.join(errors))


def test_semantics(program_file: str, debug: bool = False):
    program = read_file(program_file)

    _, errors, _, _ = check_semantics(program, debug)
    if errors:
        print('\n'.join(errors))
    else:
        print('Check Succesful')

def print_list(list):
    for item in list:
        print(item)

@app.command()
def final_execution(program_file, program_file_out, debug: bool = False, verbose=False):
    context = Context()
    
    errors, program = tokenize(program_file, debug, verbose)

    if errors:
        for e in errors:
            log_error(e)
        exit(1)
    exit(0)
	
    # ast = parse(program, debug)

    # if ast is None:
    #     # errors.append('Syntactic Errors')
    #     print('Syntactic Errors')
    # else:
    #     TypeCollector(context, errors).visit(ast)
    #     TypeBuilder(context, errors).visit(ast)
    #     CyclicDependency(context, errors)
    #     if not errors:
    #         InferenceTypeChecker(context, errors).visit(ast, Scope())
    #         CodeBuilder().visit(ast, 0) # se puede ver el codigo transformado
    #         Execution(context).visit(ast, Scope())
            
    #     else:
    #         return '\n'.join(errors) 
    # return "\n".join(errors) 
    
if __name__ == '__main__':
    app()
    # test_execution("testing/inference/program10.cl")
    # test_execution("tests/lexer/comment1.cl")
    # tokenize("tests/lexer/comment1.cl")
    # tokenize("tests/lexer/string1.cl")
    # tokenize("tests/lexer/string4.cl")
    
    #final_execution('../../tests/parser/assignment2.cl','')
    
    # final_execution('tests/lexer/c.cl',0)