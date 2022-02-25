from os import listdir
import sys

from Lexer import CoolLexer
from Parser import evaluate_reverse_parse, CoolParser
from Visitors import Collector, Builder, Inferencer, Verifier
from Cil import COOLToCIL
from Mips import CILToMIPS, MIPSPrinter


def main(file):

    ###INPUT###
    try:
        f_input = open(file, 'r')
        code = f_input.read()
    except:
        print(f"(0, 0) - CompilerError: file {file} not found")
        exit(1)


    ###LEXER###
    lexer = CoolLexer()
    tokens = lexer.tokenize(code)
    
    if len(tokens) == 1 and tokens[0].lex == '$':
        print("(0, 0) - SyntacticError: Unexpected token EOF") 
        exit(1)

    lexer_err = False
    for token in tokens:
        if token.token_type == "ERROR":
            lexer_err = True
            print(token.lex)
    
    if lexer_err:
        exit(1)


    ###PARSER###
    parsedData, (failure, token) = CoolParser(tokens, get_shift_reduce=True)
    
    if failure:
        print(f"({token.row}, {token.column}) - SyntacticError: ERROR at or near \"{token.lex}\"")
        exit(1)

    parse, operations = parsedData
    ast = evaluate_reverse_parse(parse, operations, tokens)
    errors = []


    ###COLLECTOR###
    collector = Collector()
    collector.visit(ast)
    context = collector.context
    errors.extend(collector.errors)


    ###BUILDER###
    builder = Builder(context)
    builder.visit(ast)
    errors.extend(builder.errors)


    ###CHECKER###
    inferencer = Inferencer(context)
    while inferencer.visit(ast)[0]: pass
    inferencer.errors.clear()
    _, scope = inferencer.visit(ast)
    errors.extend(inferencer.errors)

    verifier = Verifier(context)
    verifier.visit(ast)
    for e in verifier.errors:
        if not e in errors:
            errors.append(e)
    
    if errors:
        for (ex, token) in errors:
            print(f"({token.row}, {token.column}) - {type(ex).__name__}: {str(ex)}")
        exit(1)


    ###COOLtoCIL###
    cool_to_cil = COOLToCIL(context)
    cil_ast = cool_to_cil.visit(ast, scope)


    ###CILtoMIPS###
    cil_to_mips = CILToMIPS()
    mips_ast = cil_to_mips.visit(cil_ast)
    printer = MIPSPrinter()
    mips_code = printer.visit(mips_ast)


    ###OUTPUT###
    out_file = file.split(".")
    out_file[-1] = "mips"
    out_file = ".".join(out_file)

    with open(out_file, 'w') as f:
        f.write(mips_code)
        with open("./Mips/mips_lib.asm") as f2:
            f.write("".join(f2.readlines()))

    exit(0)


if __name__ == "__main__":
    file = sys.argv[1]
    main(file)