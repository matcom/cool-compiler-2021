import sys
from pathlib import Path

class Compiler:
    
    def __init__(self, input_file, output_file):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)

        print(self.input_file)
        print(self.output_file)


def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    Compiler(input_file, output_file)

if __name__ == '__main__':
    main()