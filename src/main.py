import sys

from Parser import Parser
from Semantic import *
from CIL import CIL, cil
from MIPS import MIPS

def check_errors(errors):
    if errors: 
        for error in errors: 
            print(error)
        exit(1)

def main():
    #Input and Output files
    cool_file = sys.argv[1]
    cil_file = sys.argv[2]
    mips_file = sys.argv[3]

    # List of the errors
    errors = list()
    
    # Read a cool file
    code = open(cool_file, 'r').read()

    # Lexer and Parser
    parser = Parser(errors)
    ast = parser(code)
    check_errors(errors)

    # Semantic
    context = TypeCollector(errors).visit(ast)
    check_errors(errors)
    TypeBuilder(context, errors).visit(ast)
    check_errors(errors)
    TypeCheck(context, errors).visit(ast)
    check_errors(errors)

    # Generate code
    cil = CIL(context).visit(ast)
    open(cil_file, 'w').write(str(cil))

    mips = MIPS()
    mips.visit(cil)
    open(mips_file, 'w').write(str(mips))

    # Check of errors and exit program
    exit(0)

if __name__=='__main__':
    main()