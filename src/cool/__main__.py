import sys
from pathlib import Path

from .lexer import CoolLexer, main
from .parser import CoolParser

if __name__ == '__main__':
    # in_ = sys.argv[1]
    #out_ = sys.argv[2]
    # print(f'Argv: {sys.argv} ')
    _in = sys.argv[1] if len(sys.argv) > 1 else f'{Path.cwd()}/cool/code.cl'
    _out = sys.argv[2] if len(sys.argv) > 2 else None

    # print(_in, _out)
    # in_ = f'{sys.argv[1]} {sys.argv[2]}'
    # out_ = f'{sys.argv[3]} {sys.argv[4]}'

    # print(f'{in_}')

    # _in = sys.argv[1]
    # _out = sys.argv[2]

    text: str = ''

    with open(_in) as file:
        text = file.read()

    lexer = main(text, _out)
    
    # print(lexer)
    lexer.lexer.lineno = 1
    lexer.lexer.linestart = 0

    parser = CoolParser(lexer)
    result = parser.parse(text)
    
    # print(result)
