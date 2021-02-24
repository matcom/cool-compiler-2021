import sys
from pathlib import Path

from utils.errors import *
from lexing.lexer import Lexer
from parsing.parser import Parser

class Compiler:
    
    def __init__(self, input_file, output_file):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.code = ''
        self.lexer = None
        self.parser = None
        self.ast = None

        if not str(self.input_file).endswith('.cl'):
            error_text = CompilerError.WRONG_EXTENTION
            print(CompilerError(0, 0, error_text))
            exit(1)

        try:
            with open(self.input_file, encoding = 'utf-8') as file:
                self.code += file.read()
        except (IOError, FileNotFoundError):
            error_text = CompilerError.UNKNOWN_FILE % str(self.input_file)
            print(CompilerError(0, 0, error_text))
            exit(1)

        self.steps = [ self.lexing, self.parsing ]

    def compile(self):
        for step in self.steps:
            step()

    def lexing(self):
        self.lexer = Lexer()
        tokens = self.lexer.tokenizer(self.code)

        # for token in tokens:
        #     print(token)

        if len(self.lexer.errors) > 0:
            print(self.lexer.errors[0])
            exit(1)
        elif len(tokens) == 0:
            error_text = SyntacticError.ERROR % 'EOF'
            print(SyntacticError(0, 0, error_text))
            exit(1)
        else:
            print('COMPLETED LEXER!!!')

    def parsing(self):
        self.parser = Parser(lexer=self.lexer)
        self.ast = self.parser(self.code)

        if len(self.parser.errors) > 0:
            print(self.parser.errors[0])
            exit(1)
        else:
            print('COMPLETED PARSING!!!')

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    Compiler(input_file, output_file).compile()

if __name__ == '__main__':
    main()