import sys

from lexer import CoolLexer
from parser import CoolParser


def main(input_):
    try:
        with open(input_) as f:
            text = f.read()

        print(text)

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
    # input_ = sys.argv[1]
    # output_ = sys.argv[2]
    # main(input_, output_)

    input_ = 'mytest.cl'
    main(input_)
