
import lexer.lexer as lexer
import c_parser.parser as parser
from pipeline import Pipeline


# with open('/home/yumenio/Documents/cmp/cool-compiler-2021/cool-compiler-2021/tests/semantic/self4.cl') as f:
with open('../tests/boku/test1.cl') as f:
    program =  f.read()

coolLexer = lexer.CoolLexer()
coolLexer.build()
tokens = coolLexer.input(program)
# for error in coolLexer.errors:
#     print(error)
Pipeline(program, lexer.CoolLexer(),parser.CoolParser(), False)
coolParser = parser.CoolParser()

ast = coolParser.parse(lexer.CoolLexer(), program)
for lexing_error in coolParser.lexer.errors:
    print(lexing_error)
for parsing_error in coolParser.errors:
    print(parsing_error)
a = 0