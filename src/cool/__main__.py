from .lexer import CoolLexer, main
from pathlib import Path
import sys

if __name__ == '__main__':
    # in_ = sys.argv[1]
    #out_ = sys.argv[2]
    # print(f'Argv: {sys.argv} ')
    #in_ = sys.argv[1] if len(sys.argv) > 1 else f'{Path.cwd()}/cool/code.cl'
    #out_ = sys.argv[2] if len(sys.argv) > 1 else None

    # in_ = f'{sys.argv[1]} {sys.argv[2]}'
    # out_ = f'{sys.argv[3]} {sys.argv[4]}'

    # print(f'{in_}')

    in_ = sys.argv[1]
    out_ = sys.argv[2]
    main(in_, out_)