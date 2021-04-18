"""
Cool lexical analysis package
"""

from cool_cmp.shared.token import ICoolToken
from cool_cmp.lexer.interface import ILexer
from cool_cmp.shared.pipeline import Pipeline, Pipe
from cool_cmp.shared import SymbolTable
from cool_cmp.lexer.lexer2 import CoolLexer2

default_lexer = CoolLexer2()

class LexerPipeline(Pipeline):

    def __init__(self, lexer:ILexer=default_lexer):
        result = SymbolTable()

        def get_tokens(program:str):
            tokens = lexer(program)
            result.tokens = tokens
            errors = lexer.get_errors()
            result.context.update(lexer.get_extra_info())
            for error in errors:
                result.add_error(error)
            return result

        super().__init__(Pipe(get_tokens))

    def __call__(self, program:str)->SymbolTable:
        return super().__call__(program)
