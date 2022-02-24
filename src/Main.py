from core.lexer.Lexer import Lexer
from core.parser.Parser import CoolParser
from core.tools.Evaluation import evaluate_reverse_parse
from core.semantic.TypeCollector import Type_Collector
from core.semantic.TypeBuilder import Type_Builder
from core.semantic.TypeChecker import Type_Checker
from core.cil.CoolToCilVisitor import COOLToCILVisitor
from core.cil.CilAst import get_formatter
from core.mips.CilToMipsVisitor import CILToMIPSVisitor
from core.mips.MipsAstFormatter import MIPSAstFormatter
import subprocess, re


def main(args):
    try:
        with open(args.file, 'r') as fd:
            code = fd.read()
    except Exception as e:
        print(f"(0,0) - CompilerError: {e.args}")
        print(args.file)
        exit(1)

    lexer = Lexer()
    tokens = lexer.tokenize(code)
    for t in lexer.errors:
        print(t)
    if any(lexer.errors): exit(1)

    productions, operations = CoolParser(tokens)
    for e in CoolParser.errors:
        print(e)
    if any(CoolParser.errors): exit(1)
    COOLast = evaluate_reverse_parse(productions, operations, tokens)

    type_Collector = Type_Collector()
    type_Collector.visit(COOLast)
    for e in type_Collector.errors:
        print(e)
    if any(type_Collector.errors): exit(1)
    context = type_Collector.Context

    type_Builder = Type_Builder(context)
    type_Builder.visit(COOLast)
    for e in type_Builder.errors:
        print(e)
    if any(type_Builder.errors): exit(1)

    type_Checker = Type_Checker(context)
    scope = type_Checker.visit(COOLast)
    for e in type_Checker.errors:
        print(e)
    if any(type_Checker.errors): exit(1)

    CILVisitor = COOLToCILVisitor(type_Checker.Context)
    CILast = CILVisitor.visit(COOLast, scope)
    # print(get_formatter()(CILast))

    MIPSVisitor = CILToMIPSVisitor()
    MIPSAst = MIPSVisitor.visit(CILast)
    MIPSFormatter = MIPSAstFormatter()
    mipsCode = MIPSFormatter.visit(MIPSAst)

    # print(mipsCode)

    out_file = args.file.split(".")
    out_file[-1] = "mips"
    out_file = ".".join(out_file)

    with open(out_file, 'w') as f:
        f.write(mipsCode)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='CoolCompiler pipeline')
    parser.add_argument('-f', '--file', type=str, default='code.cl', help='file to read')

    args = parser.parse_args()
    main(args)
