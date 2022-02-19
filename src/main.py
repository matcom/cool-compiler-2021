import os
import sys
from pathlib import Path
from utils.COOL_Grammar import build_COOL_Grammar
from utils.COOL_Lexer import COOL_Lexer
from utils.parser.COOL_parser import COOL_Parser
from cmp.evaluation import evaluate_reverse_parse
from cmp.semantic import Context
from utils.semantic_check.type_collector import TypeCollector
from utils.semantic_check.type_builder import TypeBuilder
from utils.semantic_check.type_checker import TypeChecker 

from utils.parser.LALR_1 import LALR1_Parser

if __name__ == "__main__":
    add = "codegen/arith.cl"

    path: str = f"{Path.cwd()}/tests/{add}" if os.path.exists(
        f"{Path.cwd()}/tests/{add}") else f"{Path.cwd()}/../tests/{add}"

    _in = sys.argv[1] if len(sys.argv) > 1 else path
    
    with open(_in) as file:
        code = file.read()

    G = build_COOL_Grammar()

    # lexer
    lexer = COOL_Lexer() 
    tokens = lexer(code)

    if lexer.errors:
        for error in lexer.errors:
            print(error)
        raise Exception()

    # parser
    parser = COOL_Parser(G)
        
    derivation, operations = parser(tokens)
    
    if parser.error:
        print(parser.error)
        raise Exception()
        
    # ast       
    ast = evaluate_reverse_parse(G, derivation, operations, lexer.fixed_tokens(tokens))
            
    # chequeo semantico
    context = Context()
    semantic_errors = []

    collector = TypeCollector(context, semantic_errors)
    collector.visit(ast)

    builder = TypeBuilder(context, semantic_errors)
    builder.visit(ast)

    checker = TypeChecker(context, semantic_errors)
    scope = checker.visit(ast)
            
    if semantic_errors:
        for error in semantic_errors:
            print(error)                          
        raise Exception()

# generacion de codigo