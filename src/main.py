import sys

from lexer import CoolLexer
from cparser import CoolParser


def main(input_):
    try:
        with open(input_) as f:
            text = f.read()

        lexer = CoolLexer()
        tokens = lexer.run(text)

        # parser = CoolParser(lexer)

        # ast = parser.parse(text)

    except FileNotFoundError:
        raise Exception()


if __name__ == "__main__":
    # input_ = sys.argv[1]
    # output_ = sys.argv[2]
    # main(input_, output_)

    input_ = '/mnt/d/UH/4to Año/EVEA/Complementos de Compilacion/cool-compiler/cool-compiler-2021/tests/lexer/iis4.cl'
    main(input_)
