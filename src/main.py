import sys

from ply.lex import lex

from Parser.parser import Parser

def check_errors(errors):
    for e in errors:
        print(e)

def parser(data, errors):
    parser = Parser(errors)
    ast = parser(data)
    check_errors(errors)
    return ast

def main():
    errors = list()
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    data = open(input_file, 'r').read()

    ast = parser(data, errors)

    exit(0) if not errors else exit(1)

if __name__=='__main__':
    main()