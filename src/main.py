import sys
from pathlib import Path

class Compiler:
    
    def __init__(self, input_file, output_file):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.code = ''

        print(self.input_file)
        print(self.output_file)

        if not str(self.input_file).endswith('.cl'):
            print('El archivo de entrada debe terminar en .cl')
            exit(1)

        try:
            with open(self.input_file, encoding = 'utf-8') as file:
                self.code += file.read()
        except (IOError, FileNotFoundError):
            print('El archivo de entrada no fue encontrado')
            exit(1)

        self.steps = [ self.lexing ]

    def compile(self):
        for step in self.steps:
            step()

    def lexing(self):
        print('lexing')

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    Compiler(input_file, output_file).compile()

if __name__ == '__main__':
    main()