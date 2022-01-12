import sys

from lexer import CoolLexer
from cparser import CoolParser


def main(_input, _output):

    with open(_input) as file:
        text = file.read()

    lexer = CoolLexer()
    tokens = lexer.run(text)

    # parser = CoolParser(lexer)

    # ast = parser.parse(text)


if __name__ == "__main__":

    path = '/mnt/d/UH/4to Año/EVEA/Complementos de Compilacion/cool-compiler/cool-compiler-2021/tests/lexer/mixed2.cl'
    _input = sys.argv[1] if len(sys.argv) > 1 else path
    _output = sys.argv[2] if len(sys.argv) > 2 else None

    main(_input, _output)

    # input_ = '/mnt/d/UH/4to Año/EVEA/Complementos de Compilacion/cool-compiler/cool-compiler-2021/tests/lexer/iis4.cl'
    # main(input_)
