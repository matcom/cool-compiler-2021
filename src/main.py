import os.path
import sys
from pathlib import Path

from cool.lexer import CoolLexer, main
from cool.parser.parser import CoolParser
from cool.semantic.semantic import main_semantic
from cool.utils.errors import SyntacticError

if __name__ == '__main__':
    path: str = f"{Path.cwd()}/src/cool/code.cl" if os.path.exists(
        f"{Path.cwd()}/src/cool/code.cl") else f"{Path.cwd()}/cool/code.cl"

    _in = sys.argv[1] if len(sys.argv) > 1 else path
    _out = sys.argv[2] if len(sys.argv) > 2 else None

    text: str = ''

    with open(_in) as file:
        text = file.read()

    lexer = main(text, _out)

    lexer.lexer.lineno = 1
    lexer.lexer.linestart = 0

    tokens = lexer.tokenize(text)

    if len(tokens) == 0:
        error_text = SyntacticError.ERROR % 'EOF'
        print(SyntacticError(error_text, 0, 0))
        raise Exception()

    # print(lexer)

    lexer.lexer.lineno = 1
    lexer.lexer.linestart = 0

    parser = CoolParser(lexer)
    ast = parser.parse(text)

    if parser.errors:
        raise Exception()

    ast, errors, context, scope = main_semantic(ast, True)

    if errors:
        for err in errors:
            print(err)
        raise Exception()
