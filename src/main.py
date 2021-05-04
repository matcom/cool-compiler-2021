import sys
from cmp.lexer import Lexer
from cmp.parser import Parser

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

def main():
    input_file = sys.argv[1]
    output_file = input_file[:-2] + 'mips'

    data = open(input_file).read()
    errors = []

    lex = lexer(data, errors)
    if errors: exit(1)
    
    ast = parser(data, errors, lex) 
    if errors: exit(1)
    
    exit(0)

if __name__ == '__main__':
    main()