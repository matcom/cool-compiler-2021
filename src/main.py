import sys
from Lexer.lexer import Lexer

def main():
    input_file = sys.argv[1]
    output_file = input_file[:-2] + 'mips'
    
    errors = []
    lexer = Lexer(errors)
    tokens = lexer.Tokenizer(open(input_file).read())
    
    if errors:
        for err in errors:
            print(err)
        exit(1)
    else:
        exit(0)

if __name__ == '__main__':
    main()
