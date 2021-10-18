import sys
from pathlib import Path

from src.cool.lexer import CoolLexer, main
from src.cool.parser.parser import CoolParser
from src.cool.utils.errors import SyntacticError

if __name__ == '__main__':
    # print(f'Argv: {sys.argv} ')

    # path: str = f"{Path.cwd()}/cool/code.cl"  # debug mode
    path: str = f"{Path.cwd()}/src/cool/code.cl"  # normal mode

    _in = sys.argv[1] if len(sys.argv) > 1 else path
    _out = sys.argv[2] if len(sys.argv) > 2 else None

    text: str = ''

    with open(_in) as file:
        text = file.read()

    lexer = main(text, _out)

    tokens = lexer.tokenize(text)

    if len(tokens) == 0:
        error_text = SyntacticError.ERROR % 'EOF'
        print(SyntacticError(error_text, 0, 0))
        raise Exception()

    # print(lexer)

    # lexer.lexer.lineno = 1
    # lexer.lexer.linestart = 0

    parser = CoolParser(lexer)
    result = parser.parse(text)

    # print(result)
