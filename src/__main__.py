import sys
from cool.lexer.lexer import Lexer, main
from cool.utils.LexerTokens import *
from cool.Parser.parser import Parser
from cool.semantic.semanticAnalizer import run_semantic_pipeline
from cool.cil_builder.cilAnalizer import run_code_gen_pipeline


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    with open(input_file, encoding="utf-8") as file:
        text = file.read()
 
    lexer = main(text)            
    tokens = lexer.tokenize()

    if (len(lexer.errors)!= 0):
        for e in lexer.errors:
            print(e)
        raise Exception()


    parser = Parser(Lexer(text))
    ast = parser.parse(text)

    if parser.found_error:
        print(parser.errors[0])
        raise Exception()

    context,scope = run_semantic_pipeline(ast)
    mips_output = run_code_gen_pipeline(ast,context,scope)

    with open(sys.argv[2], 'w') as f:
        f.write(f'{mips_output}')


