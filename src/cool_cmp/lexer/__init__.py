"""
Cool lexical analysis package
"""

from cool_cmp.shared.token import ICoolToken
from cool_cmp.lexer.interface import ILexer
from cool_cmp.shared.pipeline import Pipeline, Pipe
from cool_cmp.shared import SymbolTable

class LexerPipeline(Pipeline):

    def __init__(self, lexer:ILexer):
        result = SymbolTable()

        def get_tokens(program:str):
            tokens = lexer(program)
            result.tokens = tokens
            errors = lexer.get_errors()
            for error in errors:
                result.add_error(error)
            return result

        super().__init__(Pipe(get_tokens))

    def __call__(self, program:str)->SymbolTable:
        return super().__call__(program)
