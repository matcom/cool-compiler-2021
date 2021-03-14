"""
MIPS package
"""

from typing import List
from cool_cmp.mips.interface import IMips
from cool_cmp.cil import CilPipeline
from cool_cmp.shared import SymbolTable, InterfacePipeline

class MipsPipeline(InterfacePipeline):
    def __init__(self, cil_pipeline:CilPipeline, *mipses:List[IMips]):
        super().__init__(cil_pipeline, *mipses)
        
    def __call__(self, program:str)->SymbolTable:
        return super().__call__(program)