import sys
from pathlib import Path

from cool.lexer import CoolLexer, main
from cool.parser import CoolParser

if __name__ == '__main__':
    # print(f'Argv: {sys.argv} ')
    _in = sys.argv[1] if len(sys.argv) > 1 else f'{Path.cwd()}/src/cool/code.cl'
    _out = sys.argv[2] if len(sys.argv) > 2 else None

    text: str = ''

    with open(_in) as file:
        text = file.read()

    lexer = main(text, _out)

    # print(lexer)

    lexer.lexer.lineno = 1
    lexer.lexer.linestart = 0

    parser = CoolParser()
    result = parser.parse(text)

    # print(result)
