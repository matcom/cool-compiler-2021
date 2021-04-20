import sys
from lexer.grammar import CoolGrammar

def Lexer(input_file, output_file):
    print(CoolGrammar())

def main():
    input_file = sys.argv[1]
    output_file = input_file[:-2] + 'mips'
    Lexer(input_file, output_file)
    exit(0)

if __name__ == '__main__':
    main()
