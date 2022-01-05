import sys

from src.lexer import CoolLexer
from src.parser import CoolParser


def main(input, output):
    try:
        with open(input) as f:
            text = f.read()

        lexer = CoolLexer()
        tokens = lexer.run(text)
        print(tokens)

        parser = CoolParser(lexer)

        ast = parser.parse(text)
        print(ast)
        if parser.errors:
            raise Exception()

    except FileNotFoundError:
        pass


if __name__ == "__main__":
    input_ = sys.argv[1]
    output_ = sys.argv[2]

    main(input_, output_)
