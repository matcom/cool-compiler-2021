
import lexer.lexer as lexer
import c_parser.parser as parser

with open('/home/regnod/Documents/cmp_compiler/cmp/cool-compiler-2021/tests/lexer/string3.cl') as f:
    program =  f.read()

coolLexer = lexer.CoolLexer()
coolLexer.build()
tokens = coolLexer.input(program)
for error in coolLexer.errors:
    print(error)
# coolParser = parser.CoolParser()
# ast = coolParser.parse(coolLexer, program)
a = 0
