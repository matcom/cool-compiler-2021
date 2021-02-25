from Tools.Lexer import Lexer
from Tools.Parser import CoolParser
from Tools.Tools.evaluation import evaluate_reverse_parse
from Tools.Type_Collector import Type_Collector
from Tools.Type_Builder import Type_Builder
from Tools.Type_Checker import Type_Checker

def main(args):
    try:
        with open(args.file, 'r') as fd:
            code = fd.read()
    except Exception as e:
        print(f"(0,0) - CompilerError: {e.args}")
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
    ast = evaluate_reverse_parse(productions, operations, tokens)

    type_Collector = Type_Collector()
    type_Collector.visit(ast)
    for e in type_Collector.errors:
        print(e)
    if any(type_Collector.errors): exit(1)
    context = type_Collector.Context

    type_Builder = Type_Builder(context)
    type_Builder.visit(ast)
    for e in type_Builder.errors:
        print(e)
    if any(type_Builder.errors): exit(1)

    type_Checker = Type_Checker(context)
    type_Checker.visit(ast)
    for e in type_Checker.errors:
        print(e)
    if any(type_Checker.errors): exit(1)



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='CoolCompiler pipeline')
    parser.add_argument('-f', '--file', type=str, default='code.cl', help='file to read')

    args = parser.parse_args()
    main(args)
