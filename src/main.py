import sys

from ply.lex import lex

from Parser.parser import Parser
from Semantic.builder import TypeBuilder
from Semantic.collector import Type_Collector

def check_errors(errors):
    for e in errors:
        print(e)

def parser(data, errors):
    parser = Parser(errors)
    ast = parser(data)
    return ast

def collector(ast, errors):
    collector = Type_Collector(errors)
    context = collector.visit(ast)
    return context

def builder(ast, context, errors):
    builder = TypeBuilder(context, errors)
    builder.visit(ast)

def main():
    errors = list()
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    data = open(input_file, 'r').read()

    ast = parser(data, errors)
    context = collector(ast, errors)
    builder(ast, context, errors)

    check_errors(errors)
    exit(0) if not errors else exit(1)

if __name__=='__main__':
    main()