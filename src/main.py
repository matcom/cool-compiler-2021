import argparse 
from utils.COOL_Grammar import build_COOL_Grammar
from utils.COOL_Lexer import COOL_Lexer
from utils.parser.COOL_parser import COOL_Parser
from cmp.evaluation import evaluate_reverse_parse
from cmp.semantic import Context
from utils.semantic_check.type_collector import TypeCollector
from utils.semantic_check.type_builder import TypeBuilder
from utils.semantic_check.type_checker import TypeChecker

def main(args):
    
    try:
        with open(args.file, 'r') as file:
            code = file.read()
    except:
        print(f"(0,0) - CompilerError: file {args.file} not found")
        exit(1)

    G = build_COOL_Grammar()

    # lexer
    lexer = COOL_Lexer() 
    tokens = lexer(code)

    if lexer.errors:
        for error in lexer.errors:
            print(error)
        exit(1)

    # parser
    parser = COOL_Parser(G)
    derivation, operations = parser(tokens)
    
    if parser.error:
        print(parser.error)
        exit(1)

    # ast       
    ast = evaluate_reverse_parse(G, derivation, operations, tokens)
            
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
        exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='description')
    parser.add_argument('-f', '--file', type=str, default='', help='file to read')

    args = parser.parse_args()
    main(args)