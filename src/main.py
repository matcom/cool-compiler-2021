import sys
from parser import CoolParser
from lexer import CoolLexer


def main(input, output):
    try:
        with open(input) as f:
            text = f.read()

        lexer = CoolLexer()
        tokens = lexer.run(text)

        parser = CoolParser(lexer)
        ast = parser.parse(text, debug=True)

    except FileNotFoundError:
        pass


if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]

    main(input, output)
