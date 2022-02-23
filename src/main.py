import parser
import sys
from typing import List

from compiler_components.compiler_component import CompilerComponent
from compiler_components.lexer import Lexer
from compiler_components.cool_parser import Parser
from compiler_components.semantic_checker import SemanticChecker
from compiler_components.code_generator import CodeGenerator

def execute_compiler(cool_program : str):
    # Initialize compiler components
    lexer = Lexer(cool_program)
    cool_parser = Parser(lexer)
    semantic_checker = SemanticChecker(cool_parser)
    code_generator = CodeGenerator(semantic_checker)

    # Execute compiler components
    compiler_components: List[CompilerComponent] = [lexer, cool_parser, semantic_checker, code_generator]
    for component in compiler_components:
        component.execute()

        if component.has_errors():
            component.print_errors()
            # with errors
            print('with errors')
            return True

    # TODO: write generated code to output file 

    # without errors
    print('false')
    return False

if __name__ == '__main__':
    # read input file
    inputfile = sys.argv[1]
    with open(inputfile, encoding="utf_8")as file:
        coolprogram =  file.read()
    
    with_errors: bool = execute_compiler(cool_program = coolprogram)
    if with_errors:
        exit(1)