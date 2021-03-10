"""
Cool parsing package
"""

from cool_cmp.parser.interface import IParser
from cool_cmp.lexer import LexerPipeline
from cool_cmp.shared import SymbolTable, InterfacePipeline

class ParserPipeline(InterfacePipeline):

    def __init__(self, lexer_pipeline:LexerPipeline, parser:IParser):
        super().__init__(lexer_pipeline, *[parser,])

    def __call__(self, program:str)->SymbolTable:
        return super().__call__(program)
