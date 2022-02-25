import os.path
import sys
from pathlib import Path

from cool.lexer import CoolLexer, main
from cool.parser.parser import CoolParser
from cool.semantic.semantic import main_semantic
from cool.utils.errors import SyntacticError
from cool.codegen.codegen import run_pipeline

if __name__ == '__main__':
    add = "codegen/hello_world.cl"

    path: str = f"{Path.cwd()}/tests/{add}" if os.path.exists(
        f"{Path.cwd()}/tests/{add}") else f"{Path.cwd()}/../tests/{add}"

    out: str = f"{Path.cwd()}/mips-code.asm"

    _in = sys.argv[1] if len(sys.argv) > 1 else path
    _out = sys.argv[2] if len(sys.argv) > 2 else out

    text: str = ''

    with open(_in) as file:
        text = file.read()

    lexer = main(text, _out)  # into call to tokenize text

    lexer.lexer.lineno = 1
    lexer.lexer.linestart = 0

    tokens = lexer.tokenize(text)

    if len(tokens) == 0:
        error_text = SyntacticError.ERROR % 'EOF'
        print(SyntacticError(error_text, 0, 0))
        raise Exception()

    parser = CoolParser(CoolLexer())
    ast = parser.parse(text)

    if parser.errors:
        raise Exception()

    ast, errors, context, scope = main_semantic(ast, False)

    if errors:
        for err in errors:
            print(err)
        raise Exception()
    else:
        mips_code = run_pipeline(context, ast, scope)
        with open(_out, 'w+') as file:
            file.write(mips_code)
