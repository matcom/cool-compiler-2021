from cool_cmp.parser.interface import IParser
from cool_cmp.lexer.interface import ICoolToken
from cool_cmp.shared.errors import ErrorTracker
from cool_cmp.parser.errors import SyntacticCoolError
from cool2.cool.parser.cool_parser import cool_parser
from cool2.cool.pipeline import syntax_pipeline
from cool_cmp.shared.ast import BaseAST
from typing import List,Dict

class CoolParer2(IParser):
    
    @property
    def name(self)->str:
        return "parser"
    
    def __init__(self):
        self.error_tracker = ErrorTracker() # Error tracker implementation
    
    def __call__(self, tokens:List[ICoolToken], context:Dict[str,object]) -> BaseAST:
        result = syntax_pipeline(context)
        new_keys = set(result.keys()).difference(set(context.keys()))
        for key in new_keys:
            self.add_extra_info(key, result[key])
        return BaseAST(result["ast"])
                        
    
    def add_error(self, error:SyntacticCoolError):
        self.error_tracker.add_error(error)
    
    def get_errors(self)->List[SyntacticCoolError]:
        errors = self.error_tracker.get_errors()
        return errors
