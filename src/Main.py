from Tools.Lexer import Lexer
from Tools.Parser import CoolParser

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

    #print(CoolParser.HasConflict)

    productions, operations = CoolParser(tokens)

    for e in CoolParser.errors:
        print(e)

    if any(CoolParser.errors): exit(1)






if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='CoolCompiler pipeline')
    parser.add_argument('-f', '--file', type=str, default='code.cl', help='file to read')

    args = parser.parse_args()
    main(args)
