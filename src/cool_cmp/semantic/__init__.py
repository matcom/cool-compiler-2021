"""
Cool semantic package
"""

from typing import List
from cool_cmp.semantic.interface import ISemantic
from cool_cmp.parser import ParserPipeline
from cool_cmp.shared import SymbolTable, InterfacePipeline

class SemanticPipeline(InterfacePipeline):

    def __init__(self, parser_pipeline:ParserPipeline, *semantics:List[ISemantic]):
        super().__init__(parser_pipeline, *semantics)
        
    def __call__(self, program:str)->SymbolTable:
        return super().__call__(program)
