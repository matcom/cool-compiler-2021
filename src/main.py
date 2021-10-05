import sys

from ply.lex import lex
from CIL.cil import CIL
from MIPS.mips import MIPS

from Parser.parser import Parser
from Semantic.builder import TypeBuilder
from Semantic.check import TypeCheck
from Semantic.collector import Type_Collector

def check_errors(errors):
    if  errors:
        for e in errors:
            print(e)
        exit(1)

def parser(data, errors):
    parser = Parser(errors)
    ast = parser(data)
    check_errors(errors)
    return ast

def collector(ast, errors):
    collector = Type_Collector(errors)
    context = collector.visit(ast)
    check_errors(errors)
    return context

def builder(ast, context, errors):
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    check_errors(errors)

def check(ast, contex, errors):
    check = TypeCheck(contex, errors)
    scope = check.visit(ast)
    check_errors(errors)
    return scope

def cil(ast, contex, cil_file):
    cil = CIL(contex)
    cil_ast = cil.visit(ast)
    open(cil_file, 'w').write(str(cil_ast))
    return cil_ast

def mips(ast, output_file):
    mips = MIPS()
    code = mips.visit(ast) 
    open(output_file, 'w').write(code)

def main():
    errors = list()
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    cil_file = f'{input_file[:-2]}.cil'

    data = open(input_file, 'r').read()

    ast = parser(data, errors)
    context = collector(ast, errors)
    builder(ast, context, errors)
    scope = check(ast, context, errors)
    cil_ast = cil(ast, context, cil_file)
    #mips(cil_ast, output_file)

    exit(0) 

if __name__=='__main__':
    main()