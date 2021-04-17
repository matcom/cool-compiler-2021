"""
CIL package
"""

from typing import List
from cool_cmp.shared import SymbolTable, InterfacePipeline
from cool_cmp.semantic import SemanticPipeline
from cool_cmp.cil.interface import ICil

class CilPipeline(InterfacePipeline):
    def __init__(self, semantic_pipeline:SemanticPipeline, *cils:List[ICil]):
        super().__init__(semantic_pipeline, *cils)
        
    def __call__(self, program:str)->SymbolTable:
        return super().__call__(program)
