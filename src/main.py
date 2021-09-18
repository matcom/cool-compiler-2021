import sys

from ply.lex import lex

from Parser.parser import Parser
from Semantic.builder import TypeBuilder
from Semantic.check import TypeCheck
from Semantic.collector import Type_Collector

def check_errors(errors):
    if  errors:
        for e in errors:
            print(e)
        exit(1)

def parser(data, errors):
    parser = Parser(errors)
    ast = parser(data)
    check_errors(errors)
    return ast

def collector(ast, errors):
    collector = Type_Collector(errors)
    context = collector.visit(ast)
    check_errors(errors)
    return context

def builder(ast, context, errors):
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    check_errors(errors)

def check(ast, contex, errors):
    check = TypeCheck(contex, errors)
    scope = check.visit(ast)
    check_errors(errors)
    return scope

def main():
    errors = list()
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    data = open(input_file, 'r').read()

    ast = parser(data, errors)
    context = collector(ast, errors)
    builder(ast, context, errors)
    scope = check(ast, context, errors)

    exit(0) 

if __name__=='__main__':
    main()