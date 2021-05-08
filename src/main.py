import sys
from cmp.lexer import Lexer
from cmp.parser import Parser
from cmp.collector import TypeCollector
from cmp.builder import TypeBuilder
from cmp.check import TypeCheck

def lexer(data, errors):
    lex = Lexer(errors)
    tokens = lex.tokenizer(data)

    for err in errors:
        print(err)
    
    return lex

def parser(data, errors, lexer):
    par = Parser(lexer.tokens, errors)
    ast = par(data, lexer)

    for err in errors:
        print(err)
    
    return ast

def collector(ast, errors):
    col = TypeCollector(errors)
    col.visit(ast)

    for err in errors:
        print(err)
    
    return col.context

def builder(ast, context, errors):
    build = TypeBuilder(context, errors)
    build.visit(ast)

    for err in errors:
        print(err)

def check(ast, context, errors):
    check = TypeCheck(context, errors)
    scope = check.visit(ast)

    for err in errors:
        print(err)
    
    return scope

def main():
    input_file = sys.argv[1]
    output_file = input_file[:-2] + 'mips'

    data = open(input_file).read()
    errors = []

    lex = lexer(data, errors)
    if errors: exit(1)
    
    ast = parser(data, errors, lex) 
    if errors: exit(1)

    context = collector(ast, errors)
    if errors: exit(1)

    builder(ast, context, errors)
    if errors: exit(1)

    scope = check(ast, context, errors)
    if errors: exit(1)
    
    exit(0)

if __name__ == '__main__':
    main()