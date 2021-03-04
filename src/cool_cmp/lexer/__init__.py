"""
Cool lexical analysis package
"""

from cool_cmp.shared.token import Token
from cool_cmp.lexer.interface import ILexer
from cool_cmp.shared.pipeline import PipeResult, Pipeline, Pipe

class LexerPipeline(Pipeline):

    def __init__(self, lexer:ILexer):
        result = PipeResult()

        def get_tokens(program:str):
            tokens = lexer(program)
            result.tokens = tokens
            return result

        super().__init__(Pipe(get_tokens))

    def __call__(self, program:str)->PipeResult:
        return super().__call__(program)
