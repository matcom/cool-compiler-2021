import sys

from ply.lex import lex

from lexer.lexer import Lexer

def check_errors(errors):
    for e in errors:
        print(e)

def lexer(data, errors):
    lexer = Lexer(errors)
    lexer.tokenizer(data)
    check_errors(errors)
    return lex

def main():
    errors = list()
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    data = open(input_file, 'r').read()

    lex = lexer(data, errors)

    exit(0) if not errors else exit(1)

if __name__=='__main__':
    main()