import sys

from lexing import lexer


def main():
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        raise Exception("Incorrect number of arguments")

    program = open(input_file).read()
    lexer.input(program)
    for token in lexer:
        a = token
    if lexer.errors:
        print(lexer.errors[0])
        exit(1)


main()
