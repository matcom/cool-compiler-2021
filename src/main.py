import sys

from lexer import CoolLexer
from cparser import CoolParser


def main(input_):
    try:
        with open(input_) as f:
            text = f.read()

        print("****LEXER****")
        lexer = CoolLexer()
        tokens = lexer.run(text)

        print("TOKENS")
        print(tokens)

        print("****PARSER****")
        parser = CoolParser(lexer)

        ast = parser.parse(text)
        print(ast)
        if parser.errors:
            print("HUBO ERRORES")

    except FileNotFoundError:
        pass


if __name__ == "__main__":
    # input_ = sys.argv[1]
    # output_ = sys.argv[2]
    # main(input_, output_)

    input_ = '/mnt/d/UH/4to Año/EVEA/Complementos de Compilacion/cool-compiler/cool-compiler-2021/src/mytest.cl'
    main(input_)
