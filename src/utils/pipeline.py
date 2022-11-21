from cmath import log
from os import error
from typing import Counter
import typer

from cool_grammar import parser, errors as parser_errors
from cool_lexer import lexer, lexer_errors
from utils.ast_nodes import Token
# from utils.cyclic_dependency import CyclicDependency_, MethodChecker, cyclicDependency
from utils.formatter import Formatter, CodeBuilder, PrintingScope
from utils.semantic import Context, Scope
from utils.inference import InferenceTypeChecker
from utils.instance import Execution
from utils.type_analysis import PositionAssigner #, TypeBuilder, TypeChecker, TypeCollector, , TypeBuilderFeature
from utils.auxiliar_methods import erase_multiline_comment
# from utils.cool_to_cil import COOLToCILVisitor
# from utils.collect_dec import CollectDeclarationsDict, get_declarations_dict
from utils.code_generation import COOLwithNULL, COOLwithNULL_Type
# from utils.cil_to_mips import CILToMIPSVisitor, MipsFormatter
# from utils.cooltocil import ExtendedCoolTranslator, ExtendedCoolTypeChecker, CoolToCilTranslator
from utils.cool_cil_mips import CoolToCilTranslator, CilToMipsTranslator, MipsFormatter1, ExtendedCoolTranslator, ExtendedCoolTypeChecker
from utils.semantic_type_checker import  TypeCollector, TypeBuilderForInheritance, topological_sorting, TypeBuilderForFeatures, OverriddenMethodChecker, InferenceChecker, TypeChecker


app = typer.Typer()


def read_file(file_name: str):
    with open(file_name, 'r', encoding='utf-8') as f: 
        s = f.read()
    return s
    
def write_file(file_name: str, text: str):
    with open(file_name, 'w', encoding='utf-8') as f: 
        s = f.write(text)
        f.close()
    return s
        

def print_errors(s: str):
    styled_e = typer.style(s, fg=typer.colors.RED, bold=True)
    typer.echo(styled_e)

def parse(program: str, lexer=None, debug: bool = False):
    return parser.parse(program, lexer=lexer, debug=debug)

def check_semantics(program: str, debug: bool = False):
    context = Context()
    scope = Scope()
    errors = []

    ast = parse(program, debug)
    if parser.errorok:
        errors = ['Syntactic Error']
    else:
        TypeCollector(context, errors).visit(ast)
        # TypeBuilder(context, errors).visit(ast)
        # CyclicDependency(context, errors)
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
    program = erase_single_line_comment(program)
    
    lexer.input(program)
    tokens = []
    # print(program)
    while True:
        t = lexer.token()
        if not t:
            break
        # tokens.append(Token(t[0], t[1], t[2], t[3]))
        tokens.append(Token(t.type, t.value, t.lineno, t.lexpos, program))
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
        # if verbose:
        #     print(t)

    return errors, program, tokens

def erase_single_line_comment(program: str):
    temp = ''
    pos = 0
    while pos < len(program):
        if program[pos] == '-' and (pos + 1) < len(program):
            if program[pos + 1] == '-' and \
                (pos - 1 < 0 or program[pos - 1] not in ['<', '-']):#in [' ', '\n', '\t']):
                while pos < len(program) and program[pos] != '\n':
                    pos += 1
                # temp += program[pos]
            else:
                temp += program[pos]
                pos += 1
        else:
            temp += program[pos]
            pos += 1
                
    return temp
    

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
    # TypeBuilder(context, errors).visit(ast)
    # CyclicDependency(context, errors)
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
        # TypeBuilder(context, errors).visit(ast)
        # CyclicDependency(context, errors)
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
        # TypeBuilder(context, errors).visit(ast)
        # CyclicDependency(context, errors)
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

def ast_null(ast, context, errors, program, scope):
    new_ast = COOLwithNULL(context).visit(ast)
    scope = Scope()
    COOLwithNULL_Type(context, errors, program).visit(new_ast, scope)
    return new_ast
    
    
###########################
##### FINAL EXECUTION #####
###########################

@app.command()
def final_execution(program_file, program_file_out, debug: bool = False, verbose=False):
    context = Context()
    scope = Scope()
    
    ###########
    ## LEXER ##
    ###########
    
    errors, program, tokens = tokenize(program_file, debug, verbose)

    if errors or lexer_errors:
        for (_, line, col, value) in lexer_errors:
            totallines = program.count('\n')
            col = get_tokencolumn(program, col) if get_tokencolumn(program, col) > 1 else 2
            print_errors(f'({line}, {col - 1}) - LexicographicError: ERROR \"{value}\"')
        for e in errors:
            print_errors(e)
        exit(1)

    ############
    ## PARSER ##
    ############

    ast = parse(program, debug=debug)

    if ast is None and not parser_errors:
        print_errors("(0, 0) - SyntacticError: ERROR at or near EOF")
        exit(1)

    if parser_errors:  
        for (line, lexpos, _, value) in parser_errors:
            current_line = line - program.count('\n')
            col = get_tokencolumn(program, lexpos) if get_tokencolumn(program, lexpos) > 1 else 2
            print_errors(f'({current_line}, {col-1}) - SyntacticError: ERROR at or near "{value}"')
        exit(1)
     
    ##############
    ## SEMANTIC ##
    ##############
    
    else:
        PositionAssigner(tokens).visit(ast)
        TypeCollector(context, errors).visit(ast)
        TypeBuilderForInheritance(context, errors).visit(ast)
        topological_sorting(ast, context, errors)
        if not errors:
            TypeBuilderForFeatures(context, errors).visit(ast)
            OverriddenMethodChecker(context, errors).visit(ast)
            InferenceChecker(context, errors).visit(ast, Scope())
            TypeChecker(context, errors).visit(ast, scope)
        
        if errors:
            for item in errors:
                print_errors(item)
            exit(1)
        
        #######################
        ### CODE GENERATION ###  
        #######################
        
        new_ast = ExtendedCoolTranslator(context).visit(ast)
        
        scope = Scope()
        ExtendedCoolTypeChecker(context, errors).visit(new_ast, scope)
        
        cil_ast = CoolToCilTranslator(context).visit(new_ast, scope)
        mips_ast = CilToMipsTranslator(context).visit(cil_ast)
        program_result = MipsFormatter1().visit(mips_ast)
        
        write_file(program_file_out, program_result)
         

    
if __name__ == '__main__':
    app()